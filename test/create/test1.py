import os

import location.sentence_with_loc
import test.create

path =  os.path.dirname(location.sentence_with_loc.__file__)
p1 = os.path.dirname(test.create.__file__)

reader = open(path+"\\gazetteers_list",'r')
reader2 = open(p1+"\\tt",'r')
reader3 = open(p1+"\\left",'a')



file1 = reader.read()
file2 = reader2.read()

a1 = file2.split('\n')
a2 = file1.split('\n')


for a in a1:
    flag = True

    arr1 = a.split(' ')

    for aa in a2:
        arr2 = aa.split(' ')

        try:
            if arr1[0] == arr2[0]:
                flag = False
                break
        except:
            flag = False
            print("")

    print(a)
    if flag == True:

        reader3.write(a+"\n")


reader.close()
reader2.close()
reader3.close()








