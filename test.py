from json.tool import main
from ntpath import join
from scaner import Scaner
from irm import Vector_Space_Model


def main():
    sc = Scaner('/media/abelo/TERA/School/5to/SRI/Proyecto Final SRI/corpus')
    dir_files = list(sc.get_files())
    vsm = Vector_Space_Model(len(dir_files),dir_files,sc) 

    vsm.calc_tf()
    vsm.calc_idf()
    vsm.calc_weights()
    # print(vsm.idf)
    # print(vsm.doc_tf)
    # print(vsm.doc_wights)

    q = sc.doc_to_tokens("otter and lion")
    vsm.calc_query_tf(q)
    vsm.calc_query_weights(0.5)


    print(vsm.retrive_docs(2))



if __name__ == '__main__':
    main()

