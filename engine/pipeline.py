import os
import pickle
import uuid
from os import listdir
from os.path import join, isfile
from typing import List, Dict, Tuple

from irm import Vector_Space_Model
from text_processor import Cleaner

TF_DOCS_FILE = "tf_doc_table"
IDF_FILE = "idf_table"
INVERT_LIST_FILE = "invert_list_table"  # no hace falta a menos que cambie la coleccion
DOCS_W = "docs_weights"
NORM_DOCS = "norm_docs"
DOCS_IDS = "docs_ids"


class Pipeline:
    def __init__(self, corpus_path) -> None:
        self.corpus_path = corpus_path

    def start(self):
        self.cl = Cleaner(self.corpus_path)
        self.files = self.__scan_corpus(self.corpus_path)
        corpus_size = len(self.files)
        self.vsm = Vector_Space_Model(corpus_size)
        self.vsm.docs_id = {uuid.uuid4(): f for f in self.files}
        self.__start_search_engine_indexing()

    def __scan_corpus(self, path):
        directories = listdir(path)
        files_found = []
        for e in directories:
            file_path = join(path, e)
            if not isfile(file_path):
                files_found += self.__scan_corpus(file_path)
            else:
                files_found.append(file_path)
        return files_found

    def __start_search_engine_indexing(self):
        try:
            self.vsm.doc_tf = self.__retrieve_from_disk(TF_DOCS_FILE)
            self.vsm.idf = self.__retrieve_from_disk(IDF_FILE)
            self.vsm.doc_wights = self.__retrieve_from_disk(DOCS_W)
            self.vsm.doc_norm = self.__retrieve_from_disk(NORM_DOCS)
            self.vsm.docs_id = self.__retrieve_from_disk(DOCS_IDS)
        except:
            for dj, file in self.vsm.docs_id.items():
                plain_text = self.cl.get_text(file)
                tokens = self.cl.doc_to_tokens(plain_text)
                self.vsm.calc_tf(tokens, dj)

            self.vsm.calc_idf()
            self.vsm.calc_weights()

            self.__save_to_disk(TF_DOCS_FILE, self.vsm.doc_tf)
            self.__save_to_disk(IDF_FILE, self.vsm.idf)
            self.__save_to_disk(DOCS_W, self.vsm.doc_wights)
            self.__save_to_disk(NORM_DOCS, self.vsm.doc_norm)
            self.__save_to_disk(DOCS_IDS, self.vsm.docs_id)

    def process_query(self, query, alpha=0.5):
        q = self.cl.doc_to_tokens(query)
        q_tf = self.vsm.calc_query_tf(q)
        return self.vsm.calc_query_weights(alpha, q_tf)

    def retrieve_id_docs(self, q_weights, threshold=10):
        return self.vsm.retrieve_ids(threshold, q_weights)

    def get_subjects(self, path_and_ids):
        return self.cl.get_subjects(path_and_ids)

    @staticmethod
    def make_response(file_paths_id, subjects):
        body = []

        for i in range(len(file_paths_id)):
            body.append({
                "subject": subjects[i],
                "id": file_paths_id[i][0]
            })

        return body

    @staticmethod
    def __save_to_disk(file_name, struct):
        try:
            with open(f'tables/{file_name}', 'wb') as f:
                pickle.dump(struct, f)
                f.close()
        except:
            print("Something went wrong saving to disk")

    @staticmethod
    def __retrieve_from_disk(file_name):
        with open(os.path.join(os.getcwd(), f'tables/{file_name}'), 'rb') as tf_docs_file:
            return pickle.load(tf_docs_file)

    def retrieve_doc(self, id):
        return self.cl.get_text(self.vsm.docs_id[id])

    def boolean_model_retrieve_docs(self, query: str) -> List[object]:
        """
        :param query:
        :return: List UUID => ids docs retrieves
        """

        tf: Dict[Tuple[str, object], float] = self.vsm.doc_tf
        keys: list[Tuple[str, object]] = tf.keys()  # termino, id_doc

        query_tokens: List[str] = list(set(self.cl.doc_to_tokens(query)))

        ans = []

        for t in query_tokens:
            temp = [id_doc for (ter, id_doc) in keys if ter == t]

            if len(ans) == 0:
                ans = temp.copy()

            ans = list(set(temp) & set(ans))

            if ans is None or len(ans) == 0:
                break

        return [(id_doc, self.vsm.docs_id[id_doc]) for id_doc in ans]
