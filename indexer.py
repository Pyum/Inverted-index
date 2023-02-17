from collections import defaultdict
from bs4 import BeautifulSoup
from nltk.tokenize import RegexpTokenizer
from nltk.stem.porter import *
import json, os, sys

InvertedIndex = defaultdict({"freq": 1, "list":[], "bold":[], "title":[], "header":{"h1":[], "h2":[],"h3":[]}})
#                               Frequency | DocIDs In | In Bolded | In Title | In Header  <Header it is in>    |
#                                                     |In Theory these should be a lot smaller                 |
UniqueWords = {}

def addInvertedIndex(_documentURL, _documentContent, _docID):
    global InvertedIndex
    _tokenDict = tokenize(_documentContent)
    for _tokenWord in _tokenDict:
        if _tokenWord in InvertedIndex:
            InvertedIndex[_tokenWord]["freq"] += 1     #Add Frequency
        else:
            InvertedIndex[_tokenWord]      #Add to Dict
        InvertedIndex[_tokenWord]["list"].append(_docID)       #Add DocID (Base List)
        if _tokenWord["bold"]:                  #Is the word in bold in this document?
            InvertedIndex[_tokenWord]["bold"].append(_docID)   #Add DocID (Bold List)
        if _tokenWord["title"]:               #Is the word in the title in this document?
            InvertedIndex[_tokenWord]["title"].append(_docID)  #Add DocID (Title List)
        if len(_tokenWord["header"]) != 0:    #Is the word in the header in this document?
            for _header in _tokenWord["header"]:
                InvertedIndex[_tokenWord][_header].append(_docID) #Add DocID (Header Dict)
    return InvertedIndex

def tokenize(_documentContent):
    global UniqueWords
    _soup = BeautifulSoup(_documentContent, 'html.parser')
    _bTags = [] 
    for i in _soup.findAll('b'):
        _bTags.append(j.text for j in i.split(' ')) #Get all bold text
    _tTags = []
    for i in _soup.findAll('title'):
        _tTags.append(j.text for j in i.split(' ')) #Get all text in title
    _h1Tags = []
    for i in _soup.findAll('h1'):
        _h1Tags.append(j.text for j in i.split(' ')) #Get all text in all header 1
    _h2Tags = []
    for i in _soup.findAll('h2'):
        _h2Tags.append(j.text for j in i.split(' ')) #Get all text in all header 2
    _h3Tags = []
    for i in _soup.findAll('h3'):
        _h3Tags.append(j.text for j in i.split(' ')) #Get all text in all header 3
    _htmlText = _soup.get_text()
    _tokenList = list()
    _stemmer = PorterStemmer()
    _tokenDict = defaultdict({"bold": False, "title": False, "header":[]})
    _regExp = RegexpTokenizer('[a-zA-Z]+[\'a-zA-Z]*')
    _tokenList = _regExp.tokenize(_htmlText)
    for _word in _tokenList:
        _tokenDict = _stemmer.stem(_word) #Gets rid of plurals
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
        UniqueWords.add(_stemmer.stem(_word))
    return _tokenDict

def openJson():
    _docID = 0
    for _folder in os.listdir("DEV"):
        for _file in os.listdir("DEV/" + _folder):
            _docID += 1
            f = open("DEV/" + _folder + "/" + _file)
            _fileData = json.load(f)
            _fileContent = _fileData["content"]
            _fileURL = _fileData["url"]
            addInvertedIndex(_fileURL, _fileContent, _docID)
    return

def main():
    global UniqueWords, InvertedIndex
    openJson()

    _uniqueWordsFile = open("UniqueWords.txt", "w")
    _uniqueWordsFile.write( len(UniqueWords) + " words\n")
    for i in UniqueWords:
        _uniqueWordsFile.write( i + "\n")
    _uniqueWordsFile.close() 

    _invertedIndexFile = open("InvertedIndex.txt", "w")
    _invertedIndexFile.write( len(InvertedIndex) + " indexes\nWith size of " + sys.getsizeof(InvertedIndex))
    for keys, value in InvertedIndex.items():
        _invertedIndexFile.write( keys + " " + value + "\n")

if __name__ == '__main__':
    main()



            


