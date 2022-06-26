import math
import pickle
from os import listdir
from os.path import join, isfile
from typing import List, Dict, Any

import numpy as np

from boolean_model import BooleanModel
from constants import *
from correlation import term_processor
from feedback import Feedback
from query_sim import query_processor
from text_processor import Cleaner
from vectorial_model import VectorialModel


class Core:
    def __init__(self, corpus_path, corpus_name="cran") -> None:
        self.corpus_path = corpus_path
        self.corpus_name = corpus_name
        self.files: List[str] = []

        self.feedback: Feedback = Feedback()
        self.query_processor = query_processor()

        self.cl: Cleaner = None
        self.vsm: VectorialModel = None
        self.boolean_model: BooleanModel = None
        self.query_exp = term_processor()

        self.doc_tf = {}
        self.idf = {}
        self.invert_index = {}
        self.doc_wights = {}
        self.doc_norm = {}
        self.docs_id = {}

        self.start()

        self.corpus_size = len(self.files)

        self.start_search_engine_indexing()

    def refactor(self, corpus_path, corpus_name):
        self.corpus_path = corpus_path
        self.corpus_name = corpus_name
        self.files: List[str] = []

        self.feedback: Feedback = Feedback()

        self.cl: Cleaner = None
        self.vsm: VectorialModel = None
        self.boolean_model: BooleanModel = None

        self.query_exp = term_processor()
        self.query_processor = query_processor()

        self.doc_tf = {}
        self.idf = {}
        self.invert_index = {}
        self.doc_wights = {}
        self.doc_norm = {}
        self.docs_id = {}

        self.start()

        self.corpus_size = len(self.files)

        self.start_search_engine_indexing()

    def start(self):
        if self.cl is None:
            self.cl = Cleaner()

        self.files = self.__scan_corpus(self.corpus_path)
        self.docs_id = {i + 1: f for i, f in enumerate(self.files)}

    def start_search_engine_indexing(self):
        try:
            self.doc_tf = self.retrieve_from_disk(TF_DOCS_FILE)
            self.idf = self.retrieve_from_disk(IDF_FILE)
            self.doc_wights = self.retrieve_from_disk(DOCS_W)
            self.doc_norm = self.retrieve_from_disk(NORM_DOCS)
            self.docs_id = self.retrieve_from_disk(DOCS_IDS)
            self.query_exp.term_correlation = self.retrieve_from_disk(CORR)
        except:
            for dj, file in self.docs_id.items():
                plain_text = self.cl.get_text(file)
                tokens = self.cl.doc_to_tokens(plain_text, use_lematizer=True)
                self.query_exp.get_corr_in_text(tokens)
                self.__calc_tf(tokens, dj)

            self.__calc_idf()
            self.__calc_weights()

            self.save_to_disk(CORR, self.query_exp.term_correlation)
            self.save_to_disk(TF_DOCS_FILE, self.doc_tf)
            self.save_to_disk(IDF_FILE, self.idf)
            self.save_to_disk(DOCS_W, self.doc_wights)
            self.save_to_disk(NORM_DOCS, self.doc_norm)
            self.save_to_disk(DOCS_IDS, self.docs_id)

    def set_feedback(self, _type, doc_id, query):
        self.vsm.set_feedback(_type, doc_id, query)

    def update_corpus_path(self, new_path: str):
        self.corpus_path = new_path

    def __calc_tf(self, tokens, dj):
        aux = {}
        for t in tokens:
            try:
                aux[t, dj] += 1
            except KeyError:
                aux[t, dj] = 1
                try:
                    self.invert_index[t] += 1
                except KeyError:
                    self.invert_index[t] = 1

        max_freq_tok = max(aux.values())
        aux = {(key, dj): aux[key, dj] / max_freq_tok for key, _ in aux}
        self.doc_tf.update(aux)

    def __calc_idf(self):
        for t in self.invert_index:
            self.idf[t] = math.log10(self.corpus_size / self.invert_index[t])

    def __calc_weights(self):
        for t in self.invert_index:
            for d in self.docs_id:
                try:
                    self.doc_wights[t, d] = self.doc_tf[t, d] * self.idf[t]
                except KeyError:
                    pass
        for dj in self.docs_id:
            self.doc_norm[dj] = np.linalg.norm([self.doc_wights[k] for k in self.doc_wights if k[1] == dj])

    # def __calc_weights_norm(self):
    #     for t in self.invert_index:
    #         for d in self.docs_id:
    #             try:
    #                 self.doc_wights[t, d] = self.doc_tf[t, d] * self.idf[t]
    #                 for _ in 
    #             except KeyError:
    #                 pass
    #     for dj in self.docs_id:
    #         self.doc_norm[dj] = np.linalg.norm([self.doc_wights[k] for k in self.doc_wights if k[1] == dj])

    def load_vectorial_model(self, corpus_name=None):

        if corpus_name is not None and self.corpus_name != corpus_name:
            self.refactor(Core.map_corpus_to_constants(corpus_name), corpus_name)

        self.vsm = VectorialModel(
            doc_tf=self.doc_tf,
            doc_norm=self.doc_norm,
            corpus_size=self.corpus_size,
            doc_weights=self.doc_wights,
            invert_index=self.invert_index,
            docs_id=self.docs_id,
            idf=self.idf,
            cl=self.cl,
            feedback=self.feedback)

    def load_boolean_model(self, corpus_name=None):

        if corpus_name is not None and self.corpus_name != corpus_name:
            self.refactor(Core.map_corpus_to_constants(corpus_name), corpus_name)

        self.boolean_model = BooleanModel(
            doc_tf=self.doc_tf,
            cl=self.cl,
            docs_ids=self.docs_id)

    def __scan_corpus(self, path) -> List[str]:
        if self.corpus_name == '20newsgroup':
            directories = listdir(path)
        else:
            directories = sorted(listdir(path), key=lambda e: int(e))
        files_found = []
        for e in directories:
            file_path = join(path, e)
            if not isfile(file_path):
                files_found += self.__scan_corpus(file_path)
            else:
                files_found.append(file_path)
        return files_found

    def get_subjects(self, path_and_ids):
        return self.cl.get_subjects(path_and_ids)

    @staticmethod
    def make_response(file_paths_id, subjects) -> List[Dict[str, Any]]:
        body = []

        for i in range(len(file_paths_id)):
            body.append({
                "subject": subjects[i],
                "id": file_paths_id[i][0]
            })

        return body

    def save_to_disk(self, file_name, struct):
        try:
            file_name = f'tables/{self.corpus_name}/' + file_name
            os.makedirs(os.path.dirname(file_name), exist_ok=True)
            with open(file_name, 'wb') as f:
                pickle.dump(struct, f)
                f.close()
        except:
            print("Something went wrong saving to disk")

    def retrieve_from_disk(self, file_name):
        with open(os.path.join(os.getcwd(), f'tables/{self.corpus_name}/{file_name}'), 'rb') as tf_docs_file:
            return pickle.load(tf_docs_file)

    def retrieve_doc(self, doc_id):
        return self.cl.get_text(self.docs_id[int(doc_id)])

    def recoverd_docs(self, retrived_docs: dict, relevant_docs: list):
        rr = 0
        nr = 0
        for dicc in retrived_docs:
            if dicc['id'] in relevant_docs:
                rr += 1
            else:
                nr += 1
        return rr, nr

    def get_similar(self) -> List[str]:
        if self.vsm is None:
            return []

        return self.vsm.get_similar(self.query_processor)

    def precision(self, retrived_docs: dict, relevant_docs: list):
        rr, nr = self.recoverd_docs(retrived_docs, relevant_docs)
        return (rr / (rr + nr)) * 100

    def recall(self, retrived_docs: dict, relevant_docs: list):
        rr, _ = self.recoverd_docs(retrived_docs, relevant_docs)
        rn = abs(len(relevant_docs) - rr)
        return (rr / (rr + rn)) * 100

    def f1(self, retrived_docs: dict, relevant_docs: list):
        p = self.precision(retrived_docs, relevant_docs)
        r = self.recall(retrived_docs, relevant_docs)
        if p != 0 or r != 0:
            return (2 * p * r / (p + r))
        else:
            return 0

    # def map(self,retrived_docs:dict,relevant_docs:list):
    #     for 

    @staticmethod
    def process_corpus_name(name: str) -> str:
        return name.split()[0].lower()

    @staticmethod
    def map_corpus_to_constants(name: str) -> str:
        if name == '20newsgroup':
            return NEWS_GROUPS_CORPUS
        elif name == 'med':
            return MED_CORPUS
        else:
            return CRAN_CORPUS
