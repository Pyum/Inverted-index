from collections import defaultdict
from bs4 import BeautifulSoup
from nltk.tokenize import RegexpTokenizer
from nltk.stem.porter import *
import json, os, sys, nltk

InvertedIndex = defaultdict()

UniqueWords = set()

def addInvertedIndex(_documentURL, _documentContent, _docID):
    global InvertedIndex
    _tokenDict = tokenize(_documentContent)
    for _tokenWord in _tokenDict.keys():
        if _tokenWord in InvertedIndex:
            InvertedIndex[_tokenWord]["freq"] += 1     #Add Frequency
        else:
            InvertedIndex[_tokenWord] = {"freq": 1, "list":[], "bold":[], "title":[], "header":{"h1":[], "h2":[],"h3":[]}}      #Add to Dict
            #                            Frequency | DocIDs In | In Bolded | In Title | In Header  <Header it is in>    |
            #                                      |In Theory these should be a lot smaller                             |
        InvertedIndex[_tokenWord]["list"].append(_docID)       #Add DocID (Base List)
        if _tokenDict[_tokenWord]["bold"]:                  #Is the word in bold in this document?
            InvertedIndex[_tokenWord]["bold"].append(_docID)   #Add DocID (Bold List)
        if _tokenDict[_tokenWord]["title"]:               #Is the word in the title in this document?
            InvertedIndex[_tokenWord]["title"].append(_docID)  #Add DocID (Title List)
        if len(_tokenDict[_tokenWord]["header"]) != 0:    #Is the word in the header in this document?
            for _header in _tokenWord["header"]:
                InvertedIndex[_tokenWord][_header].append(_docID) #Add DocID (Header Dict)
    return InvertedIndex

def tokenize(_documentContent):
    global UniqueWords
    _soup = BeautifulSoup(_documentContent, 'html.parser')
    _bTags = [] 
    for i in _soup.findAll('b'):
        if type(i) == str:
            _bTags.append(j.text for j in i.split(' ')) #Get all bold text
    _tTags = []
    for i in _soup.findAll('title'):
        if type(i) == str:
            _tTags.append(j.text for j in i.split(' ')) #Get all text in title
    _h1Tags = []
    for i in _soup.findAll('h1'):
        if type(i) == str:
            _h1Tags.append(j.text for j in i.split(' ')) #Get all text in all header 1
    _h2Tags = []
    for i in _soup.findAll('h2'):
        if type(i) == str:
            _h2Tags.append(j.text for j in i.split(' ')) #Get all text in all header 2
    _h3Tags = []
    for i in _soup.findAll('h3'):
        if type(i) == str:
            _h3Tags.append(j.text for j in i.split(' ')) #Get all text in all header 3
    _htmlText = _soup.get_text()
    text = re.sub(r"[^a-zA-Z0-9]", " ", _htmlText) # remove all symbols before tokenizing
    _tokenList = nltk.word_tokenize(text)
    _stemmer = PorterStemmer()
    _tokenDict = defaultdict()
    for _word in _tokenList:
        _tokenDict[_stemmer.stem(_word)] = {"bold": False, "title": False, "header":[]} #Gets rid of plurals
        '''
        if _word in _bTags:
            _tokenDict[_stemmer.stem(_word)]["bold"] = True #Checking if word is bold 
        if _word in _tTags:
            _tokenDict[_stemmer.stem(_word)]["title"] = True #Checking if word is in the title
        if _word in _h1Tags:
            _tokenDict[_stemmer.stem(_word)]["header"].append("h1") #Checking if word is in a header 1
        if _word in _h2Tags:
            _tokenDict[_stemmer.stem(_word)]["header"].append("h2") #Checking if word is in a header 2
        if _word in _h3Tags:
            _tokenDict[_stemmer.stem(_word)]["header"].append("h3") #Checking if word is in a header 3
        '''
        UniqueWords.add(_stemmer.stem(_word))
    return _tokenDict

def openJson():
    _docID = 0
    for _folder in os.listdir("DEV"):
        print("In folder " + _folder)
        for _file in os.listdir("DEV/" + _folder):
            _docID += 1
            print("On docID " + str(_docID)) #TODO Delete
            f = open("DEV/" + _folder + "/" + _file)
            _fileData = json.load(f)
            _fileContent = _fileData["content"]
            _fileURL = _fileData["url"]
            addInvertedIndex(_fileURL, _fileContent, _docID)
    return

def main():
    global UniqueWords, InvertedIndex
    nltk.download('punkt')
    openJson()

    _uniqueWordsFile = open("UniqueWords.txt", "w")
    _uniqueWordsFile.write( str(len(UniqueWords)) + " words\n")
    for i in UniqueWords:
        _uniqueWordsFile.write( i + "\n")
    _uniqueWordsFile.close() 

    _invertedIndexFile = open("InvertedIndex.txt", "w")
    _invertedIndexFile.write( str(len(InvertedIndex)) + " indexes\nWith size of " + str(sys.getsizeof(InvertedIndex)))
    '''
    for keys, value in InvertedIndex.items():
        _invertedIndexFile.write( keys)
        for i in value:
            _invertedIndexFile.write(" " + i + " ")
            _invertedIndexFile.write(str(value[i]))
        _invertedIndexFile.write("\n")
    '''
        

if __name__ == '__main__':
    main()



            


