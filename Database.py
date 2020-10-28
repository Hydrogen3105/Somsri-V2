from datetime import datetime
from Scrapping import getStockData, isMarketOpen
import json

# connect to firebase
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from Visualization import plot_upload_data


cred = credentials.Certificate('./somsriversion2-firebase-adminsdk.json') 
if not firebase_admin._apps:
    default_app = firebase_admin.initialize_app(cred)

#default_app = firebase_admin.initialize_app(cred)
db = firestore.client()
    

#stock name
stocks_name = ['ADVANC','AOT','AWC','BBL','BDMS','BEM','BGRIM','BH','BJC','BPP',
                'BTS','CBG','CPALL','CPF','CPN','CRC','DTAC','EA','EGCO','GLOBAL',
                'GPSC','GULF','HMPRO','INTUCH','IRPC','IVL','KBANK','KTB','KTC','LH',
                'MINT','MTC','OSP','PTT','PTTEP','PTTGC','RATCH','SAWAD','SCB','SCC',
                'TCAP','TISCO','TMB','TOA','TOP','TRUE','TTW','TU','VGI','WHA',]

#get current time
def getCurrentTime():
    time = datetime.now().strftime("%H:%M:%S").split(":")
    return time

def addToDatabase(stock_name):
    #get stock data from Scrapping.py

    if stock_name in stocks_name:
        if isMarketOpen(stock_name):
            print('Adding {} to database'.format(stock_name))
            stock_data = getStockData(stock_name)
            time_doc = stock_data['time'].split(':')[0]+ ":" + stock_data['time'].split(':')[1]
            doc_name = stock_data['date']+ '/time/' + time_doc

            db.collection(stock_data['name']).document(doc_name).set(stock_data)
            print('Completed Adding {} data'.format(stock_name))
            #plot_upload_data(stock_name)
        else: print('Market is still Closed')
    else: print('It is not in SET50')

def addAllToDatabase():
    #get all stocks data from Scrapping.py
    for stock_name in stocks_name:
        addToDatabase(stock_name)
    for stock_name in stocks_name:
        plot_upload_data(stock_name)

        

if __name__ == "__main__":
    while(1):
        time = getCurrentTime()
        hour = int(time[0])
        minute = int(time[1])
        second = int(time[2])
        
        if (hour >= 17) or (hour <= 9) :
            print("Stock market closed, please comeback tomorrow")
        elif (minute % 2 == 0 and second == 0):
            print(time)
            print("Start Adding to database")
            addAllToDatabase()
            print("Completed Adding to database")
        
            