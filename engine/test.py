from pipeline import Pipeline
import os

MY_CORPUS = os.path.join(os.getcwd(), 'corpus')
REAL_CORPUS = '/media/abelo/TERA/School/5to/SRI/PF SRI/Test Collections/20 Newsgroups/20news-18828'


def main():
    pipeline = Pipeline(MY_CORPUS)
    pipeline.start()
    pipeline.process_query("subject: Subject reef")
    print(pipeline.retrive_docs())


if __name__ == '__main__':
    main()
