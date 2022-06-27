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

    def __closest_term(self,t,closer = 1):
        result = []
        try:
            found = [t for t,_ in sorted(self.term_correlation[t].items(),key=lambda kv:kv[1],reverse=True)]
            found = pos_tag(found,tagset='universal')
            for t,pos in found:
                if pos in ['NOUN','ADJ']:
                    closer -= 1
                    result.append(t)
                    if closer == 0: break    
            return result
        except KeyError:
            return ''

    
    def expand_query(self,query):
        query = pos_tag(word_tokenize(query),tagset='universal')
        query_exp = ''
        query_exp_syn = ''

        lemma = WordNetLemmatizer()
        
        for t in query:
            if not t[0] in stopwords.words('english') and t[0].isalpha(): 
                posible_t = lemma.lemmatize(t[0].lower())

                if t[1] == "NOUN" or t[1] == "ADJ":
                    try:
                        ss = wordnet.synsets(posible_t)
                        query_exp_syn +=' ' + ss[0].lemmas()[0].name()
                    except IndexError:
                        query_exp_syn +=' ' + posible_t
                
                if posible_t in query_exp :
                    continue

                query_exp += ' ' + posible_t 

                if t[1] == 'NOUN':
                    for close_t in self.__closest_term(posible_t):
                        query_exp += ' ' + close_t  
            else:
                query_exp += ' ' + t[0]

        return [query_exp,query_exp_syn]
    