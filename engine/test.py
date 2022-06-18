import os

from pipeline import Pipeline

BASE_PATH = os.getcwd()

MY_CORPUS = f'{BASE_PATH}/corpus2'
REAL_CORPUS = f'{BASE_PATH}/corpus'
OTHER = f'{BASE_PATH}/corpus/rec.autos'


def main():
    pipeline = Pipeline(MY_CORPUS)
    pipeline.start()
    q_w = pipeline.process_query("lion fox")

    # file_paths_and_ids = pipeline.retrieve_id_docs(q_w)
    file_paths_and_ids_boolean = pipeline.boolean_model_retrieve_docs("lion fox")

    s = pipeline.get_subjects(file_paths_and_ids_boolean)
    response = pipeline.make_response(file_paths_and_ids_boolean, s)

    print(response)

    return response


if __name__ == '__main__':
    main()
