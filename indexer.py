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
            if _tokenWord["header"] != "none":    #Is the word in the header in this document?
                _invertedIndex[_tokenWord][_tokenWord["header"]].append(_docID) #Add DocID (Header Dict)
    return _invertedIndex

def tokenize(_document):
    _soup = BeautifulSoup(_document, 'html.parser')
    _htmlText = _soup.get_text()
    _tokenList = list()
    _stemmer = PorterStemmer()
    _tokenDict = defaultdict({"bold": False, "title": False, "header":"none"})
    _regExp = RegexpTokenizer('[a-zA-Z]+[\'a-zA-Z]*')
    _tokenList = _regExp.tokenize(_htmlText)
    _tokenDict = [_stemmer.stem(_word) for _word in _tokenList] #Gets rid of plurals
    return _tokenDict