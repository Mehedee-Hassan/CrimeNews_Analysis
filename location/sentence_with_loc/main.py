
import nltk
import location.sentence_with_loc.gazetteer as gaztteer



def main(doc):



    temp = process_document(doc)


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


    return  loc.sub_leaves(t,'LOCATION')



def sub_leaves(tree, label):
    return [t.leaves() for t in tree.subtrees(lambda s: s.label() == label)]



def process_document(document):
    s = nltk.sent_tokenize(document)
    s = [nltk.word_tokenize(a) for a in s]
    s = [nltk.pos_tag(a) for a in s]

    return s





if __name__=="__main__":
    doc_sample ="I was amazed to notice no protest from the readers; despite numerous news reports on housewives being killed by husbands & in-laws, due to non-receipt of committed dowries. Thank you Md. Tanjil, from the dept. of Geography and Environmental Studies, University of Chittagong, for writing against this social evil (source: The Daily Star, 03-05-2010). It usually happens among very poor citizens, living in remote villages. There is nobody to listen to them."


    main(doc_sample)





