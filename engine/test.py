import os
from typing import List, Dict, Any

from core import Core

BASE_PATH = os.getcwd()

MY_CORPUS = f'{BASE_PATH}/corpus2'
CRAN_CORPUS = f'{BASE_PATH}/corpus_cran'
MED_CORPUS = f'{BASE_PATH}/corpus_med'
REAL_CORPUS = f'{BASE_PATH}/corpus'
OTHER = f'{BASE_PATH}/corpus/rec.autos'


def process_boolean_model(core: Core) -> List[Dict[str, Any]]:
    core.load_boolean_model()
    file_paths_and_ids_boolean = core.boolean_model.boolean_model_retrieve_docs("lion fox")

    subjects = core.get_subjects(file_paths_and_ids_boolean)

    response = core.make_response(file_paths_and_ids_boolean, subjects)
    return response


def process_vectorial_model(core: Core, query:str) -> List[Dict[str, Any]]:
    core.load_vectorial_model()

    query_process = core.vsm.process_query(query)
    file_paths_and_ids_vectorial_model = core.vsm.retrieve_id_docs(query_process)

    subjects = core.get_subjects(file_paths_and_ids_vectorial_model)

    response = core.make_response(file_paths_and_ids_vectorial_model, subjects)
    
    return response


def main():
    core = Core(CRAN_CORPUS)

    # boolean model
    # print(process_boolean_model(core))

    # vectorial model
    q = "what similarity laws must be obeyed when constructing aeroelastic models\
    of heated high speed aircraft"
    q_exp = core.query_exp.expand_query(q)
    print(q_exp)
    response = process_vectorial_model(core,q_exp)
    r = [184,29 ,31  ,12  ,51   ,102   ,13   ,14   ,15  ,57  ,378  ,859  ,185  ,30  , 37 , 52  , 142  , 195  , 875  , 56  , 66  , 95  , 462  ,497  , 858, 876, 879, 880,  486]
    print('precision: ',core.precision(response,r),'%')
    print('recall: ',core.recall(response,r),'%')
    print('f1: ',core.f1(response,r),'%')



if __name__ == '__main__':
    main()
