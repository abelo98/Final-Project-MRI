from typing import Tuple, List


class BooleanModel:
    def __init__(self, doc_tf, cl, docs_ids):
        self.doc_tf = doc_tf
        self.cl = cl
        self.docs_ids = docs_ids

    def boolean_model_retrieve_docs(self, query: str) -> List[object]:
        """
        :param query:
        :return: List UUID => ids docs retrieves
        """

        # tf: Dict[Tuple[str, object], float] = self.warehouse.doc_tf
        keys: List[Tuple[str, object]] = self.doc_tf.keys()  # termino, id_doc

        query_tokens: List[str] = list(set(self.cl.doc_to_tokens(query)))

        ans = []

        for t in query_tokens:
            temp = [id_doc for (ter, id_doc) in keys if ter == t]

            if len(ans) == 0:
                ans = temp.copy()

            ans = list(set(temp) & set(ans))

            if ans is None or len(ans) == 0:
                break

        return [(id_doc, self.docs_ids[id_doc]) for id_doc in ans]
