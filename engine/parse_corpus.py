def get_and_split_corpus(dir):
    with open(dir) as f:
        articles = f.read().split('\n.I')
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



a = get_and_split_corpus("/media/abelo/TERA/School/5to/SRI/corpus pal trabajo/med/MED.ALL")
print(a[1])