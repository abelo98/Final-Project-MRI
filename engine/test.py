import os
from typing import List, Dict, Any

from core import Core

BASE_PATH = os.getcwd()

CRAN_QUERY_RESULT = f'{BASE_PATH}/queries_rel/cranqrel'
MED_QUERY_RESULT = f'{BASE_PATH}/queries_rel/MED.REL'
CRAN_QUERIES = f'{BASE_PATH}/queries_rel/cran.qry'
MED_QUERIES = f'{BASE_PATH}/queries_rel/MED.QRY'
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
       
        for i,splited_text in enumerate(queries_splited):
            q = splited_text.split('\n.W\n')[1]
            try:
                queries[i+1].append(q)
            except KeyError:
                queries[i+1] = q
        f.close()
        return queries

def run_tests(dir_results,dir_q,dir_corpus):
    best = parse_query_rel(dir_results)
    queries = parse_query_request(dir_q)
    core = Core(dir_corpus)

    precision = 0
    recall = 0
    f1 = 0

    precision_exp = 0
    recall_exp = 0
    f1_exp = 0

    total_q = len(queries)

    for i,q in enumerate(queries.values()):
        q_exp = core.query_exp.expand_query(q)

        response_exp = process_vectorial_model(core,q_exp)
        response_normal = process_vectorial_model(core,q)

        precision += core.precision(response_normal,best[i+1])
        recall += core.recall(response_normal,best[i+1])
        x = core.f1(response_normal,best[i+1])
        f1 += x

        if(x == 0): 
            print("query con 0 f1: ")
            print(" ")
            print(q)


        precision_exp += core.precision(response_exp,best[i+1])
        recall_exp += core.recall(response_exp,best[i+1])
        x_exp = core.f1(response_exp,best[i+1])
        f1_exp += x_exp

        if(x_exp == 0): 
            print("query expanded con 0 f1 : ",i+1)
            print(" ")
            print(q_exp)

    print('mean precision: ',precision/total_q,'%')
    print('mean recall: ',recall/total_q,'%')
    print('mean f1: ',f1/total_q,'%')
    print(" ")
    print('mean precision with expanded queries: ',precision_exp/total_q,'%')
    print('mean recall with expanded queries: ',recall_exp/total_q,'%')
    print('mean f1 with expanded queries: ',f1_exp/total_q,'%')


def main():
    run_tests(CRAN_QUERY_RESULT,CRAN_QUERIES,CRAN_CORPUS)

    # core = Core(CRAN_CORPUS)

    # # boolean model
    # # print(process_boolean_model(core))

    # # vectorial model
    # q = parse_query_request(CRAN_QUERIES)
    # q_exp = core.query_exp.expand_query(q)
    # print(q_exp)
    # response = process_vectorial_model(core,q_exp)


    # best = parse_query_rel(CRAN_QUERY_RESULT)
    # print('precision: ',core.precision(response,best[1]),'%')
    # print('recall: ',core.recall(response,best[1]),'%')
    # print('f1: ',core.f1(response,best[1]),'%')



if __name__ == '__main__':
    main()
