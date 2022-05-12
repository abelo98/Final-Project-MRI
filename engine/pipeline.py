from os import listdir
from os.path import join,isfile
from irm import Vector_Space_Model
from scaner import Scaner

class Pipeline:
    def __init__(self,corpus_path) -> None:
        self.corpus_path = corpus_path
    
    def start(self):
        self.sc = Scaner(self.corpus_path)
        self.files = self.__scan_corpus(self.corpus_path)
        self.vsm = Vector_Space_Model(len(self.files))
        self.__start_search_engine_indexing()

    def __scan_corpus(self,path):
        directories = listdir(path)
        files_found = []
        for e in directories:
            file_path = join(path,e)
            if not isfile(file_path):
                files_found += self.__scan_corpus(file_path)
            else:
                files_found.append(file_path)
        return files_found

    def __start_search_engine_indexing(self):
        for dj,file in enumerate(self.files):
            
            plain_text = self.sc.get_text(file)
            tokens = self.sc.doc_to_tokens(plain_text)
            self.vsm.calc_tf(tokens,dj,file)

        self.vsm.calc_idf()
        self.vsm.calc_weights()

    def process_query(self,query,alpha = 0.5):
        q = self.sc.doc_to_tokens(query)
        self.vsm.calc_query_tf(q)
        self.vsm.calc_query_weights(alpha)

    def retrive_docs(self, threshold = 10):
        return self.vsm.retrive_docs(threshold)