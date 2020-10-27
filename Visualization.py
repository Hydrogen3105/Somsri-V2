import firebase_admin
from firebase_admin import credentials ,firestore, storage
import matplotlib.pyplot as plt
from datetime import datetime
import numpy as np
import requests

cred = credentials.Certificate('./somsriversion2-firebase-adminsdk.json') 
if not firebase_admin._apps:
    default_app = firebase_admin.initialize_app(cred)

#default_app = firebase_admin.initialize_app(cred)
db = firestore.client()

def get_data_from_database(stock_name):
    date = datetime.now().strftime("%d-%m-%Y")

    # change 22-10-2020 to date

    doc_ref = db.collection(stock_name).document(date).collection("time")
    docs = doc_ref.get()
    if(len(docs) != 0):
        return docs
    else: 
        return 0

def get_current_price_data(stock_name):
    current_price_list = []
    docs = get_data_from_database(stock_name)
    if(docs != 0):
        for doc in docs:
            current_price_list.append(float(doc.__dict__["_data"]["current_price"]))
        
        return current_price_list
    else: 
        return 0

def plot_upload_data(stock_name):
    date = datetime.now().strftime("%d-%m-%Y")

    data = get_current_price_data(stock_name)
    if(data != 0 and len(data) > 1):
        print("Plotting {}".format(stock_name))
        x = list(range(0,len(data)))
        plt.plot(x, data,'g')
        plt.xlabel("time")
        plt.ylabel("Price (Bath)")
        plt.title("{} price chart".format(stock_name))

        #linear regression
        if(len(data) < 5):
            m, b = np.polyfit(x, data, 1)
            fit_eq = []
            for i in x:
                fit_eq.append(m*i + b)
            plt.plot(x, fit_eq, 'r')

        #plt.show()
        plt.savefig("graphs/main_{}_{}.jpg".format(date,stock_name))
        file_url = upload_graph("main_{}_{}.jpg".format(date,stock_name),stock_name)

        plt.clf()
        #return file_url
    else: return ""

def plot_bar_chart(stock_name):
    data = get_current_price_data(stock_name)
    if data != 0:
        mean = np.mean(data)
        count = [0,0]
        price = ['> mean','<= mean']

        for each in data:
            if each > mean:
                count[0] += 1
            else: count[1] += 1
        
        fig = plt.figure(figsize = (10, 5)) 
        plt.bar(price,count,width= 0.5)
        plt.xlabel('Prices compared with mean')
        plt.ylabel('count')
        plt.title('number of prices each is less or more than mean')
        plt.show()

def upload_graph(file_name,stock_name):
    data = get_data_from_database(stock_name)
    bucket_name = "somsriversion2.appspot.com"
    bucket = storage.bucket(bucket_name)
    try: 
        before_last = data[-2].__dict__["_data"]["time"]
        before_last = before_last.split(":")[0] + "-" + before_last.split(":")[1]
        del_blob = bucket.blob('graphs/main/{}_'.format(before_last) +file_name)
        del_blob.delete()
    except:
        pass

    last_update = data[-1].__dict__["_data"]["time"]
    last_update = last_update.split(":")[0] + "-" + last_update.split(":")[1]

    print("Uploading {}".format(stock_name))
    blob = bucket.blob('graphs/main/{}_'.format(last_update) +file_name)
    sourcefile = 'graphs/' + file_name
    blob.upload_from_filename(sourcefile)
    blob.make_public()
    print(blob.public_url)

    return blob.public_url

if __name__ == "__main__":
    #get_current_price_data("ADVANC")
    #print(plot_upload_data(get_current_price_data("CBG")))
    #print(get_current_price_data("ADVANC"))
    #plot_bar_chart("VGI")
    pass