
import os
import sys
import nltk
from nltk.stem import WordNetLemmatizer
import classifier


# crime_path = "D:\\google_drive\\MSc Research\\implement\\nlp python\\classification\\classification1\\svm_test\\test_classification1\\data\\crime"
# noncrime_path = "D:\\google_drive\\MSc Research\\implement\\nlp python\\classification\\classification1\\svm_test\\test_classification1\\data\\ncrime"

crime_path = classifier.__file__+"\\data\\crime"
noncrime_path = classifier.__file__+"\\data\\ncrime"

word_path = "wordlist.txt"



def main():


    word_dictionary = []

    with open(word_path ,"r") as files:
        lines = files.readlines()
        for l in lines:
            l = l.strip('\n')
            l = l.lower()

            word_dictionary.append(l)



        print(word_dictionary[0:20])

    crimefiles = os.listdir(crime_path)
    noncrimefiles = os.listdir(noncrime_path)
    performWork(crimefiles,word_dictionary)
    performWork(noncrimefiles,word_dictionary)




def performWork(files,word_dictionary):
    file_word_list = open("wordlist_not_english.txt", 'w+')
    wordnet_lemmatizer = WordNetLemmatizer()

    i = 0
    for cf in files:
        print ("i = ",i)
        i += 1
        with open(crime_path+"\\"+cf , "r") as f :
            lines = f.readlines()
            for line in lines:

                line = line.lower()
                words = nltk.word_tokenize(line)

                for w in words:
                    w = wordnet_lemmatizer.lemmatize(w)

                    if w not in word_dictionary and not w.isdigit():
                        file_word_list.write(w+"\n")

    file_word_list.close()



if __name__ == "__main__":
    main()


