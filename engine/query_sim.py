import numpy as np


class query_processor:
    def __init__(self) -> None:
        self.query_historial = {}

    def save_query(self, q, vector_q: dict):
        if not q in self.query_historial.keys():
            self.query_historial[q] = (vector_q, np.linalg.norm(list(vector_q.values())))

    # q is a tuple formed by q[0] = dict (reresenting the vector of the query) 
    # and q[1] is the norm of the vect
    def similar(self, q_original, vector_q, k=4):
        sim = np.zeros(k)
        queries_result = [None] * k

        for query_str, vector_q_saved_and_norm in self.query_historial.items():
            vect_prod = 0
            term_coincidences = 0
            if q_original == query_str: continue
            for t in vector_q:
                try:
                    vect_prod += vector_q_saved_and_norm[0][t] * vector_q[t]
                    term_coincidences += 1
                except KeyError:
                    pass

            if len(vector_q) > 0 and (term_coincidences * 100) / len(vector_q) >= 30:
                norm_q1 = vector_q_saved_and_norm[1]
                norm_q2 = np.linalg.norm(list(vector_q.values()))
                norm_p = norm_q1 * norm_q2
                if norm_p and vect_prod:
                    s = vect_prod / norm_p
                    if s > sim.min():
                        index = sim.argmin()
                        sim[index] = s
                        queries_result[index] = query_str

        return queries_result
