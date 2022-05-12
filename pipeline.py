from os import listdir
from os.path import join,isfile
from irm import Vector_Space_Model
from scaner import Scaner
import pickle

TF_DOCS_FILE = "tf_doc_table"
IDF_FILE = "idf_table"
INVERT_LIST_FILE = "invert_list_table" #no hace falta a menos que cambie la coleccion
DOCS_W = "docs_weights"



class Pipeline:
    def __init__(self,corpus_path) -> None:
        self.corpus_path = corpus_path
    
    def start(self):
        self.sc = Scaner(self.corpus_path)
        self.files = self.__scan_corpus(self.corpus_path)
        corpus_size = len(self.files)
        self.vsm = Vector_Space_Model(corpus_size)
        self.vsm.number_to_doc = dict(zip(range(corpus_size),self.files))
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
        try:
            self.vsm.doc_tf = self.__retrive_from_disk(TF_DOCS_FILE)
            self.vsm.idf = self.__retrive_from_disk(IDF_FILE)
            self.vsm.doc_wights = self.__retrive_from_disk(DOCS_W)
        except:
            for dj,file in enumerate(self.files):
                plain_text = self.sc.get_text(file)
                tokens = self.sc.doc_to_tokens(plain_text)
                self.vsm.calc_tf(tokens,dj,file)

            self.vsm.calc_idf()
            self.vsm.calc_weights()

            self.__save_to_disk(TF_DOCS_FILE,self.vsm.doc_tf)
            self.__save_to_disk(IDF_FILE,self.vsm.idf)
            self.__save_to_disk(DOCS_W,self.vsm.doc_wights) 


    def process_query(self,query,alpha = 0.5):
        q = self.sc.doc_to_tokens(query)
        self.vsm.calc_query_tf(q)
        self.vsm.calc_query_weights(alpha)

    def retrive_docs(self, threshold = 10):
        return self.vsm.retrive_docs(threshold)

    def __save_to_disk(self,file_name,struct):
        try:
            saved_struct = open(file_name, 'wb')
            pickle.dump(struct, saved_struct)
            saved_struct.close()
  
        except:
            print("Something went wrong saving to disk")

    def __retrive_from_disk(self,file_name):
        tf_docs_file = open(file_name,'rb')
        return pickle.load(tf_docs_file)
        