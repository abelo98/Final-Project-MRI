import numpy as np
import math
import os
from scaner import Scaner

class Vector_Space_Model:
    def __init__(self,corpus_size, path) -> None:
        self.query_tf = {}
        self.doc_tf = {}

        self.idf = {}
        self.invert_index = {}
        self.doc_wights = {}
        self.query_wights = {}
        self.sim = {}
        self.corpus_size = corpus_size
        self.corpus_path = path
        self. sc = Scaner()

    def calc_tf(self):
        files = os.listdir(self.corpus_path)
        for dj,file in enumerate(files):
            path_file = os.path.join(self.corpus_path, file)
            if os.path.isfile(path_file):
                plain_text = self.sc.get_text(path_file)
                tokens = self.sc.doc_to_tokens(plain_text)
                
                for t in tokens:
                    try:
                        self.invert_index[t]
                    except KeyError:
                        self.invert_index[t] = 1 + self.invert_index[t] if dj else 1

                    try:
                        self.doc_tf[t,dj] += 1
                    except KeyError:
                        self.doc_tf[t,dj] = 1

                max_freq_tok = max(self.doc_tf.values())
                self.doc_tf = {key:self.doc_tf[key,dj]/max_freq_tok for key,_ in self.doc_tf}

    def calc_idf(self):
        for t in self.invert_index:
            self.idf[t] = math.log10(self.corpus_size/self.invert_index)
        
    def calc_weights(self):
        for t in self.invert_index:
            for d in range(self.corpus_size):
                self.doc_wights[t,d] = self.doc_tf[t,d] * self.idf[t]

    def calc_query_tf(self,query):
        for t in query:
            try:
                self.query_tf[t] += 1
            except KeyError:
                self.query_tf[t] = 1

        max_freq_tok = max(self.query_tf.values())
        self.query_tf = {key:self.query_tf[key]/max_freq_tok for key,_ in self.query_tf}


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
                vect_prod += self.doc_wights[t,dj] * self.query_wights[t]

            norm_d = np.linalg.norm(list(self.doc_wights.values()))
            norm_q = np.linalg.norm(list(self.query_wights.values()))

            self.sim[dj] = vect_prod/(norm_d * norm_q)

        return sorted(self.sim.items(),key=lambda kv:kv[1],reverse=True)[0:threshold]
            

