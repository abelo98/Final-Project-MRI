from pipeline import Pipeline

MY_CORPUS = '/media/abelo/TERA/School/5to/SRI/Proyecto Final SRI/corpus'
REAL_CORPUS = '/media/abelo/TERA/School/5to/SRI/PF SRI/Test Collections/20 Newsgroups/20news-18828'

def main():
    pipeline = Pipeline(REAL_CORPUS)
    pipeline.start()
    pipeline.process_query("Cuba")
    print(pipeline.retrive_docs())

   

if __name__ == '__main__':
    main()

