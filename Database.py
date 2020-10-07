from datetime import datetime
from Scrapping import getStocksData
import json

#get current time
time = datetime.now().strftime("%H:%M:%S").split(":")
hour = time[0]
minute = time[1]
second = time[2]


stocks = getStocksData()

# connect to firebase
from firebase import firebase
db_url = "https://somsriversion2.firebaseio.com/"
firebase = firebase.FirebaseApplication(db_url, None)

#convert class to dictionary
def addToDatabase():
    for stock in stocks:
        stock_dict = stock.__dict__
        print("Adding {} data".format(stock_dict.get('name')))
        table_name = "/stocks_data/{}".format(stock_dict.get('name'))
        result = firebase.post(table_name, stock_dict)

if __name__ == "__main__":
    if int(hour) >= 16 and int(minute) >= 0 and int(second) >= 0:
        print("Stock market closed, please comeback tomorrow")
    else: addToDatabase()