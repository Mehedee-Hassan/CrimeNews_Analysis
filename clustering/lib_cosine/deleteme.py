

def test(a):
    a.append(10)
    a.append(20)
    a.append(30)

def k (a):
    a = 123123



def callByReference():
    a = []
    test(a)
    print(a)

    n =10
    k(n)
    print(n)


def returnDouble():
    return 'sadfasdf',22323

def returnDoubleVal():
    a ,b = returnDouble()

    print(a)
    print(b)


# returnDoubleVal()

def testset():
    t = set()
    t.add('a')
    t.add('a')
    t.add('a')
    t.add('a')
    t.add('b')

    print(t," \nlen = ",len(t))


testset()