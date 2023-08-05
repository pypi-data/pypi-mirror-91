from soco_encoders.cloud_bucket import CloudBucket
from soco_encoders.encoders import *
from soco_encoders.Tokenizer import Tokenizer
from soco_encoders.util import Pack
from soco_device import DeviceCheck

class EncoderLoader(object):

    @staticmethod
    def _load_sent_transformer(config, model_family, model_id, use_gpu, region):
        bucket = CloudBucket(region)
        model_dir = bucket.download_transformer_model(model_family, model_id)

        constructor = globals()[config.encoder_class]
        model = constructor(model_dir, config)
        model.eval()
        if use_gpu:
            model.to(config.device)

        return model

    @staticmethod
    def _load_term_transformer(config, model_family, model_id, use_gpu, region):
        bucket = CloudBucket(region)
        model_dir = bucket.download_term_transformer_model(model_family, model_id)

        constructor = globals()[config.encoder_class]
        model = constructor(model_dir, config)
        model.eval()
        if use_gpu:
            model.to(config.device)

        return model

    @staticmethod
    def load_model(model_family, model_id, use_gpu, region='us', device_name='cpu'):
        if not torch.cuda.is_available():
            use_gpu = False

        bucket = CloudBucket(region)
        model_dir = bucket.download_config(model_family, model_id)
        config = json.load(open(os.path.join(model_dir, 'config.json')))
        if device_name.startswith("cuda") or device_name.startswith("gpu"):
            device = torch.device(device_name)
        else:
            device_check = DeviceCheck()
            device_name, device_ids = device_check.get_device_by_model(model_id, n_gpu=1 if use_gpu else 0)
            device_name = '{}:{}'.format(device_name, device_ids[0]) if len(device_ids) == 1 else device_name
            device = torch.device(device_name)

        config['use_gpu'] = False if device_name == 'cpu' else True
        config['device'] = device
        config = Pack(config)
        if config.encoder_class == 'TransformerWrapper':
            return EncoderLoader._load_sent_transformer(config, model_family, model_id, use_gpu, region)
        elif config.encoder_class == 'TermTransformer':
            return EncoderLoader._load_term_transformer(config, model_family, model_id, use_gpu, region)

        else:
            raise Exception("{} is unknown.".format(config.encoder_class))

    @staticmethod
    def load_tokenizer(model_id, region='us'):
        return Tokenizer(model_id, region)

