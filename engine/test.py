from pipeline import Pipeline

MY_CORPUS = '/media/abelo/TERA/School/5to/SRI/Proyecto Final SRI/corpus'
REAL_CORPUS = '/media/abelo/TERA/School/5to/SRI/PF SRI/Test Collections/20 Newsgroups/20news-18828'

def main():
    pipeline = Pipeline(REAL_CORPUS)
    pipeline.start()
    pipeline.process_query("volvo car")
    file_paths = pipeline.retrive_docs()

    s = pipeline.get_subjects(file_paths)
    response =  pipeline.make_response(file_paths,s)
    print(s)
    return response

if __name__ == '__main__':
    main()

