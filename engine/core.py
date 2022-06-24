import math
import pickle
from os import listdir
from os.path import join, isfile
from typing import List, Dict, Any

import numpy as np

from boolean_model import BooleanModel
from constants import *
from feedback import Feedback
from text_processor import Cleaner
from vectorial_model import VectorialModel


class Core:
    def __init__(self, corpus_path) -> None:
        self.corpus_path = corpus_path
        self.files: List[str] = []

        self.feedback: Feedback = Feedback()
        self.cl: Cleaner = None
        self.vsm: VectorialModel = None
        self.boolean_model: BooleanModel = None

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
        self.cl = Cleaner(self.corpus_path)
        self.files = self.__scan_corpus(self.corpus_path)
        self.docs_id = {i + 1: f for i, f in enumerate(self.files)}

    def start_search_engine_indexing(self):
        try:
            self.doc_tf = Core.retrieve_from_disk(TF_DOCS_FILE)
            self.idf = Core.retrieve_from_disk(IDF_FILE)
            self.doc_wights = Core.retrieve_from_disk(DOCS_W)
            self.doc_norm = Core.retrieve_from_disk(NORM_DOCS)
            self.docs_id = Core.retrieve_from_disk(DOCS_IDS)
        except:
            for dj, file in self.docs_id.items():
                plain_text = self.cl.get_text(file)
                tokens = self.cl.doc_to_tokens(plain_text)
                self.__calc_tf(tokens, dj)

            self.__calc_idf()
            self.__calc_weights()

            Core.save_to_disk(TF_DOCS_FILE, self.doc_tf)
            Core.save_to_disk(IDF_FILE, self.idf)
            Core.save_to_disk(DOCS_W, self.doc_wights)
            Core.save_to_disk(NORM_DOCS, self.doc_norm)
            Core.save_to_disk(DOCS_IDS, self.docs_id)

    def set_feedback(self, _type, doc_id, query):
        self.vsm.set_feedback(_type, doc_id, query)

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

    def load_vectorial_model(self):
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

    def load_boolean_model(self):
        self.boolean_model = BooleanModel(
            doc_tf=self.doc_tf,
            cl=self.cl,
            docs_ids=self.docs_id)

    def __scan_corpus(self, path) -> List[str]:
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

    @staticmethod
    def save_to_disk(file_name, struct):
        try:
            file_name = f'tables/' + file_name
            os.makedirs(os.path.dirname(file_name), exist_ok=True)
            with open(file_name, 'wb') as f:
                pickle.dump(struct, f)
                f.close()
        except:
            print("Something went wrong saving to disk")

    @staticmethod
    def retrieve_from_disk(file_name):
        with open(os.path.join(os.getcwd(), f'tables/{file_name}'), 'rb') as tf_docs_file:
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

    def precision(self, retrived_docs: dict, relevant_docs: list):
        rr, nr = self.recoverd_docs(retrived_docs, relevant_docs)
        return (rr / (rr + nr)) * 100

    def recall(self, retrived_docs: dict, relevant_docs: set):
        rr, _ = self.recoverd_docs(retrived_docs, relevant_docs)
        rn = abs(len(relevant_docs) - rr)
        return (rr / (rr + rn)) * 100
