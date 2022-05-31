from os import listdir
from os.path import join,isfile
import re
from irm import Vector_Space_Model
from text_processor import Cleaner
import pickle
import uuid

TF_DOCS_FILE = "tf_doc_table"
IDF_FILE = "idf_table"
INVERT_LIST_FILE = "invert_list_table" #no hace falta a menos que cambie la coleccion
DOCS_W = "docs_weights"
NORM_DOCS = "norm_docs"
DOCS_IDS = "docs_ids"


class Pipeline:
    def __init__(self,corpus_path) -> None:
        self.corpus_path = corpus_path
    
    def start(self):
        self.cl = Cleaner(self.corpus_path)
        self.files = self.__scan_corpus(self.corpus_path)
        corpus_size = len(self.files)
        self.vsm = Vector_Space_Model(corpus_size)
        self.vsm.docs_id =  {uuid.uuid4():f for f in self.files}  
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
            # self.vsm.doc_tf = self.__retrive_from_disk(TF_DOCS_FILE)
            self.vsm.idf = self.__retrive_from_disk(IDF_FILE)
            self.vsm.doc_wights = self.__retrive_from_disk(DOCS_W)
            self.vsm.doc_norm = self.__retrive_from_disk(NORM_DOCS)
            self.vsm.docs_id = self.__retrive_from_disk(DOCS_IDS)
        except:
            print(len(self.vsm.docs_id.items()))
            i = 0
            for dj,file in self.vsm.docs_id.items():
                plain_text = self.cl.get_text(file)
                tokens = self.cl.doc_to_tokens(plain_text)
                self.vsm.calc_tf(tokens,dj)
            print("Calc idf")
            self.vsm.calc_idf()
            self.vsm.calc_weights()

            # self.__save_to_disk(TF_DOCS_FILE,self.vsm.doc_tf)
            self.__save_to_disk(IDF_FILE,self.vsm.idf)
            self.__save_to_disk(DOCS_W,self.vsm.doc_wights) 
            self.__save_to_disk(NORM_DOCS,self.vsm.doc_norm)
            self.__save_to_disk(DOCS_IDS,self.vsm.docs_id) 

        
    def process_query(self,query,alpha = 0.5):
        q = self.cl.doc_to_tokens(query)
        self.vsm.calc_query_tf(q)
        self.vsm.calc_query_weights(alpha)
        
    def retrive_id_docs(self, threshold = 10):
        return self.vsm.retrive_ids(threshold)

    def get_subjects(self,path_and_ids):
        return self.cl.get_subjects(path_and_ids)

    def make_response(self,file_paths_id, subjects):
        body = []

        for i in range(len(file_paths_id)):
            body.append({
                "subject": subjects[i],
                "id": file_paths_id[i][0]
            })

        return body

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
        
    def retrive_doc(self,id):
        return self.cl.get_text(self.vsm.docs_id[id])