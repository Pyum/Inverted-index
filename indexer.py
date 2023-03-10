from collections import defaultdict
from bs4 import BeautifulSoup
from nltk.tokenize import RegexpTokenizer
from nltk.stem.porter import *
import json, os, sys, nltk, re, time

InvertedIndex = defaultdict()
LinkIndex = defaultdict()

UniqueWords = set()

def clearTxtFiles():
    for _file in "abcdefghijklmnopqrstuvwxyz":
        for _subfile in "abcdefghijklmnopqrstuvwxyz":
            open("indexes/" + _file + "/" + _subfile + ".txt", 'w').close()
    open("indexes/LinkIndex.txt", 'w').close()

def openJson():
    global LinkIndex
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
            LinkIndex[_docID] = _fileURL
            addInvertedIndex(_fileURL, _fileContent, _docID)
    return

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

def clearInvertedIndex():
    global InvertedIndex
    for _indexName, _indexValue in sorted(InvertedIndex.items(), key=lambda x:(x[1]["freq"]), reverse=True):
        if len(_indexName) == 1:
            _fileName = "indexes/"+ str(_indexName[0]) + "/0" + ".txt"
        else:
            _fileName = "indexes/" + str(_indexName[0]) + "/" + str(_indexName[1])+ ".txt"
        _file = open(_fileName, "a")
        _file.write(_indexName + ":{")
        for i in _indexValue:
            _file.write(i+":"+str(_indexValue[i]))
            if i != 'header':
                _file.write(",")
            else:
                _file.write("}")
        _file.write("\n")
        _file.close()
    InvertedIndex = defaultdict()
    return

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
    for i in _soup.findAll('strong'):
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

def getWordFromIndexes(_word): #word should have already been PorterStemmer()
    _lineNum = 0
    if len(_word) == 1:
        _fileName = "indexes/"+ str(_word[0]) + "/0" + ".txt"
    else:
        _fileName = "indexes/" + str(_word[0]) + "/" + str(_word[1])+ ".txt"
    _file = open(_fileName, "r")
    _regExp = r'(\w+):{freq:([\d]+),list:\[([\d, ]*)],bold:\[([\d, ]*)],title:\[([\d, ]*)],header:{\'h1\': \[([\d, ]*)], \'h2\': \[([\d, ]*)], \'h3\': \[([\d, ]*)]}}' #Do I ahve to escape the \ ??
    while True:
        _line = _file.readline()
        if _line == "":
            break
        _match = re.search(_regExp, _line)
        if _match.group(1) == _word:
            _bold = []
            if len(_match.group(4)) != 0:
                _bold = _match.group(4).split(', ')
            _title = []
            if len(_match.group(5)) != 0:
                _title = _match.group(5).split(', ')
            _header = {'h1':[], 'h2':[], 'h3':[]}
            if len(_match.group(6)) != 0:
                _header['h1'] = _match.group(6).split(', ')
            if len(_match.group(7)) != 0:
                _header['h2'] = _match.group(7).split(', ')
            if len(_match.group(8)) != 0:
                _header['h3'] = _match.group(8).split(', ')
            _file.close()
            return ({_match.group(1): {'freq':int(_match.group(2)), 'list':_match.group(3).split(', '), 'bold':_bold, 'title':_title, 'header':_header}}, _lineNum)
        _lineNum += 1
    _file.close()
    return ({_word: {"freq": 0, "list":[], "bold":[], "title":[], "header":{"h1":[], "h2":[],"h3":[]}}}, -1)

def intersect(_word1, _word2):
    _finalDict = defaultdict(int)
    _dictofWord1 = getWordFromIndexes(_word1)[0]
    _dictofWord2 = getWordFromIndexes(_word2)[0]
    if _dictofWord1[_word1]["freq"] < _dictofWord2[_word2]["freq"]:
        for _docID in _dictofWord1[_word1]["list"]:
                if _docID in _dictofWord2[_word2]["list"]:
                    _finalDict[int(_docID)] = 2
                    if _docID in _dictofWord2[_word2]["bold"] or _docID in _dictofWord1[_word1]["bold"]:
                        _finalDict[int(_docID)] += 15
                    if _docID in _dictofWord2[_word2]["title"] or _docID in _dictofWord1[_word1]["title"]:
                        _finalDict[int(_docID)] += 100
                    if len(_dictofWord2[_word2]["header"]) != 0:
                        _headNum = 3
                        for _header in _dictofWord2[_word2]["header"].values():
                            if _docID in _header:
                                _finalDict[int(_docID)] += (25 * _headNum)
                            _headNum -= 1
                    if len(_dictofWord1[_word1]["header"]) != 0:
                        _headNum = 3
                        for _header in _dictofWord1[_word1]["header"].values():
                            if _docID in _header:
                                _finalDict[int(_docID)] += (25 * _headNum)
                            _headNum -= 1
    else:
        for _docID in _dictofWord2[_word2]["list"]:
                if _docID in _dictofWord1[_word1]["list"]:
                    _finalDict[int(_docID)] = 2
                    if _docID in _dictofWord1[_word1]["bold"] or _docID in _dictofWord2[_word2]["bold"]:
                        _finalDict[int(_docID)] += 15
                    if _docID in _dictofWord1[_word1]["title"] or _docID in _dictofWord2[_word2]["title"]:
                        _finalDict[int(_docID)] += 100
                    if len(_dictofWord1[_word1]["header"]) != 0:
                        _headNum = 3
                        for _header in _dictofWord1[_word1]["header"].values():
                            if _docID in _header:
                                _finalDict[int(_docID)] += (25 * _headNum)
                            _headNum -= 1
                    if len(_dictofWord2[_word2]["header"]) != 0:
                        _headNum = 3
                        for _header in _dictofWord2[_word2]["header"].values():
                            if _docID in _header:
                                _finalDict[int(_docID)] += (25 * _headNum)
                            _headNum -= 1
    return _finalDict

def combineDicts(_dict1, _dict2):
    _finDict = defaultdict(int)
    if len(_dict2) == 0:
        return _dict1
    for i in _dict1.keys():
        if i in _dict2.keys():
            _finDict[i] = _dict1[i] + _dict1[i]
    return _finDict

def getlinks(_listOfDocID):
    global LinkIndex
    _finList = []
    for _docID in _listOfDocID:
        _finList.append(LinkIndex[int(_docID)])
    return _finList
    _finList = []
    for _folder in os.listdir("DEV"):
        for _file in os.listdir("DEV/" + _folder):
            _docID += 1
            if _docID in _listOfDocID:
                f = open("DEV/" + _folder + "/" + _file)
                _fileData = json.load(f)
                _finList.append(_fileData["url"])
    return _finList

def GetLinkIndexTxt():
    global LinkIndex
    _fileName = "indexes/LinkIndex.txt"
    _file = open(_fileName, "r")
    while True:
        _item = _file.readline()
        if _item == "":
            break
        _item = _item.split("->")
        LinkIndex[int(_item[0])] = _item[1].split("\n")[0]
    _file.close()

def FillLinkIndexTxt():
    global LinkIndex
    _fileName = "indexes/LinkIndex.txt"
    _file = open(_fileName, "a")
    for _docID, _link in LinkIndex.items():
        _file.write(str(_docID) + "->" + str(_link) + "\n")
    _file.close()

def main():
    global UniqueWords, InvertedIndex
    nltk.download('punkt')
    makeIndex = True #Ran on 3/5/23 @ 1:17AM Ended @ 2:52AM
    askQuery = True
    if makeIndex:
        clearTxtFiles()
        openJson()
        clearInvertedIndex()
        FillLinkIndexTxt()
        print("Indexing Complete...")
    if askQuery:
        print("Loading...")
        if not makeIndex:
            GetLinkIndexTxt()
        while True:
            _query = input("What would you like to seach for:\n")
            _startTime = time.time()
            if _query == "end":
                break
            if _query[-1] == " ":
                _query = _query[:-1]
            _setOfQueryWords = tokenizeQuery(_query)
            _listOfQueryWords = [item for item in _setOfQueryWords]
            _finDict = defaultdict(int)
            if len(_listOfQueryWords) == 1:
                _wordIndex = getWordFromIndexes(_listOfQueryWords[0])[0]
                for _docID in _wordIndex[_listOfQueryWords[0]]["list"]:
                    _finDict[_docID] = 1
                    if _docID in _wordIndex[_listOfQueryWords[0]]["bold"]:
                        _finDict[_docID] += 15
                    if _docID in _wordIndex[_listOfQueryWords[0]]["title"]:
                        _finDict[_docID] += 100
                    if len(_wordIndex[_listOfQueryWords[0]]["header"]) != 0:
                        _headNum = 3
                        for _header in _wordIndex[_listOfQueryWords[0]]["header"].values():
                            if _docID in _header:
                                _finDict[_docID] += (25 * _headNum)
                            _headNum -= 1
            while len(_listOfQueryWords) > 1:
                _word1 = _listOfQueryWords[0]
                _listOfQueryWords = _listOfQueryWords[1:]
                _dict1 = intersect(_word1, _listOfQueryWords[0])
                _finDict = combineDicts(_dict1, _finDict)
            _maxList = 5
            _finalList = []
            _searchProductFile = open("SeachProduct.txt", "w")
            for keys, value in sorted(_finDict.items(), key=lambda x:(x[1], x[-1]), reverse=True):
                _finalList.append(keys)
                _maxList -= 1
                if _maxList == 0:
                    break
            _finalList = getlinks(_finalList)
            for i in _finalList:
                _searchProductFile.write(str(i)+"\n")
             
            _endtime = time.time()
            _searchProductFile.write("\nQuery was:" + _query + "\nThe search took " +str((_endtime - _startTime)*1000) + " milliseconds")
            _searchProductFile.close()
            print('Execution time:', str((_endtime - _startTime)*1000), 'milliseconds')

    _uniqueWordsFile = open("UniqueWords.txt", "w")
    _uniqueWordsFile.write( str(len(UniqueWords)) + " words\n")
    for i in UniqueWords:
        _uniqueWordsFile.write( i + "\n")
    _uniqueWordsFile.close() 

if __name__ == '__main__':
    main()



            


