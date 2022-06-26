from typing import List, Dict

import numpy as np

from feedback import Feedback
from query_sim import query_processor


class VectorialModel:
    def __init__(self, corpus_size, doc_tf, idf, invert_index, doc_weights, doc_norm, docs_id, cl, feedback: Feedback):
        self.doc_tf = doc_tf
        self.idf = idf
        self.invert_index = invert_index
        self.doc_weights = doc_weights
        self.doc_norm = doc_norm
        self.docs_id = docs_id
        self.cl = cl
        self.feedback: Feedback = feedback

        self.tokens_query: List[str] = []

        self.corpus_size = corpus_size

    @staticmethod
    def calc_query_tf(query):
        query_tf = {}
        for t in query:
            try:
                query_tf[t] += 1
            except KeyError:
                query_tf[t] = 1

        max_freq_tok = max(query_tf.values())
        query_tf = {key: query_tf[key] / max_freq_tok for key in query_tf}
        return query_tf

    def calc_query_weights(self, alpha, query_tf):
        query_wights = {}
        for t in query_tf:
            try:
                idf = self.idf[t]
            except KeyError:
                continue

            query_wights[t] = (alpha + (1 - alpha) * query_tf[t]) * idf

        return self.get_feedback(query_wights, self.tokens_query)

    def similarity(self, threshold, query_wights):
        sim = {}
        for dj in self.docs_id:
            vect_prod = 0
            for t in query_wights:
                try:
                    vect_prod += self.doc_weights[t, dj] * query_wights[t]
                except KeyError:
                    pass
            norm_d = self.doc_norm[dj]
            norm_q = np.linalg.norm(list(query_wights.values()))
            norm_p = norm_d * norm_q
            if norm_p and vect_prod:
                sim[dj] = vect_prod / norm_p

        return sorted(sim.items(), key=lambda kv: kv[1], reverse=True)[:threshold]

    def retrieve_ids(self, threshold, q_weights):
        return [(dj, self.docs_id[dj]) for dj, _ in self.similarity(threshold, q_weights)]

    def get_similar(self, query_process: query_processor) -> List[str]:
        if self.tokens_query is None or len(self.tokens_query) == 0:
            return []

        return query_process.similar(self.tokens_query, k=3)

    def set_similar(self, query_process: query_processor, query: str, vector_q):
        if self.tokens_query is None or len(self.tokens_query) == 0:
            return

        query_process.save_query(q=query, vector_q=vector_q)

    def process_query(self, query, alpha=0.5, query_process: query_processor = None):
        q = self.cl.doc_to_tokens(query)

        self.tokens_query = q

        q_tf = self.calc_query_tf(q)
        ans = self.calc_query_weights(alpha, q_tf)

        if query_process is not None:
            self.set_similar(query_process, query, ans)

        return ans

    def retrieve_id_docs(self, q_weights, threshold=15):
        return self.retrieve_ids(threshold, q_weights)

    def set_feedback(self, _type, doc_id, query: List[str] = None):
        if query is None:
            query = self.tokens_query

        self.feedback.set_feedback(_type, doc_id, query)

    def get_feedback(self, query_weight: Dict, query: List[str]):
        feed = self.feedback.get_feedback(query)

        if feed is None:
            return query_weight

        id_docs_relevant, id_docs_no_relevant = feed

        for dj in id_docs_no_relevant:
            for t in query_weight:
                try:
                    query_weight[t] -= self.doc_weights[t, dj] * (.5 / len(id_docs_no_relevant))
                except KeyError:
                    pass

        for dj in id_docs_relevant:
            for t in query_weight:
                try:
                    query_weight[t] += self.doc_weights[t, dj] * (1 / len(id_docs_relevant))
                except KeyError:
                    pass

        return query_weight
