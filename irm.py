import math
import re
import string
from nltk.tokenize import word_tokenize
from nltk.stem.porter import PorterStemmer
from nltk import *
from nltk.corpus import stopwords

class Vector_Space_Model:
    def __init__(self,corpus_size) -> None:
        self.tf = {}
        self.idf = {}
        self.invert_index = {}
        self.wights = {}
        self.corpus_size = corpus_size


    def __remove_reg__(self,tokens):
        re_punc = re.compile('[%s]' % re.escape(string.punctuation))
        stripped = [re_punc.sub('', w) for w in tokens]
        return stripped

    def doc_to_tokens(self,path_doc):
        with open(path_doc,'r') as doc:
            plain_text = doc.read()

        tokens = word_tokenize(plain_text)
        tokens = [t.lower() for t in tokens]
        # remove regular expr. 
        tokens = self.__remove_reg__(tokens)
        # filters all non words
        tokens = [word for word in tokens if word.isalpha()]
        # filters all stepwords
        stop_words = set(stopwords.words('english'))
        tokens = [t for t in tokens if not t in stop_words]
        # word to root word
        # porter = PorterStemmer()
        # tokens = [porter.stem(word) for word in tokens]

        return tokens

    def calc_tf(self,tokens,dj):
        for t in tokens:
            try:
                self.invert_index[t]
            except KeyError:
                self.invert_index[t]+=1
            try:
                self.tf[t,dj] += 1
            except KeyError:
                self.tf[t,dj] = 1
        max_freq_tok = max(self.tf.values())
        self.tf = {key:self.tf[key,dj]/max_freq_tok for key,_ in self.tf}

    def calc_idf(self):
        for t in self.invert_index:
            self.idf[t] = math.log10(self.corpus_size/self.invert_index)
        
    def calc_weights(self):
        for t in self.invert_index:
            for d in range(self.corpus_size):
                self.wights[t,d] = self.tf[t,d] * self.idf[t]