from collections import defaultdict
from nltk.stem.porter import *

def createInvertedIndex(_documentSet):
    _invertedIndex = defaultdict({"freq": 1, "list":[]})
    _docID = 0
    for _document in _documentSet:
        _docID += 1
        _tokenList = tokenize(_document)
        for _tokenWord in _tokenList:
            if _tokenWord in _invertedIndex:
                _invertedIndex[_tokenWord]["freq"] += 1
            else:
                _invertedIndex[_tokenWord]
            _invertedIndex[_tokenWord]["list"].append(_docID)
    return _invertedIndex

def tokenize(_document):
    _temptokeList = list()
    _tokenList = list()
    _stemmer = PorterStemmer()
    #_tokenDict = defaultdict({"bold": false, "title": false, "header":"none"}) #Use later?
    #TODO
    #   Make sure there are no duplicates
    #   Do not get rid of stopwords
    #   Generalize words... with a library?
    #   Do we need BeautifulSoup again?

    _tokenList = [_stemmer.stem(_word) for _word in _temptokeList] #Gets rid of plurals

    return _tokenList