import os
import torch
from .util import http_get, import_from_string
import json
from . import __DOWNLOAD_SERVER__
from typing import List, Union, Dict
import numpy as np
import tqdm
import nltk
import torch.multiprocessing as mp
import queue
import math
import re
import logging

logger = logging.getLogger(__name__)


class EasyNMT:
    def __init__(self, model_name: str, cache_folder: str = None, translator=None, device=None, **kwargs):
        self.fasttext_lang_id = None
        self.config = None

        if cache_folder is None:
            if 'EASYNMT_CACHE_DIR' in os.environ:
                cache_folder = os.environ['EASYNMT_CACHE_DIR']
            else:
                cache_folder = os.path.join(torch.hub._get_torch_home(), 'easynmt')
        self.cache_folder = cache_folder

        if translator is not None:
            self.translator = translator
        else:
            if os.path.exists(model_name) and os.path.isdir(model_name):
                model_path = model_name
            else:
                folder_name = model_name.replace("/", "_")
                model_path = os.path.join(cache_folder, folder_name)

                if not os.path.exists(model_path) or not os.listdir(model_path):
                    logger.info("Downloading EasyNMT model {} and saving it at {}".format(model_name, model_path))

                    model_path_tmp = model_path.rstrip("/").rstrip("\\") + "_part"
                    os.makedirs(model_path_tmp, exist_ok=True)

                    #Download easynmt.json
                    config_url = __DOWNLOAD_SERVER__+"/{}/easynmt.json".format(model_name)
                    config_path = os.path.join(model_path_tmp, 'easynmt.json')
                    http_get(config_url, config_path)

                    with open(config_path) as fIn:
                        downloaded_config = json.load(fIn)

                    if 'files' in downloaded_config:
                        for filename, url in downloaded_config['files'].items():
                            logger.info("Download {} from {}".format(filename, url))
                            http_get(url, os.path.join(model_path_tmp, filename))

                    ##Rename tmp path
                    os.rename(model_path_tmp, model_path)

            with open(os.path.join(model_path, 'easynmt.json')) as fIn:
                self.config = json.load(fIn)

            if device is None:
                device = 'cuda' if torch.cuda.is_available() else 'cpu'
            self.device = device

            module_class = import_from_string(self.config['model_class'])
            self.translator = module_class(model_path, **kwargs)

    def translate_sentences(self, sentences: Union[str, List[str]], source_lang: str = None, target_lang: str = None,
                  show_progress_bar: bool = True, beam_size: int = 5, batch_size: int = 8, **kwargs):
        """
        This method translates individual sentences.

        :param sentences: A single sentence or a list of sentences to be translated
        :param source_lang: Source language for all sentences. If none, determines automatically the source language
        :param target_lang: Target language for the translation
        :param show_progress_bar: Show a progress bar
        :param beam_size: Size for beam search
        :param batch_size: Mini batch size
        :return: List of translated sentences
        """

        if source_lang == target_lang:
            return sentences

        is_single_sentence = False
        if isinstance(sentences, str):
            sentences = [sentences]
            is_single_sentence = True

        output = []
        if source_lang is None:
            #Determine languages for sentences
            src_langs = [self.language_detection(sent) for sent in sentences]
            logger.info("Detected languages: {}".format(set(src_langs)))


            #Group by languages
            lang2id = {}
            for idx, lng in enumerate(src_langs):
                if lng not in lang2id:
                    lang2id[lng] = []

                lang2id[lng].append(idx)

            #Translate language wise
            output = [None] * len(sentences)
            for lng, ids in lang2id.items():
                logger.info("Translate sentences of language: {}".format(lng))
                try:
                    grouped_sentences = [sentences[idx] for idx in ids]
                    translated = self.translate_sentences(grouped_sentences, source_lang=lng, target_lang=target_lang, show_progress_bar=show_progress_bar, beam_size=beam_size, batch_size=batch_size, **kwargs)
                    for idx, translated_sentences in zip(ids, translated):
                        output[idx] = translated_sentences
                except Exception as e:
                    logger.warn("Exception: "+str(e))
                    raise e
        else:
            #Sort by length to speed up processing
            length_sorted_idx = np.argsort([len(sen) for sen in sentences])
            sentences_sorted = [sentences[idx] for idx in length_sorted_idx]

            iterator = range(0, len(sentences_sorted), batch_size)
            if show_progress_bar:
                scale = min(batch_size, len(sentences))
                iterator = tqdm.tqdm(iterator, total=len(sentences)/scale, unit_scale=scale, smoothing=0)

            for start_idx in iterator:
                output.extend(self.translator.translate_sentences(sentences_sorted[start_idx:start_idx+batch_size], source_lang=source_lang, target_lang=target_lang, beam_size=beam_size, device=self.device, **kwargs))

            #Restore original sorting of sentences
            output = [output[idx] for idx in np.argsort(length_sorted_idx)]

        if is_single_sentence:
            output = output[0]

        return output

    def translate_documents(self, documents: Union[str, List[str]], source_lang: str = None, target_lang: str = None,
                            show_progress_bar: bool = True, beam_size: int = 5, batch_size: int = 8,
                            paragraph_split="\n", sentence_splitter=None, **kwargs):

        if source_lang == target_lang:
            return documents

        is_single_doc = False
        if isinstance(documents, str):
            documents = [documents]
            is_single_doc = True

        if sentence_splitter is None:
            sentence_splitter = self.sentence_splitting

        translated_paragraphs = []
        sentences_to_translate = []
        sentences_to_translate_index = []
        document_paragraph_endix = []

        for doc in documents:
            #Split document into paragraphs and then into sentences and preserve white spaces
            paragraphs = doc.split(paragraph_split)
            for paragraph in paragraphs:
                if len(paragraph.strip()) == 0:
                    translated_paragraphs.append([paragraph])
                else:
                    splitted_sentences = []
                    for sent in sentence_splitter(paragraph, source_lang):
                        text_start = len(sent) - len(sent.lstrip())
                        text_end = len(sent.rstrip())
                        whitespace_left = sent[0:text_start]
                        whitespace_right = sent[text_end:]

                        para_id = len(translated_paragraphs)
                        sent_id = len(splitted_sentences)
                        sentences_to_translate.append(sent.strip())
                        sentences_to_translate_index.append([para_id, sent_id])
                        splitted_sentences.append([whitespace_left, sent.strip(), whitespace_right])

                    translated_paragraphs.append(splitted_sentences)

            document_paragraph_endix.append(len(translated_paragraphs))

        translated_sentences = self.translate_sentences(sentences_to_translate, source_lang=source_lang, target_lang=target_lang, show_progress_bar=show_progress_bar, beam_size=beam_size, batch_size=batch_size, **kwargs)

        # Merge values back
        for translated_sentence, position in zip(translated_sentences, sentences_to_translate_index):
            translated_paragraphs[position[0]][position[1]][1] = translated_sentence

        for p_idx in range(len(translated_paragraphs)):
            for s_idx in range(len(translated_paragraphs[p_idx])):
                translated_paragraphs[p_idx][s_idx] = "".join(translated_paragraphs[p_idx][s_idx])
            translated_paragraphs[p_idx] = " ".join(translated_paragraphs[p_idx])


        # Recombine
        translated_docs = []
        for idx in range(len(documents)):
            start_idx = document_paragraph_endix[idx-1] if idx > 0 else 0
            end_idx = document_paragraph_endix[idx]
            translated_docs.append(paragraph_split.join(translated_paragraphs[start_idx:end_idx]))

        if is_single_doc:
            translated_docs = translated_docs[0]

        return translated_docs

    def start_multi_process_pool(self, target_devices: List[str] = None):
        """
        Starts multi process to process the encoding with several, independent processes.
        This method is recommended if you want to encode on multiple GPUs. It is advised
        to start only one process per GPU. This method works together with encode_multi_process
        :param target_devices: PyTorch target devices, e.g. cuda:0, cuda:1... If None, all available CUDA devices will be used
        :return: Returns a dict with the target processes, an input queue and and output queue.
        """
        if target_devices is None:
            if torch.cuda.is_available():
                target_devices = ['cuda:{}'.format(i) for i in range(torch.cuda.device_count())]
            else:
                logger.info("CUDA is not available. Start 4 CPU worker")
                target_devices = ['cpu'] * 4

        logger.info("Start multi-process pool on devices: {}".format(', '.join(map(str, target_devices))))

        ctx = mp.get_context('spawn')
        input_queue = ctx.Queue()
        output_queue = ctx.Queue()
        processes = []

        for cuda_id in target_devices:
            p = ctx.Process(target=EasyNMT._encode_multi_process_worker, args=(cuda_id, self, input_queue, output_queue), daemon=True)
            p.start()
            processes.append(p)

        return {'input': input_queue, 'output': output_queue, 'processes': processes}

    def translate_multi_process(self, pool: Dict[str, object], sentences: List[str],  source_lang: str = None, target_lang: str = None, beam_size: int = 5, batch_size: int = 32, chunk_size: int = None):
        """
        This method allows to run encode() on multiple GPUs. The sentences are chunked into smaller packages
        and sent to individual processes, which encode these on the different GPUs. This method is only suitable
        for encoding large sets of sentences
        :param sentences: List of sentences
        :param pool: A pool of workers started with SentenceTransformer.start_multi_process_pool
        :param is_pretokenized: If true, no tokenization will be applied. It is expected that the input sentences are list of ints.
        :param chunk_size: Sentences are chunked and sent to the individual processes. If none, it determine a sensible size.
        """

        if chunk_size is None:
            chunk_size = min(math.ceil(len(sentences) / len(pool["processes"]) / 10), 1000)

        logger.info("Chunk data into packages of size {}".format(chunk_size))

        input_queue = pool['input']
        last_chunk_id = 0

        for start_idx in range(0, len(sentences), chunk_size):
            input_queue.put([last_chunk_id, source_lang, target_lang, beam_size, batch_size, sentences[start_idx:start_idx+chunk_size]])
            last_chunk_id += 1

        output_queue = pool['output']
        results_list = sorted([output_queue.get() for _ in tqdm.trange(last_chunk_id, smoothing=0)], key=lambda x: x[0])
        translated = np.concatenate([result[1] for result in results_list])
        return translated

    @staticmethod
    def stop_multi_process_pool(pool):
        """
        Stops all processes started with start_multi_process_pool
        """
        for p in pool['processes']:
            p.terminate()

        for p in pool['processes']:
            p.join()
            p.close()

        pool['input'].close()
        pool['output'].close()

    @staticmethod
    def _encode_multi_process_worker(target_device: str, translator, input_queue, results_queue):
        """
        Internal working process to encode sentences in multi-process setup
        """

        while True:
            try:
                id, source_lang, target_lang, beam_size, batch_size, sentences = input_queue.get()
                translated = translator.translate_sentences(sentences, source_lang=source_lang, target_lang=target_lang, beam_size=beam_size, show_progress_bar=False, batch_size=batch_size, device=target_device)
                results_queue.put([id, translated])
            except queue.Empty:
                break

    def language_detection(self, text: str) -> str:
        """
        Given a text, detects the language code and returns the ISO language code. It supports 176 languages. Uses
        the fasttext model for language detection:
        https://fasttext.cc/blog/2017/10/02/blog-post.html
        https://fasttext.cc/docs/en/language-identification.html

        :param text: Text for which we want to determine the language
        :return: ISO language code
        """
        if self.fasttext_lang_id is None:
            import fasttext
            model_path = os.path.join(self.cache_folder, 'lid.176.ftz')
            if not os.path.exists(model_path):
                http_get('https://dl.fbaipublicfiles.com/fasttext/supervised-models/lid.176.ftz', model_path)
            self.fasttext_lang_id = fasttext.load_model(model_path)

        return self.fasttext_lang_id.predict(text.replace("\r\n", " ").replace("\n", " ").strip())[0][0].split('__')[-1]

    def sentence_splitting(self, text: str, lang: str = None):
        if lang == 'th':
            from thai_segmenter import sentence_segment
            return [str(sent) for sent in sentence_segment(text)]
        elif lang in ['ar', 'jp', 'ko', 'zh']:
            return list(re.findall(u'[^!?。\.]+[!?。\.]*', text, flags=re.U))

        try:
            nltk.data.find('tokenizers/punkt')
        except LookupError:
            nltk.download('punkt')

        return nltk.sent_tokenize(text)

    def available_models(self, source_lang: str = None, target_lang: str = None):
        pass