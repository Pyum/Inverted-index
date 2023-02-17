from collections import defaultdict
from bs4 import BeautifulSoup
from nltk.tokenize import RegexpTokenizer
from nltk.stem.porter import *

def createInvertedIndex(_documentSet):
    _invertedIndex = defaultdict({"freq": 1, "list":[], "bold":[], "title":[], "header":{"h1":[], "h2":[],"h3":[]}})
    #                            Frequency | DocIDs In | In Bolded | In Title | In Header  <Header it is in>    |
    #                                                  |In Theory these should be a lot smaller                 |
    _docID = 0
    for _document in _documentSet:
        _docID += 1
        _tokenDict = tokenize(_document)
        for _tokenWord in _tokenDict:
            if _tokenWord in _invertedIndex:
                _invertedIndex[_tokenWord]["freq"] += 1     #Add Frequency
            else:
                _invertedIndex[_tokenWord]      #Add to Dict
            _invertedIndex[_tokenWord]["list"].append(_docID)       #Add DocID (Base List)
            if _tokenWord["bold"]:                  #Is the word in bold in this document?
                _invertedIndex[_tokenWord]["bold"].append(_docID)   #Add DocID (Bold List)
            if _tokenWord["title"]:               #Is the word in the title in this document?
                _invertedIndex[_tokenWord]["title"].append(_docID)  #Add DocID (Title List)
            if len(_tokenWord["header"]) != 0:    #Is the word in the header in this document?
                for _header in _tokenWord["header"]:
                    _invertedIndex[_tokenWord][_header].append(_docID) #Add DocID (Header Dict)
    return _invertedIndex

def tokenize(_document):
    _soup = BeautifulSoup(_document, 'html.parser')
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
    return _tokenDict