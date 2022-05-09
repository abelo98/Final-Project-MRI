import re
import string
from nltk.tokenize import word_tokenize
from nltk.stem.porter import PorterStemmer
from nltk import *
from nltk.corpus import stopwords


class Scaner:
    def __init__(self) -> None:
        pass

    def get_text(self,path_file):
        with open(path_file,'r') as file:
            plain_text = file.read()
            file.close()
            return plain_text

    def __remove_reg__(self,tokens):
        re_punc = re.compile('[%s]' % re.escape(string.punctuation))
        stripped = [re_punc.sub('', w) for w in tokens]
        return stripped

    def doc_to_tokens(self,plain_text):
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
