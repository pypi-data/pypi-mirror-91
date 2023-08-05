import json
import logging
import os
import shutil
from collections import OrderedDict
from typing import List, Dict, Tuple, Iterable, Type
from zipfile import ZipFile

import numpy as np
import torch
from numpy import ndarray
from torch import nn
from tqdm import tqdm

from soco_encoders import __DOWNLOAD_SERVER__
from soco_encoders import __version__
from soco_encoders.util import import_from_string, http_get


class SentenceTransformer(nn.Sequential):
    def __init__(self, model_name_or_path: str = None, modules: Iterable[nn.Module] = None, device: str = None):
        if modules is not None and not isinstance(modules, OrderedDict):
            modules = OrderedDict([(str(idx), module) for idx, module in enumerate(modules)])

        if model_name_or_path is not None and model_name_or_path != "":
            logging.info("Load pretrained SentenceTransformer: {}".format(model_name_or_path))

            if '/' not in model_name_or_path and '\\' not in model_name_or_path and not os.path.isdir(model_name_or_path):
                logging.info("Did not find a / or \\ in the name. Assume to download model from server")
                model_name_or_path = __DOWNLOAD_SERVER__ + model_name_or_path + '.zip'

            if model_name_or_path.startswith('http://') or model_name_or_path.startswith('https://'):
                model_url = model_name_or_path
                folder_name = model_url.replace("https://", "").replace("http://", "").replace("/", "_")[:250]

                try:
                    from torch.hub import _get_torch_home
                    torch_cache_home = _get_torch_home()
                except ImportError:
                    torch_cache_home = os.path.expanduser(
                        os.getenv('TORCH_HOME', os.path.join(
                            os.getenv('XDG_CACHE_HOME', '~/.cache'), 'torch')))
                default_cache_path = os.path.join(torch_cache_home, 'sentence_transformers')
                model_path = os.path.join(default_cache_path, folder_name)
                os.makedirs(model_path, exist_ok=True)


                if not os.listdir(model_path):
                    if model_url[-1] is "/":
                        model_url = model_url[:-1]
                    logging.info("Downloading sentence transformer model from {} and saving it at {}".format(model_url, model_path))
                    try:
                        zip_save_path = os.path.join(model_path, 'model.zip')
                        http_get(model_url, zip_save_path)
                        with ZipFile(zip_save_path, 'r') as zip:
                            zip.extractall(model_path)
                    except Exception as e:
                        shutil.rmtree(model_path)
                        raise e
            else:
                model_path = model_name_or_path

            #### Load from disk
            if model_path is not None:
                logging.info("Load SentenceTransformer from folder: {}".format(model_path))
                with open(os.path.join(model_path, 'modules.json')) as fIn:
                    contained_modules = json.load(fIn)

                modules = OrderedDict()
                for module_config in contained_modules:
                    model_type = module_config['type']
                    if 'soco_sentence_transformers' in model_type:
                        model_type = model_type.replace('soco_sentence_transformers', 'soco_encoders')
                    module_class = import_from_string(model_type)
                    module = module_class.load(os.path.join(model_path, module_config['path']))
                    modules[module_config['name']] = module


        super().__init__(modules)
        if device is None:
            device = "cuda" if torch.cuda.is_available() else "cpu"
            logging.info("Use pytorch device: {}".format(device))
        self.device = torch.device(device)
        self.to(device)

    def encode(self, sentences: List[str], batch_size: int = 8, show_progress_bar: bool = None) -> List[ndarray]:
        """
       Computes sentence embeddings

       :param sentences:
           the sentences to embed
       :param batch_size:
           the batch size used for the computation
       :param show_progress_bar:
            Output a progress bar when encode sentences
       :return:
           a list with ndarrays of the embeddings for each sentence
       """
        if show_progress_bar is None:
            show_progress_bar = (logging.getLogger().getEffectiveLevel()==logging.INFO or logging.getLogger().getEffectiveLevel()==logging.DEBUG)

        all_embeddings = []
        length_sorted_idx = np.argsort([len(sen) for sen in sentences])

        iterator = range(0, len(sentences), batch_size)
        if show_progress_bar:
            iterator = tqdm(iterator, desc="Batches")

        for batch_idx in iterator:
            batch_tokens = []

            batch_start = batch_idx
            batch_end = min(batch_start + batch_size, len(sentences))

            longest_seq = 0

            for idx in length_sorted_idx[batch_start: batch_end]:
                sentence = sentences[idx]
                tokens = self.tokenize(sentence)
                longest_seq = max(longest_seq, len(tokens))
                batch_tokens.append(tokens)

            features = {}
            for text in batch_tokens:
                sentence_features = self.get_sentence_features(text, longest_seq)

                for feature_name in sentence_features:
                    if feature_name not in features:
                        features[feature_name] = []
                    features[feature_name].append(sentence_features[feature_name])

            for feature_name in features:
                features[feature_name] = torch.tensor(np.asarray(features[feature_name])).to(self.device)

            with torch.no_grad():
                embeddings = self.forward(features)
                embeddings = embeddings['sentence_embedding'].to('cpu').numpy()
                all_embeddings.extend(embeddings)


        reverting_order = np.argsort(length_sorted_idx)
        all_embeddings = [all_embeddings[idx] for idx in reverting_order]

        return all_embeddings

    def tokenize(self, text):
        return self._first_module().tokenize(text)

    def get_sentence_features(self, *features):
        return self._first_module().get_sentence_features(*features)

    def get_sentence_embedding_dimension(self):
        return self._last_module().get_sentence_embedding_dimension()

    def _first_module(self):
        """Returns the first module of this sequential embedder"""
        return self._modules[next(iter(self._modules))]

    def _last_module(self):
        """Returns the last module of this sequential embedder"""
        return self._modules[next(reversed(self._modules))]

    def save(self, path):
        """
        Saves all elements for this seq. sentence embedder into different sub-folders
        """
        logging.info("Save model to {}".format(path))
        contained_modules = []

        for idx, name in enumerate(self._modules):
            module = self._modules[name]
            model_path = os.path.join(path, str(idx)+"_"+type(module).__name__)
            os.makedirs(model_path, exist_ok=True)
            module.save(model_path)
            contained_modules.append({'idx': idx, 'name': name, 'path': os.path.basename(model_path), 'type': type(module).__module__})

        with open(os.path.join(path, 'modules.json'), 'w') as fOut:
            json.dump(contained_modules, fOut, indent=2)

        with open(os.path.join(path, 'config.json'), 'w') as fOut:
            json.dump({'__version__': __version__}, fOut, indent=2)

    def smart_batching_collate(self, batch):
        """
        Transforms a batch from a SmartBatchingDataset to a batch of tensors for the model

        :param batch:
            a batch from a SmartBatchingDataset
        :return:
            a batch of tensors for the model
        """
        num_texts = len(batch[0][0])

        labels = []
        paired_texts = [[] for _ in range(num_texts)]
        max_seq_len = [0] * num_texts
        for tokens, label in batch:
            labels.append(label)
            for i in range(num_texts):
                paired_texts[i].append(tokens[i])
                max_seq_len[i] = max(max_seq_len[i], len(tokens[i]))

        features = []
        for idx in range(num_texts):
            max_len = max_seq_len[idx]
            feature_lists = {}
            for text in paired_texts[idx]:
                sentence_features = self.get_sentence_features(text, max_len)

                for feature_name in sentence_features:
                    if feature_name not in feature_lists:
                        feature_lists[feature_name] = []
                    feature_lists[feature_name].append(sentence_features[feature_name])

            for feature_name in feature_lists:
                feature_lists[feature_name] = torch.tensor(np.asarray(feature_lists[feature_name]))

            features.append(feature_lists)

        return {'features': features, 'labels': torch.stack(labels)}
