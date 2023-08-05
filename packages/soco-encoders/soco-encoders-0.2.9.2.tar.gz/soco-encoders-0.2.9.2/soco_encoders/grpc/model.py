from typing import Union, List, Dict
from soco_encoders.model_loaders import EncoderLoader
from soco_encoders.models.module_bases import BaseEncoder
from collections import OrderedDict
from soco_encoders.config import EnvVars
import soco_encoders.grpc.embedding_pb2_grpc as embedding_pb2_grpc
import soco_encoders.grpc.embedding_pb2 as embedding_pb2
import json
import zlib

class MyModel(embedding_pb2_grpc.EncoderServicer):
    def __init__(self):
        self.models = OrderedDict()

    def load_model(self, model_id):
        if len(self.models) > EnvVars.MAX_NUM_MODEL:
            self.models.popitem(last=False)

        if model_id not in self.models:
            m = EncoderLoader.load_model('pretrain-models', model_id, EnvVars.USE_GPU, EnvVars.REGION)
            self.models[model_id] = m

        return self.models[model_id]

    def _predict(self, model_id: str, text: Union[List[str], str], batch_size: int=10,
                mode: str = BaseEncoder.DEFAULT, kwargs: Dict = None):

        if not kwargs:
            kwargs = None

        if mode == BaseEncoder.TSCORE and kwargs is None:
            kwargs = {'start_symbol': '<a>', 'end_symbol': '</a>', 'return_meta': True,
                      'min_threshold': 1e-2,
                      'top_k': 500,
                      'to_sparse': 'csr',
                      'term_batch_size': 3000,
                      'force_seq_len': -1,
                      'approx_padding': False,
                      'mask_padding': True
                      }

        m = self.load_model(model_id)
        f = m.encode(text, show_progress_bar=True, batch_size=batch_size, mode=mode, args=kwargs)
        if type(f) is tuple:
            f, meta = f
            res = []
            for row_id in range(f.shape[0]):
                coo_row = f[row_id].tocoo()
                terms = []
                for col_id, v in zip(coo_row.col, coo_row.data):
                    terms.append({'score': float(v), 'term': meta['vocab'][col_id]})
                terms = sorted(terms, key=lambda x: x['score'] * -1)
                res.append(terms)
            byte_data = json.dumps(res).encode('utf-8')
            shape = f.shape
            data_type = 1
        else:
            byte_data = f.tobytes()
            shape = f.shape
            data_type = 0

        return byte_data, shape, data_type

    def encode(self, request, context):
        text_list = [t for t in request.text]
        kwargs = json.loads(request.kwargs) if request.kwargs else None
        data, shape, d_type = self._predict(request.model_id, text_list,
                                            batch_size=request.batch_size,
                                            mode=request.mode,
                                            kwargs=kwargs)
        if request.compress == 'zlib':
            data = zlib.compress(data)

        response = embedding_pb2.Embedding(data=data,
                                           shape=shape,
                                           type=d_type,
                                           compress=request.compress)
        return response

if __name__ == '__main__':
    x1 = 'I am from New York city and am a professor in computer science.'
    body = embedding_pb2.Input()
    body.model_id = 'bert-base-nli-stsb-mean-tokens'
    body.text.append(x1)
    x = MyModel().encode(body, None)
    print(x)