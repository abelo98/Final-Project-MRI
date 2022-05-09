from json.tool import main
from scaner import Scaner
from irm import Vector_Space_Model

def main():
    sc = Scaner()
    vsm = Vector_Space_Model(5,'/media/abelo/TERA/School/5to/SRI/Proyecto Final SRI/corpus') 

    vsm.calc_tf()

if __name__ == '__main__':
    main()

