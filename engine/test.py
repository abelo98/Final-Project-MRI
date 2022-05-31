from uuid import UUID
from pipeline import Pipeline

MY_CORPUS = '/media/abelo/TERA/School/5to/SRI/Proyecto Final SRI/engine/corpus2'
REAL_CORPUS = '/media/abelo/TERA/School/5to/SRI/PF SRI/Test Collections/20 Newsgroups/20news-18828'
OTHER ='/media/abelo/TERA/School/5to/SRI/Proyecto Final SRI/engine/corpus/rec.autos'

def main():
    pipeline = Pipeline(REAL_CORPUS)
    pipeline.start()
    pipeline.process_query("volvo")
    file_paths_and_ids = pipeline.retrive_id_docs()

    s = pipeline.get_subjects(file_paths_and_ids)
    response =  pipeline.make_response(file_paths_and_ids,s)
    txt = pipeline.retrive_doc(UUID('2e13dab8-5d7a-43cb-af22-bbfae7adaa4f'))
    print(txt)
    return response

if __name__ == '__main__':
    main()
