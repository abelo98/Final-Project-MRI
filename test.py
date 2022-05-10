from json.tool import main
from ntpath import join
from scaner import Scaner
from irm import Vector_Space_Model


def main():
    sc = Scaner()
    vsm = Vector_Space_Model(5,'/media/abelo/TERA/School/5to/SRI/Proyecto Final SRI/corpus') 

    vsm.calc_tf()
    vsm.calc_idf()
    # print(vsm.doc_tf)
    print(vsm.idf)


if __name__ == '__main__':
    main()

