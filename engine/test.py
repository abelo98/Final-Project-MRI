import os
from typing import List, Dict, Any

from core import Core

BASE_PATH = os.getcwd()

MY_CORPUS = f'{BASE_PATH}/corpus2'
REAL_CORPUS = f'{BASE_PATH}/corpus'
OTHER = f'{BASE_PATH}/corpus/rec.autos'


def process_boolean_model(core: Core) -> List[Dict[str, Any]]:
    core.load_boolean_model()
    file_paths_and_ids_boolean = core.boolean_model.boolean_model_retrieve_docs("lion fox")

    subjects = core.get_subjects(file_paths_and_ids_boolean)

    response = core.make_response(file_paths_and_ids_boolean, subjects)
    return response


def process_vectorial_model(core: Core) -> List[Dict[str, Any]]:
    core.load_vectorial_model()

    query_process = core.vsm.process_query("lion fox")
    file_paths_and_ids_vectorial_model = core.vsm.retrieve_id_docs(query_process)

    subjects = core.get_subjects(file_paths_and_ids_vectorial_model)

    response = core.make_response(file_paths_and_ids_vectorial_model, subjects)
    
    return response


def main():
    core = Core(MY_CORPUS)

    # boolean model
    # print(process_boolean_model(core))

    # vectorial model
    print(process_vectorial_model(core))


if __name__ == '__main__':
    main()
