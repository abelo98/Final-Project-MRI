from nltk import *
from nltk.corpus import stopwords

class term_processor:
    def __init__(self) -> None:
        self.term_correlation = {}
    
    def get_corr_in_text(self,text:str):
        for i,w1 in enumerate(text):
            try:
                w2 = text[i+1]
                try:
                    self.term_correlation[w1]
                    try:
                        self.term_correlation[w1][w2] += 1
                    except KeyError:
                        self.term_correlation[w1][w2] = 1
                except KeyError:
                    self.term_correlation[w1] = {w2:1}
            except IndexError:
                break

    def __closest_term(self,t):
        s = sorted(self.term_correlation[t].items(),key=lambda kv:kv[1],reverse=True)[:2]
        for term in s:
            yield term[0]

    def expand_query(self,query):
        query = word_tokenize(query)
        query_exp = ''
        stemmer = PorterStemmer()
        for t in query:
            
            if not t in stopwords.words('english') and t.isalpha(): 
                t = stemmer.stem(t.lower())
                
                if t in query_exp:continue
                query_exp += ' ' + t 

                for close_t in self.__closest_term(t):
                    query_exp += ' ' + close_t
                
            else:
                query_exp += ' ' + t

        return query_exp
    