import time

import classifier
import clustering
import crawler
import location
from clustering import console_main
from location import  main_from_db
from crawler import crawler_main
from classifier import portable_main
import shutil
import config.config
import os
from location import main as locationMain

path =  os.path.abspath('.')

def main():

    print(path)
    while True:

        print("(1) rank location from database")
        print("(2) crawl and save")
        print("(3) classify raw data and save ")
        print("(4) Group story based on a news ")
        print("(5) single document classify ")
        print("(6) single document location extraction ")

        a = input('\nInput Option: ')

        if a == "1":
            main_from_db.Main()
        elif a == '2':
            crawler_main.main()
        elif a == '4':
            console_main.search_main()
        elif a == '5':
            doc = input('Search document string :')
            result = portable_main.singleDocClassify(doc)

            if result == 'crime':
                print('Crime related news')

            else:
                print('Not a crime news')

            print("\n\n")

        elif a == '6':
            doc = input('Document string for location:')
            locationList = locationMain.readSingle(doc)


            print("\nCrime locations :")

            for location in locationList:
                print(location)

            if len(locationList) == 0:
                print("no crime location found.")

            print("\n\n")

        elif a == '3':
            try:
                shutil.rmtree(config.config.__temp_dir_name)
                os.mkdir(path+"\\"+config.config.__temp_dir_name)
                os.mkdir(path+"\\"+config.config.__temp_dir_name_nc)
                os.mkdir(path+"\\"+config.config.__temp_dir_name_c)

                portable_main.classify_and_save()


            except Exception as e:

                os.mkdir(path + "\\" + config.config.__temp_dir_name)
                os.mkdir(path + "\\" + config.config.__temp_dir_name_nc)
                os.mkdir(path + "\\" + config.config.__temp_dir_name_c)

                try:
                    portable_main.classify_and_save()
                except Exception as e:

                    print ("could not classify :",str(e))

                print("file not found" ,str(e))


        time.sleep(2)
        print("\n\n")


if __name__=='__main__':
    main()