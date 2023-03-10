Group: 
	Can We Do It?
Members:
	Brian Caballero
	Serena Trieu

Code can be ran with CMD or in Visual Studio Code
(Simple CD into the folder and run the indexer.py by itself)

To make the inverse index library:
	By default, this is set to False and will not create a new index.
	To change, open the code and change the bool on line 7:
		"MakeIndex = False" -> "MakeIndex = True"
	
	Once it is True, the next time the program is ran it shall 
	clear out the current inverted index and fill out a new one. 
	You may change the folder it searches through on line 24:
		"for _folder in os.listdir("DEV")" -> "for _folder in os.listdir("DEVTEST")"
	
	This takes about an hour and a half to go through all 55k files.
	We provides a filled index already.
	

To make a query:
	By default, this is set to True and will ask for a query.
	To change, open the code and change the bool on line 8:
		"AskQuery = True" -> "AskQuery = False"
		
	When it's True and the code is ran, the start will depend if you
	are asking it to create a new index or not.
	If you are using the provided index it will do a quick load and then
	ask the user for a query, returning the time it took to search.

To find the results of your query:
	Check the txt file named "SearchProduct"
	
To find the amount of unique words:
	Check the txt file named "UniqueWords"
	
To find the inversed library:
	1. Open Indexes
		There will be a folder for each letter of the alphabet representing
		the First letter of the word.
	2. Open a file
		There will be a txt file for each letter of the alphabet representing
		the Second letter of the word. Along with a txt file for words that
		don't have a 2nd letter (Due to PorterStemmer)