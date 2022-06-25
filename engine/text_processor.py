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


# c = Cleaner('lsl')
# tokens2 = c.doc_to_tokens('''theory of aircraft structural models subjected to aerodynamic
# heating and external loads .
#   the problem of investigating the simultaneous effects of transient
# aerodynamic heating and external loads on aircraft structures for the
# purpose of determining the ability of the structure to withstand flight
# to supersonic speeds is studied .  by dimensional analyses it is shown
# that ..
# constructed of the same materials as the aircraft will be thermally
# similar to the aircraft with respect to
# the flow of heat through the structure
# will be similar to those of the aircraft when the structural model is
# constructed at the same temperature as the aircraft .
# external loads will be similar to those of the aircraft .
# subjected to heating and cooling that correctly simulate the aerodynamic
# heating of the aircraft, except with respect to angular velocities and
# angular accelerations, without requiring determination of the heat flux
# at each point on the surface and its variation with time .
# acting on the aerodynamically heated structural model to those acting
# on the aircraft is determined for the case of zero angular velocity and
# zero angular acceleration, so that the structural model may be subjected
# to the external loads required for simultaneous simulation of stresses
# and deformations due to external loads .''')

# tokens1 = c.doc_to_tokens('''what similarity laws must be obeyed when constructing aeroelastic models
# of heated high speed aircraft .''')

# tokens3 = c.doc_to_tokens('''scale models for thermo-aeroelastic research .
#   an investigation is made of the
# parameters to be satisfied for
# thermo-aeroelastic similarity .  it is concluded
# that complete similarity obtains
# only when aircraft and model are identical
# in all respects, including size .
#   by limiting consideration to
# conduction effects, by assuming the major
# load carrying parts of the structure
# are in regions where the flow is either
# entirely laminar, or entirely turbulent,
# and by assuming a specific
# relationship between reynolds number and nusselt
# number, an approach to similarity can
# be achieved for small scale models .
# experimental and analytical work is
# required to check on the validity of these assumptions .
#   it appears that existing hot wind
# tunnels will not be completely
# adequate for thermo-aeroelastic work, and
# accordingly a possible layout for
# the type of tunnel required is described .
# automatic programmed control of
# the tunnel would appear to be necessary .''')


# equal_toks1 = set(tokens1).intersection(set(tokens2))
# equal_toks2 = set(tokens1).intersection(set(tokens3))


# print(equal_toks1)
# print(equal_toks2)
