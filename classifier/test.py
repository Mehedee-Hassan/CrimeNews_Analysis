import os

import sys

import classifier


import pprint

def test2():

    txt ="A murder case accused was killed in a “gunfight” with detectives in Dhaka’s Mirpur area early today. The deceased was identified as Sohel, 30, Sazzadur Rahman, deputy commissioner of Detective Branch of Dhaka police, told The Daily Star. Being informed that a wanted criminal along with his associates was gathering near Lohar Pool in Bhashantek, detectives conducted a drive there around 2:00am, he said. \"As soon as police reached the spot, the gang members opened fire on them prompting the police personnel to retaliate – which triggered a gunfight,\" he said. Later, police found Sohel lying there. He was rushed to the Dhaka Medical College Hospital where the doctors declared him dead, said the senior DB official. Police also arrested two—Hiron and Sohan—from the spot while others managed to flee the scene, Sazzadur said. Detectives also recovered a pistol, two revolvers and ammunition from the scene."

    print(txt)
    pprint.pprint(txt)

def test1():
    cc = os.path.dirname(os.path.realpath('test.py'))

    print(cc)
    p = os.path.abspath('.')
    print(p)




    top_file_path = os.path.dirname(sys.modules['__main__'].__file__)


    # top_file_path = os.path.join(os.path.dirname(classifier.__file__), 'main.py')

    print(top_file_path)
    print(os.path.abspath(__file__))


    path = os.path.abspath(__file__)



# test1()
test2()