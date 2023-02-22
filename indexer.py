from collections import defaultdict
from bs4 import BeautifulSoup
from nltk.tokenize import RegexpTokenizer
from nltk.stem.porter import *
import json, os, sys, nltk, re

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
            for _header in _tokenDict[_tokenWord]["header"]:
                InvertedIndex[_tokenWord]["header"][_header].append(_docID) #Add DocID (Header Dict)
    return InvertedIndex

def tokenizeQuery(_query):
    _tokenizedQuery = set()
    _stemmer = PorterStemmer()
    for _word in _query.split(" "):
        _tokenizedQuery.add(_stemmer.stem(_word))
    return _tokenizedQuery

def tokenize(_documentContent):
    global UniqueWords
    _stemmer = PorterStemmer()
    _soup = BeautifulSoup(_documentContent, 'html.parser')
    _tTags = set()
    if _soup.title is not None:
        for i in _soup.title.getText().split(" "):
            _tTags.add(_stemmer.stem(i))
    _bTags = set() 
    for i in _soup.findAll('b'):
        if len(i) > 0:
            for j in str(i.getText()).split(" "):
                for k in j.split("\n"):
                    _bTags.add(_stemmer.stem(k)) #Get all bold text
    _h1Tags = set()
    for i in _soup.findAll('h1'):
        if len(i) > 0:
            for j in str(i.getText()).split(" "):
                for k in j.split("\n"):
                    _h1Tags.add(_stemmer.stem(k)) #Get all text in all header 1
    _h2Tags = set()
    for i in _soup.findAll('h2'):
        if len(i) > 0:
            for j in str(i.getText()).split(" "):
                for k in j.split("\n"):
                    _h2Tags.add(_stemmer.stem(k)) #Get all text in all header 2
    _h3Tags = set()
    for i in _soup.findAll('h3'):
        if len(i) > 0:
            for j in str(i.getText()).split(" "):
                for k in j.split("\n"):
                    _h3Tags.add(_stemmer.stem(k)) #Get all text in all header 3
    _htmlText = _soup.get_text()
    #text = re.sub(r"[^a-zA-Z0-9]", " ", _htmlText) # remove all symbols before tokenizing
    #_tokenList = nltk.word_tokenize(text)
    _regExp = RegexpTokenizer('[a-zA-Z]+')
    _tempTokenList = _regExp.tokenize(_htmlText)
    _tokenList = [nltk.word_tokenize(_token) for _token in _tempTokenList]
    _tokenDict = defaultdict()
    for _word in _tokenList:
        _codeWord = _stemmer.stem(_word[0])
        _tokenDict[_codeWord] = {"bold": False, "title": False, "header":[]} #Gets rid of plurals
        
        if _codeWord in _bTags:
            _tokenDict[_codeWord]["bold"] = True #Checking if word is bold 
        if _codeWord in _tTags:
            _tokenDict[_codeWord]["title"] = True #Checking if word is in the title
        if _codeWord in _h1Tags:
            _tokenDict[_codeWord]["header"].append("h1") #Checking if word is in a header 1
        if _codeWord in _h2Tags:
            _tokenDict[_codeWord]["header"].append("h2") #Checking if word is in a header 2
        if _codeWord in _h3Tags:
            _tokenDict[_codeWord]["header"].append("h3") #Checking if word is in a header 3
        UniqueWords.add(_codeWord)
    return _tokenDict

def openJson():
    _docID = 0
    for _folder in os.listdir("DEV"):
        print("In folder " + _folder)
        for _file in os.listdir("DEV/" + _folder):
            _docID += 1
            print("    On docID #" + str(_docID) + "/55393") #TODO Delete
            f = open("DEV/" + _folder + "/" + _file)
            _fileData = json.load(f)
            _fileContent = _fileData["content"]
            _fileURL = _fileData["url"]
            addInvertedIndex(_fileURL, _fileContent, _docID)
    return

def intersect (_word1, _word2):
    global InvertedIndex
    _finalLst = []
    _firstWord = _word1
    _secondWord = _word2
    if InvertedIndex[_word2]["freq"] < InvertedIndex[_word1]["freq"]:
        _firstWord = _word2
        _secondWord = _word1
    for _docID in InvertedIndex[_firstWord]["list"]:
            if _docID in InvertedIndex[_secondWord]["list"]:
                _finalLst.addpend(_docID)
    return _finalLst

def getlinks (listOfDocID):
    _docID = 0
    _linksList = []
    for _folder in os.listdir("DEV"):
        for _file in os.listdir("DEV/" + _folder):
            _docID += 1
            if _docID in listOfDocID:
                f = open("DEV/" + _folder + "/" + _file)
                _fileData = json.load(f)
                _linksList.append(_fileData["url"])
    return _linksList


def main():
    global UniqueWords, InvertedIndex
    nltk.download('punkt')
    openJson()
    askQuery = True
    if askQuery:
        _query = input("Indexing Complete...\nWhat would you like to seach for:\n")
        _listOfQueryWords = tokenizeQuery(_query)
        


    _uniqueWordsFile = open("UniqueWords.txt", "w")
    _uniqueWordsFile.write( str(len(UniqueWords)) + " words\n")
    for i in UniqueWords:
        _uniqueWordsFile.write( i + "\n")
    _uniqueWordsFile.close() 

    _invertedIndexFile = open("InvertedIndex.txt", "w")
    _invertedIndexFile.write( str(len(InvertedIndex)) + " indexes\nWith size of " + str(sys.getsizeof(InvertedIndex)) + "\n\n")

    for keys, value in InvertedIndex.items():
        _invertedIndexFile.write(keys + "\n     ")
        for i in value:
            _invertedIndexFile.write(" " + i + " ")
            _invertedIndexFile.write(str(value[i]) + "\n     ")
        _invertedIndexFile.write("\n")



        

if __name__ == '__main__':
    main()



            


