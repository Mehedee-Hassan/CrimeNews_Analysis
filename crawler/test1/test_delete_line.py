import platform
from bs4 import BeautifulSoup
from selenium import webdriver
from itertools import islice

__d = "@-DEBUG:"
file_1 = 'link_to_visit.bin'
file_2 = 'link_to_visit.bin.txt'
file_now = 1

def main():

    crawl()


def crawl():



    print(__d,"2 here")
    # let's parse our html

    l2v_file_reader = open('data/link_to_visit.bin.txt','r+b')

    line_no = 0


    for line in islice(l2v_file_reader,5,None):




        print(line)
        line_no = line_no + 1

    # l2v_file_reader.truncate()





    l2v_file_reader.close()

    # l2v_file_reader = open('data/link_to_visit.bin.txt','w')
    # l2v_file_reader.seek(0)
    # l2v_file_reader.write("")
    # l2v_file_reader.close()





if __name__=="__main__":
    main()