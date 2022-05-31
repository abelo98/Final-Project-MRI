from pipeline import Pipeline

MY_CORPUS = '/home/jch/Documents/School/5to/SRI/Final-Project-MRI/engine/corpus2'
REAL_CORPUS = '/media/abelo/TERA/School/5to/SRI/PF SRI/Test Collections/20 Newsgroups/20news-18828'
OTHER = '/media/abelo/TERA/School/5to/SRI/Proyecto Final SRI/engine/corpus/rec.autos'


def main():
    pipeline = Pipeline(MY_CORPUS)
    pipeline.start()
    pipeline.process_query("lion")
    file_paths_and_ids = pipeline.retrive_id_docs()

    s = pipeline.get_subjects(file_paths_and_ids)
    response = pipeline.make_response(file_paths_and_ids, s)
    # print(s)
    print(response)
    return response


if __name__ == '__main__':
    main()
