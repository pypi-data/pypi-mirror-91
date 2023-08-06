import pandas as pd
import os

def test():
    dir_path = os.path.dirname(os.path.realpath(__file__))
    print(__file__)
    return ("hello am here at genstopwords")

def gno_generalstopwords():
    dir_path = os.path.dirname(os.path.realpath(__file__))
    filepath = os.path.join(dir_path, "gen_stopwords_gno.csv")
    file = open(filepath, "r", encoding = "utf8", errors = 'backslashreplace')
    GenStopWords = pd.read_csv(file, sep = ",", skipinitialspace = True, keep_default_na = False ,header="infer")
    file.close()
    return GenStopWords

def gno_generalstopwords_cn():
    dir_path = os.path.dirname(os.path.realpath(__file__))
    filepath = os.path.join(dir_path, "stopwords_cn.csv")
    file = open(filepath, "r", encoding = "utf8", errors = 'backslashreplace')
    GenStopWords_cn = pd.read_csv(file, sep = " ", skipinitialspace = True, keep_default_na = False ,header="infer")
    file.close()
    return GenStopWords_cn
    
