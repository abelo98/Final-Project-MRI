from nltk import *
from nltk.corpus import stopwords,wordnet

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
        try:
            s = sorted(self.term_correlation[t].items(),key=lambda kv:kv[1],reverse=True)[:5]
            for element,_ in s:
                yield element
        except KeyError:
            yield ''

    def expand_query(self,query):
        query = pos_tag(word_tokenize(query))
        query_exp = ''
        lemma = WordNetLemmatizer()
        
        for t in query:
            if not t[0] in stopwords.words('english') and t[0].isalpha(): 
                posible_t = lemma.lemmatize(t[0].lower())
                
                if posible_t in query_exp :
                    continue

                query_exp += ' ' + posible_t 

                if t[1] == 'NN':
                    for close_t in self.__closest_term(posible_t):
                        query_exp += ' ' + close_t  
            else:
                query_exp += ' ' + t[0]

        return query_exp
    