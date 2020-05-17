
from nltk.tokenize import word_tokenize 
from nltk.corpus import stopwords 
from afinn import Afinn 
from textblob import Word
import json
import re
import nltk

def sentiment_analysis(text):
    afinn = Afinn()
    stop_words = set(stopwords.words('english')) 
    tokenized = word_tokenize(text.lower())
    sw_removed = [word for word in tokenized if not word in stop_words] 
    corrected = list()
    for word in sw_removed:
        corrected.append(Word(word).spellcheck()[0][0])
    sentiment = 0
    for word in corrected:
        sentiment += afinn.score(word)
    return sentiment

filehandle = open("db.json", 'r')
txt_file_path = 'processed.json'
data = {}
data["docs"] = []
json_file_path = open(txt_file_path, "w")
count = 0
while True:
    line = filehandle.readline()
    if not line:
        break
    if "text" in line:
        line = line.strip("\n")
        line = line.rstrip()
        line = line.rstrip(",")
        line_dict = json.loads(line)
        sentence = line_dict['doc']['text']
        line_dict['sentiment'] = sentiment_analysis(sentence)
        print(line_dict['sentiment'])
        data["docs"].append(line_dict)
        count += 1
        if count > 5:
            break

json.dump(data, json_file_path)
json_file_path.close()
