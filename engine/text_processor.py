import string

from nltk import *
from nltk.corpus import stopwords


class Cleaner:
    def __init__(self, path) -> None:## Esto no hace falta
        self.corpus_path = path

    def get_text(self, path_file):
        with open(path_file, encoding='utf8', errors='ignore') as file:
            plain_text = file.read()
            file.close()
            return plain_text

    def __remove_reg(self, tokens):
        re_punc = re.compile('[%s]' % re.escape(string.punctuation))
        stripped = [re_punc.sub('', w) for w in tokens]
        return stripped

    def doc_to_tokens(self, plain_text):
        plain_text = re.sub('from:(.*\n)', '', plain_text)
        plain_text = re.sub('[\w]+[\._]?[\w]+[@]+[\w.]+', '', plain_text)
        plain_text = re.sub('Subject:|subject:', '', plain_text)

        tokens = word_tokenize(plain_text)
        tokens = [t.lower() for t in tokens]
        # remove regular expr. 
        tokens = self.__remove_reg(tokens)
        # filters all non words
        tokens = [word for word in tokens if word.isalpha()]
        # filters all stepwords
        stop_words = set(stopwords.words('english'))
        tokens = [t for t in tokens if not t in stop_words]
        # word to root word
        porter = PorterStemmer()
        tokens = [porter.stem(word) for word in tokens]
        return tokens

    def get_subjects(self, file_paths):
        subj = []
        for _, fp in file_paths:
            file = self.get_text(fp)
            subject = re.findall('Subject:[^\n]*', file)
            if subject:
                subject = subject[0].replace('Subject:', '')
                subject = subject.replace('Re:', '')
                subject = subject.strip()
            else:
                subject = fp

            subj.append(subject)
        return subj
