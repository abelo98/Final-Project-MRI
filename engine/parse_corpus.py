import os
import sys

def get_and_split_corpus(dir,corpus_type = 'cran'):
    with open(dir) as f:
        articles = f.read().split('\n.I')
        parser = None
        if corpus_type == 'cran':
            data = {(i+1):process_cran(article) for i,article in enumerate(articles)}
        else:
            data = {(i+1):process_med(article) for i,article in enumerate(articles)}
        
        f.close()
    return data


def process_cran(article):
    article = article.split('\n.T\n')[1]
    T, _, article = article.partition('\n.A\n')
    A, _, article = article.partition('\n.B\n')
    B, _, W = article.partition('\n.W\n')
    return {'T':T, 'A':A, 'B':B, 'W':W}

def process_med(article):
    B, _, W = article.partition('\n.W\n')
    return {'W':W}


def save_corpus(docs,directory):
    try:
        for i,doc in enumerate(docs.values()):
            filename = f'{directory}/{i+1}'
            os.makedirs(os.path.dirname(filename), exist_ok=True)
            with open(filename, "w") as f:
                if len(doc) == 1:
                    f.write(doc['W'])
                else:
                    txt = 'Subject: ' + doc['T'] + '\n' + doc['W']
                    f.write(txt)
                f.close()
    except:
        print("Something went wrong saving to disk")


def main(path,corpus_path,corpus_type):
    docs = get_and_split_corpus(path,corpus_type)
    save_corpus(docs,corpus_path)
   

if __name__ == "__main__":
    main(sys.argv[1],sys.argv[2],sys.argv[3])
