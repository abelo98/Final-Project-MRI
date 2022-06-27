from cProfile import run
from typing import List, Dict, Any

from constants import *
from core import Core
from query_sim import query_processor


def process_boolean_model(core: Core) -> List[Dict[str, Any]]:
    core.load_boolean_model()
    file_paths_and_ids_boolean = core.boolean_model.boolean_model_retrieve_docs("lion fox")

    subjects = core.get_subjects(file_paths_and_ids_boolean)

    response = core.make_response(file_paths_and_ids_boolean, subjects)
    return response


def process_vectorial_model(core: Core, query_vect: dict) -> List[Dict[str, Any]]:
    file_paths_and_ids_vectorial_model = core.vsm.retrieve_id_docs(query_vect)

    subjects = core.get_subjects(file_paths_and_ids_vectorial_model)

    response = core.make_response(file_paths_and_ids_vectorial_model, subjects)

    core.set_feedback(1, 51, None)

    return response


def parse_query_rel(dir):
    with open(dir) as f:
        docs_for_query = {}
        queries_result = f.read().split('\n')

        for result in queries_result:
            elements = result.split(' ')
            try:
                docs_for_query[int(elements[0])].append(int(elements[1]))
            except KeyError:
                docs_for_query[int(elements[0])] = [int(elements[1])]
        f.close()
        return docs_for_query


def parse_query_request(dir):
    with open(dir) as f:
        queries = {}
        queries_splited = f.read().split('\n.I')

        for i, splited_text in enumerate(queries_splited):
            q = splited_text.split('\n.W\n')[1]
            try:
                queries[i + 1].append(q)
            except KeyError:
                queries[i + 1] = q
        f.close()
        return queries


def run_tests(dir_results, dir_q, core: Core):
    best = parse_query_rel(dir_results)
    queries = parse_query_request(dir_q)
    q_p = query_processor()

    precision = 0
    recall = 0
    f1 = 0

    precision_exp = 0
    recall_exp = 0
    f1_exp = 0

    total_q = len(queries)

    for i,q in enumerate(queries.values()):
        q_exp = core.query_exp.expand_query(q)[1]

        query_process = core.vsm.process_query(q)
        query_process_exp = core.vsm.process_query(q_exp)

        response_exp = process_vectorial_model(core,query_process)
        response_normal = process_vectorial_model(core,query_process_exp)


        precision += core.precision(response_normal,best[i+1])
        recall += core.recall(response_normal,best[i+1])
        x = core.f1(response_normal,best[i+1])
        f1 += x

        if(x == 0): 
            print("query con 0 f1: ")
            print(" ")
            print(q)
            print(' ')
            print('sugested: ', q_p.similar(q,query_process,k=1))

        q_p.save_query(q,query_process)

        precision_exp += core.precision(response_exp,best[i+1])
        recall_exp += core.recall(response_exp,best[i+1])
        x_exp = core.f1(response_exp,best[i+1])
        f1_exp += x_exp

        if (x_exp == 0):
            print("query expanded con 0 f1 : ", i + 1)
            print(" ")
            print(q_exp)

    print('mean precision: ', precision / total_q, '%')
    print('mean recall: ', recall / total_q, '%')
    print('mean f1: ', f1 / total_q, '%')
    print(" ")
    print('mean precision with expanded queries: ', precision_exp / total_q, '%')
    print('mean recall with expanded queries: ', recall_exp / total_q, '%')
    print('mean f1 with expanded queries: ', f1_exp / total_q, '%')


def process_vectorial_model_test_feedback(core: Core, query: str) -> None:
    core.vsm.process_query(query)


def test_med():
    core = Core(MED_CORPUS,MED_CORPUS_NAME)
    core.load_vectorial_model(MED_CORPUS_NAME)
    run_tests(MED_QUERY_RESULT,MED_QUERIES,core)
    
def test_cran():
    core = Core(CRAN_CORPUS)
    core.load_vectorial_model(CRAN_CORPUS_NAME)
    run_tests(CRAN_QUERY_RESULT,CRAN_QUERIES,core)

def test_20newsgroup(q:str):
    core = Core(NEWS_GROUPS_CORPUS,NEWS_GROUPS_CORPUS_NAME)
    core.load_vectorial_model(NEWS_GROUPS_CORPUS_NAME)
    query_process = core.vsm.process_query(q)

    q_exp = core.query_exp.expand_query(q)
    print(q_exp)
    print(' ')
    response = process_vectorial_model(core,query_process)
    print(response)


def main():
    test_med()
    test_cran()

    
if __name__ == '__main__':
    main()
