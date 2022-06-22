from typing import List, Tuple, Set


class Node:
    def __init__(self):
        self.terms = {}
        self.relevant_docs = set()
        self.no_relevant_docs = set()


class Feedback:
    def __init__(self):
        self.first: Node = Node()

    def set_feedback(self, _type: int, doc_id, query: List[str]):
        node = self.first

        for t in query:
            if not node.terms.__contains__(t):
                node.terms[t] = Node()

            node = node.terms[t]

        if _type == -1:
            if node.relevant_docs.__contains__(doc_id):
                node.relevant_docs.remove(doc_id)
            node.no_relevant_docs.add(doc_id)
        else:
            if node.no_relevant_docs.__contains__(doc_id):
                node.no_relevant_docs.remove(doc_id)
            node.relevant_docs.add(doc_id)

    def get_feedback(self, query: List[str]) -> Tuple[Set, Set]:
        node = self.first

        for t in query:
            if node.terms.__contains__(t):
                node = node.terms[t]
            else:
                return None

        return node.relevant_docs, node.no_relevant_docs
