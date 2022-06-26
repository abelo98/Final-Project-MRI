import os

BASE_PATH = os.path.join(os.getcwd(), 'corpus')

TF_DOCS_FILE = "tf_doc_table"
IDF_FILE = "idf_table"
INVERT_LIST_FILE = "invert_list_table"
DOCS_W = "docs_weights"
NORM_DOCS = "norm_docs"
DOCS_IDS = "docs_ids"

MY_CORPUS = f'{BASE_PATH}/corpus2'
CRAN_CORPUS = f'{BASE_PATH}/corpus_cran'
MED_CORPUS = f'{BASE_PATH}/corpus_med'
NEWS_GROUPS_CORPUS = f'{BASE_PATH}/corpus_20newsgroup'
REAL_CORPUS = f'{BASE_PATH}/corpus'
OTHER = f'{BASE_PATH}/rec.autos'

CRAN_CORPUS_NAME = 'cran'
MED_CORPUS_NAME = 'name'
NEWS_GROUPS_CORPUS_NAME = '20newsgroup'

CORR = "correlation_mat"

CRAN_QUERY_RESULT = f'{os.getcwd()}/queries_rel/cranqrel'
MED_QUERY_RESULT = f'{os.getcwd()}/queries_rel/MED.REL'
CRAN_QUERIES = f'{os.getcwd()}/queries_rel/cran.qry'
MED_QUERIES = f'{os.getcwd()}/queries_rel/MED.QRY'
