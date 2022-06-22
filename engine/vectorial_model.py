from typing import List, Dict

import numpy as np

from feedback import Feedback


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

        # TODO: call get_feedback

        return query_wights

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
                sim[dj] = vect_prod / (norm_d * norm_q)

        return sorted(sim.items(), key=lambda kv: kv[1], reverse=True)[:threshold]

    def retrieve_ids(self, threshold, q_weights):
        return [(dj, self.docs_id[dj]) for dj, _ in self.similarity(threshold, q_weights)]

    def process_query(self, query, alpha=0.5):
        q = self.cl.doc_to_tokens(query)

        self.tokens_query = q

        q_tf = self.calc_query_tf(q)
        return self.calc_query_weights(alpha, q_tf)

    def retrieve_id_docs(self, q_weights, threshold=10):
        return self.retrieve_ids(threshold, q_weights)

    def set_feedback(self, _type, doc_id, query: List[str] = None):
        if query is None:
            query = self.tokens_query

        self.feedback.set_feedback(_type, doc_id, query)

    def get_feedback(self, query_weight: Dict, query: List[str]):
        feed = self.feedback.get_feedback(query)

        if feed is None:
            return None

        relevant, no_relevant = feed

        # TODO: apply formule
