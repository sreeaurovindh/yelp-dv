#Alankrit Shah

import wikipedia
import traceback

class SaveCuisines():
    def GetCuisineUrls():
        cuisineFile = open('cuisine.txt','r')
        array = [line.strip('\n') for line in cuisineFile]
        urlFile = open('urlFileB.txt', 'w')
        matchedURLList = []

        try:
            for selection in array:
                resultArray = wikipedia.search(selection + ' food')
                wikiPage = None

                print selection + ' ---------------------------'

                matches = 0
                for i in resultArray:
                    #print i

                    if any(keyword in i.split() for keyword in ['food', 'cuisine', 'dishes']):
                        try:
                            wikiPage = wikipedia.page(i)
                        except Exception as e:
                            print 'Exception ' + str(e) +'\n' + traceback.format_exc()

                        if(wikiPage):
                            matches += 1
                            matchedURLList.append(wikiPage.url)
                            urlFile.write(wikiPage.url + '\n')
                            print 'Matched: ' + str(matches) + '  ' + wikiPage.url + ' Asize:' + str(len(matchedURLList))

                if(matches == 0):
                    print selection + '  ' + str(matches) + ' None matched====================++++++++++++++++++++++++++++++++++++'

        except Exception as e:
            print 'EXCEPTION: ' + str(e)

    if __name__ == "__main__":
        GetCuisineUrls()
