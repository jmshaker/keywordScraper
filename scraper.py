import requests
import re
from sqlalchemy import create_engine
from bs4 import BeautifulSoup

db_connect = create_engine('sqlite:///test.db')

words = []

baseAddress = "https://en.oxforddictionaries.com/definition/"

def DB_getWords():

    conn = db_connect.connect()

    query = conn.execute("select WORD from keywords")

    words = [i[0] for i in query.cursor.fetchall()]

    dictionary_definitionScraper(words)

def dictionary_definitionScraper(words):

    wordTypes = [] 
    wordDefs = []

    for i in range(0, words.__len__()):

        link = baseAddress + words[i]
        
        source_code = requests.get(link)
        
        plaintext = source_code.text

        soup = BeautifulSoup(plaintext)

        try:
            wordDef = soup.find("span", class_="ind")

            wordDef = wordDef.get_text()
        except:

            wordDef = ""
        
        wordDefs.append(wordDef)

        try:
            wordType = soup.find("span", class_="sense-registers")

            wordType = wordType.get_text()

        except:

            wordType = ""

        wordTypes.append(wordType)

    dictionary_addDefinitionsDB(words, wordTypes, wordDefs)

        
def dictionary_addDefinitionsDB(words, wordTypes, wordDefs):

    conn = db_connect.connect()

    for i in range(0, words.__len__()):

        conn.execute("UPDATE KEYWORDS SET TYPE = \"%s\", DEFINITION = \"%s\" WHERE WORD = \"%s\";" %(wordTypes[i], wordDefs[i], words[i]))
            
DB_getWords()