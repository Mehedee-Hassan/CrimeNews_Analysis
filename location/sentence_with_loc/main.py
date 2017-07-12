
import nltk
import location.sentence_with_loc.gazetteer as gaztteer



def main(doc):



    temp = process_document(doc)
    # print("debug## temp",temp)

    # print(nltk.corpus.treebank.tagged_sents()[22])
    # print("==========")
    #
    # test1 = temp[0]
    singleArray = []


    for t in temp:
        singleArray.extend(t)

    # print (singleArray)


    # temp_ne = nltk.ne_chunk(singleArray)
    # print (temp_ne)

    loc = gaztteer.LocationChunker()
    t = loc.parse(singleArray)

    # a = "For/IN the/DT past/JJ few/JJ days/NNS ,/, there/EX has/VBZ been/VBN a/DT rather/RB surprising/JJ change/NN in/IN the/DT way/NN things/NNS go/VBP on/IN at/IN the/DT Agargaon/NNP passport/NN office/NN in/IN the/DT capital/NN"

    # print("===")
    # print (t)
    # print(loc.sub_leaves(t,'LOCATION'))
    # print(t)
    # print(loc)

    return  loc.sub_leaves(t,'LOCATION')



def sub_leaves(tree, label):
    return [t.leaves() for t in tree.subtrees(lambda s: s.label() == label)]


# import re
def process_document(document):

    # p = re.compile('\w+')

    tokenizer = nltk.RegexpTokenizer(r'\w+')
    s = nltk.sent_tokenize(document)
    # print("s = ",s)
    s = [ tokenizer.tokenize(a) for a in s]
    # print("s = ",s)
    s = [nltk.pos_tag(a) for a in s]

    return s





if __name__=="__main__":
    doc_sample ="A suspected bomber died in what is believed to be a suicide blast at a barrack of the Rapid Action Battalion (Rab) in Dhaka’s Ashkona area during Jumma prayers this afternoon. The bomber died on the spot and two Rab men were “slightly injured,” Mufti Mahmud Khan, director of the force’s legal and media wing, told The Daily Star.The Ashkona Rab barracks is a proposed site for the headquarters of the elite force. Currently, it is mostly an empty space fenced by brick walls. Inside, a large barrack is situated."


    main(doc_sample)





