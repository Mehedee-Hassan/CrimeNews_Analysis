
import os
import sys
import nltk
from nltk.stem import WordNetLemmatizer


path = "J:\\bk_data\\new_decode_download\\___crime_data_title_fstop_nodate\\"

def deleteLines():
    files = os.listdir(path)

    for file in files:

        with open(path+file, 'r',encoding='utf-8') as fin:
            data = fin.read().splitlines(True)

        with open(path+file, 'w',encoding='utf-8') as fout:
            fout.writelines(data[1:])



if __name__ == '__main__':
    deleteLines()