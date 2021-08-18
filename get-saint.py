import requests
from pymongo import MongoClient
import json
import numpy as np

hostname = ''
client = MongoClient(hostname)
dbname = ''
db = client[dbname]
lng = 'fr'
tMonth = 1

def checkDate(i) :
    if i < 10:
        return '0' + str(i)
    return str(i)

def getDay() :
    global tMonth
    if tMonth == 2:
        return 29
    if tMonth < 8:
        if tMonth % 2 != 0:
            print(tMonth, tMonth % 2)
            return  31
        return 30
    elif tMonth > 7:
        if tMonth % 2 != 0:
            return  30
        return 31
  
while tMonth < 13:
    days = getDay()
    for i in range(0, days):
        page = requests.get('https://www.vaticannews.va/'+ lng +'/saint-du-jour/'+ checkDate(tMonth) +'/'+ checkDate(i + 1) +'.saints.js')
        print(checkDate(tMonth) + "/" + checkDate(i + 1))
        res = json.loads(page.content)['saints']
        saints = db.saints
        for i2 in range(0, len(res)):
            saint = {
                "date": checkDate(tMonth) + "/" + checkDate(i + 1),
                "lng":lng,
                "name": res[i2]['name'],
            }
          
            text = res[i2].get('text')
            summary = res[i2].get('summary')
            if text:
             saint['text'] = res[i2]['text']
            if summary: 
             saint['summary'] = res[i2]['summary']
            saint_id = saints.insert_one(saint)
    tMonth+=1



