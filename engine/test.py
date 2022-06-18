from pipeline import Pipeline

MY_CORPUS = '/home/jch/Documents/School/5to/SRI/Final-Project-MRI/engine/corpus2'
REAL_CORPUS = '/media/abelo/TERA/School/5to/SRI/Proyecto Final SRI/engine/corpus'
OTHER = '/media/abelo/TERA/School/5to/SRI/Proyecto Final SRI/engine/corpus/rec.autos'


def main():
    pipeline = Pipeline(REAL_CORPUS)
    pipeline.start()
    q_w = pipeline.process_query("volvo")

    file_paths_and_ids = pipeline.retrieve_id_docs(q_w)

    s = pipeline.get_subjects(file_paths_and_ids)
    response = pipeline.make_response(file_paths_and_ids, s)
    print(s)

    return response


if __name__ == '__main__':
    main()
