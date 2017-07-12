import nltk.data
import os
import location.sentence_with_loc.main as gaz



__path = "D:/google_drive/MSc Research/implement/nlp python/classification/classification1/svm_test/test_classification1/data/crime/"
__path_file = "\D:/google_drive/MSc Research/implement/nlp python/classification/classification1/svm_test/test_classification1/data/crime/1.txt"

__to_write_path = 'list_of_sentence_with_loc.txt'

tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')


def line_token(data):

    lines = tokenizer.tokenize(data)
    # print ('\n-----\n'.join(lines))
    # print(lines)

    location_lines = []

    for line in lines:
        locs = gaz.main(line)
        # print("*********************")
        # print("locs = ",locs)
        # print("=size =",len(locs))

        if len(locs) != 0:
            location_lines.append((line,locs))


        # print("*********************")
    return location_lines



def readDir():
    files = os.listdir(__path)

    p1 = __path+"/"


    # reader = open(__path_file)
    # text = reader.read()
    #
    # line_token(text)
    #
    # reader.close()
    i = 0
    for file in files:



        reader = open(p1+file ,"r")

        text = reader.read()

        lines = line_token(text)

        # data.append(text)

        reader.close()


def write_location(line_with_loc):
    write_to = open(__to_write_path, 'a')
    write_to.write(line_with_loc)
    write_to.write("\n\n")

    write_to.close()


if __name__=="__main__":
    readDir()