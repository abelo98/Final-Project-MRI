from typing import List, Dict, Any

from constants import *
from core import Core


def process_boolean_model(core: Core) -> List[Dict[str, Any]]:
    core.load_boolean_model()
    file_paths_and_ids_boolean = core.boolean_model.boolean_model_retrieve_docs("lion fox")

    subjects = core.get_subjects(file_paths_and_ids_boolean)

    response = core.make_response(file_paths_and_ids_boolean, subjects)
    return response


def process_vectorial_model(core: Core, query: str) -> List[Dict[str, Any]]:
    core.load_vectorial_model()

    query_process = core.vsm.process_query(query)
    file_paths_and_ids_vectorial_model = core.vsm.retrieve_id_docs(query_process)

    subjects = core.get_subjects(file_paths_and_ids_vectorial_model)

    response = core.make_response(file_paths_and_ids_vectorial_model, subjects)

    core.set_feedback(1, 51, None)

    return response


def process_vectorial_model_test_feedback(core: Core, query: str) -> None:
    core.vsm.process_query(query)


def main():
    core = Core(CRAN_CORPUS)

    # boolean model
    # print(process_boolean_model(core))

    # vectorial model
    q = "what similarity laws must be obeyed when constructing aeroelastic models\
    of heated high speed aircraft"
    response = process_vectorial_model(core, q)
    r = [184, 29, 31, 12, 51, 102, 13, 14, 15, 57, 378, 859, 185, 30, 37, 52, 142, 195, 875, 56, 66, 95, 462, 497, 858,
         876, 879, 880, 486]
    print('precision: ', core.precision(response, r))
    print('recall: ', core.recall(response, r))
    print(response)

    process_vectorial_model_test_feedback(core, q)


if __name__ == '__main__':
    main()
