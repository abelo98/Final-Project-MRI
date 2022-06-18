import math

import numpy as np


class Vector_Space_Model:
    def __init__(self, corpus_size) -> None:
        self.doc_tf = {}
        self.idf = {}
        self.invert_index = {}
        self.doc_wights = {}
        self.doc_norm = {}
        self.docs_id = {}

        self.corpus_size = corpus_size

    def calc_tf(self, tokens, dj):
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

    def calc_idf(self):
        for t in self.invert_index:
            self.idf[t] = math.log10(self.corpus_size / self.invert_index[t])

    def calc_weights(self):
        for t in self.invert_index:
            for d in self.docs_id:
                try:
                    self.doc_wights[t, d] = self.doc_tf[t, d] * self.idf[t]
                except KeyError:
                    pass
        for dj in self.docs_id:
            self.doc_norm[dj] = np.linalg.norm([self.doc_wights[k] for k in self.doc_wights if k[1] == dj])

    def calc_query_tf(self, query):
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
            idf = 0
            try:
                idf = self.idf[t]
            except KeyError:
                continue

            query_wights[t] = (alpha + (1 - alpha) * query_tf[t]) * idf

        return query_wights

    def similarity(self, threshold, query_wights):
        sim = {}
        for dj in self.docs_id:
            vect_prod = 0
            for t in query_wights:
                try:
                    vect_prod += self.doc_wights[t, dj] * query_wights[t]
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
