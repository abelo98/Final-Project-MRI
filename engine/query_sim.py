import numpy as np


class query_processor:
    def __init__(self) -> None:
        self.query_historial = {}

    def save_query(self, q, vector_q: dict):
        self.query_historial[str(q)] = (vector_q, np.linalg.norm(list(vector_q.values())))

    # q is a tuple formed by q[0] = dict (reresenting the vector of the query) 
    # and q[1] is the norm of the vect
    def similar(self, vector_q, k=4):
        sim = np.zeros(k)
        queries_result = [None] * k
        vect_prod = 0

        for query_str, vector_q_saved_and_norm in self.query_historial.items():
            for t in vector_q:
                try:
                    vect_prod += vector_q_saved_and_norm[0][t] * vector_q[t]
                except KeyError:
                    pass
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
