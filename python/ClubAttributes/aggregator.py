import spacy                         # See "Installing spaCy"
import pandas as pd

class aggregator:

    df=pd.read_csv('documents.csv', sep=',')

    nlp = spacy.load('en_core_web_sm')
    #nlp = spacy.load('en_vectors_glove_md')
    similarityFactor = .73#.74

    attrList = [x[0] for x in df.values]
    attrNLP = []
    for index, word in enumerate(attrList):
        attrNLP.append(nlp.make_doc(word))

    print('Phrase size:' + str(len(attrNLP)) + "  Similarity < " + str(similarityFactor))

    similarityList = []

    for index, word in enumerate(attrNLP):
        tempArr = []
        #tempdict = {}
        tempArr.append(str(word))
        tempArr.append(index)
        for index2, word2 in enumerate(attrNLP):
            if(index2 > index):
                similarity = word.similarity(word2)
                if similarity > similarityFactor:
                    #print(str(word) + " and " + str(word2) + " similarity: " + str(similarity))
                    ta = []
                    ta.append(word2)
                    ta.append(index2)
                    ta.append(similarity)
                    tempArr.append(ta)
                    attrNLP.remove(word2)
        
        if(len(tempArr) > 2):
            similarityList.append(tempArr)

    for line in similarityList:
        print(str(line))
