from lib2to3.pgen2 import token
import numpy as np
import math
# import scaner

class Vector_Space_Model:
    def __init__(self,corpus_size) -> None:
        self.query_tf = {}
        self.doc_tf = {}

        self.idf = {}
        self.invert_index = {}
        self.doc_wights = {}
        self.query_wights = {}
        self.sim = {}
        self.number_to_doc = {}

        self.corpus_size = corpus_size
        # self.files = files
        # self. sc = sc

    def calc_tf(self, tokens, dj, file):
        aux = {}
        self.number_to_doc[dj] = file
        for t in tokens:
            try:
                aux[t,dj] += 1
            except KeyError:
                aux[t,dj] = 1
                try:
                    self.invert_index[t] += 1 
                except KeyError:
                    self.invert_index[t] = 1 

        max_freq_tok = max(aux.values())
        aux = {(key,dj):aux[key,dj]/max_freq_tok for key,_ in aux}
        self.doc_tf.update(aux)

    def calc_idf(self):
        for t in self.invert_index:
            self.idf[t] = math.log10(self.corpus_size/self.invert_index[t])
        
    def calc_weights(self):
        for t in self.invert_index:
            for d in range(self.corpus_size):
                try:
                    self.doc_wights[t,d] = self.doc_tf[t,d] * self.idf[t]
                except KeyError:
                    pass
                    

    def calc_query_tf(self,query):
        for t in query:
            try:
                self.query_tf[t] += 1
            except KeyError:
                self.query_tf[t] = 1

        max_freq_tok = max(self.query_tf.values())
        self.query_tf = {key:self.query_tf[key]/max_freq_tok for key in self.query_tf}


    def calc_query_weights(self,alpha):
        for t in self.query_tf:
            idf = 0
            try:
                idf = self.idf[t]
            except KeyError: 
                continue
            
            self.query_wights[t] = (alpha + (1-alpha) * self.query_tf[t]) * idf

    def similarity(self,threshold):
        for dj in range(self.corpus_size):
            vect_prod = 0
            for t in self.query_wights:
                try:
                    vect_prod += self.doc_wights[t,dj] * self.query_wights[t]
                except KeyError:
                    pass

            norm_d = np.linalg.norm(list(self.doc_wights.values()))
            norm_q = np.linalg.norm(list(self.query_wights.values()))

            self.sim[dj] = vect_prod/(norm_d * norm_q)

        return sorted(self.sim.items(),key=lambda kv:kv[1],reverse=True)[:threshold]
            
    def retrive_docs(self,threshold):
        return [self.number_to_doc[dj] for dj,_ in self.similarity(threshold)]

