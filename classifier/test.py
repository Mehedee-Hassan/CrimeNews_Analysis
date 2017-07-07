import os

import sys

import classifier



cc = os.path.dirname(os.path.realpath('test.py'))

print(cc)
p = os.path.abspath('.')
print(p)




top_file_path = os.path.dirname(sys.modules['__main__'].__file__)


# top_file_path = os.path.join(os.path.dirname(classifier.__file__), 'main.py')

print(top_file_path)
print(os.path.abspath(__file__))


path = os.path.abspath(__file__)