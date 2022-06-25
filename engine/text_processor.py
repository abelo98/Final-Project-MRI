import string

from nltk import *
from nltk.corpus import stopwords,wordnet


class Cleaner:
    def __init__(self) -> None:## Esto no hace falta
        pass

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
        lemmatizer = WordNetLemmatizer()
        tokens = [lemmatizer.lemmatize(word) for word in tokens]
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


c = Cleaner()
exp = c.doc_to_tokens('''dynamic stability of vehicles traversing ascending
or descending paths through the atmosphere .
  an analysis is given of the oscillatory motions of vehicles which
traverse ascending and descending paths through the atmosphere at high
speed .  the specific case of a skip path is examined in detail, and
this leads to a form of solution for the oscillatory motion which should
recur over any trajectory .  the distinguishing feature of this form is
the appearance of the bessel rather than the trigonometric function as
the characteristic mode of oscillation .''')

q = c.doc_to_tokens('''does there exist a good basic treatment of the dynamics of re-entry
combining consideration of realistic effects with relative simplicity of
results .''')

given = c.doc_to_tokens('''aerodynamic characteristics of two winged reentry vehicles at supersonic
 and hypersonic speeds .
tests were conducted at the langley research center on two winged
lifting hypersonic reentry glider configurations . performance, stability,
and control data are presented at mach numbers of 1.62 and 2.91 for
angles of attack up to 15degree and at mach numbers of 6.8 and 9.6 for
angles of attack up to 25degree  .''')


equal_toks1 = set(q).intersection(set(exp))
equal_toks2 = set(q).intersection(set(given))


print(equal_toks1)
print(equal_toks2)
