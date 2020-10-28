import json
import os
import requests
from flask import Flask, request, abort
from flask import make_response
from datetime import datetime

from Scrapping import getStockData
from Modeling import monte_simulation

# connect to firebase
import firebase_admin
from firebase_admin import credentials, storage, firestore

cred = credentials.Certificate('./somsriversion2-firebase-adminsdk.json') 
if not firebase_admin._apps:
    default_app = firebase_admin.initialize_app(cred)

#default_app = firebase_admin.initialize_app(cred)
db = firestore.client()
    
# stocks name 
stocks_name = ['ADVANC','AOT','AWC','BBL','BDMS','BEM','BGRIM','BH','BJC','BPP',
                'BTS','CBG','CPALL','CPF','CPN','CRC','DTAC','EA','EGCO','GLOBAL',
                'GPSC','GULF','HMPRO','INTUCH','IRPC','IVL','KBANK','KTB','KTC','LH',
                'MINT','MTC','OSP','PTT','PTTEP','PTTGC','RATCH','SAWAD','SCB','SCC',
                'TCAP','TISCO','TMB','TOA','TOP','TRUE','TTW','TU','VGI','WHA',]

# Flask
app = Flask(__name__)
@app.route('/', methods=['POST','GET']) 
def webhook():
    if request.method == 'POST':
        payload = request.json
        print(payload)
        reply_token = payload['events'][0]['replyToken']
        message = payload['events'][0]['message']['text']

        access_token = 'JKJje25awz+u/4WzUjSz1+oqsaGo7uU18eaE8+xhOetYBu4gxhYAzN8hECLuQ9XXXaiwdGQsd4LKYNpgm77ymDnfOW/sRwpyZ+eV29PeFW2Q1E9ryRlgvNLXuDookxSwoRkSGm4wecFdJIDaHNQUHQdB04t89/1O/w1cDnyilFU='
        list_message = message.strip().split()
        stock = ""
        reply_message = ""
        graph_url = ""
        if len(list_message) == 2 and list_message[0] == 'จำลอง':
            if list_message[1].upper() in stocks_name:
                print('Simulating')
                simulated_data = monte_simulation(list_message[1].upper(),5000)
                if simulated_data != -1:
                    reply_message = "ผลการจำลองราคาหุ้น {}\nจะพบว่าการจำลองราคาหุ้นเฉลี่ยในอีก 1 วันต่อไปมีแนวโน้มที่จะมีค่าประมาณ {:.3f}\nและมีอัตราของราคาตกลง 10 % คิดเป็น {:.3f} %".format(list_message[1].upper(),simulated_data[0],simulated_data[1] *100)
                else: 
                    reply_message = "ไม่สามารถจำลองหุ้นตัวนี้ได้ ณ ขณะนี้ หรือมีข้อมูลไม่เพียงพอ กรุณาเรียกใช้คำสั่งอีกครั้งหลังจากตลาดหุ้นปิดนะคะ"
        else:
            for word in list_message:
                if word.upper() in stocks_name:
                    stock = word.upper()
                    reply_message, url = generate_answer(stock)
                    graph_url = url

        ReplyMessage(reply_token,reply_message,access_token,graph_url)
        return request.json, 200
    else: 
        abort(400)

def ReplyMessage(Reply_token, TextMessage, Line_Access_Token, Graph_url):
    print("Replying")
    LINE_API = 'https://api.line.me/v2/bot/message/reply'
    Authorization = 'Bearer {}'.format(Line_Access_Token)
    headers = {
    'Content-Type': 'application/json; charset=UTF-8',
    'Authorization': Authorization
    }
    if TextMessage != "" and Graph_url != "":
        data = {
            "replyToken":Reply_token,
            "messages":[
                {
                    "type":"image",
                    "originalContentUrl": Graph_url,
                    "previewImageUrl": Graph_url
                },
                {
                    "type":"text",
                    "text":TextMessage
                },
                
            ]
        }
    elif TextMessage != "":
        data = {
            "replyToken":Reply_token,
            "messages":[
                {
                    "type":"text",
                    "text":TextMessage
                },
                
            ]
        }
    else: 
        TextMessage = "ไม่พบราชื่อนี้อยู่ใน SET50 กรุณากรอกชื่อย่อของหุ้นที่ถูกต้อง หรือกรุณาตรวจสอบข้อความ"
        data = {
            "replyToken":Reply_token,
            "messages":[
                {
                    "type":"text",
                    "text":TextMessage
                },
                
            ]
        }
    data = json.dumps(data)
    r = requests.post(LINE_API, headers=headers, data=data)
    return 200

def generate_answer(stock):
    answer_str = ""
    hasGraph = False
    stock_data = get_last_record_from_database(stock)
    generated_graph = get_graph_url(stock, stock_data)
    if stock_data == 0:
        stock_data = getStockData(stock)
        answer_str = """สถานะหุ้น {} ณ ขณะนี้\nราคา ณ ขณะนี้ : {} บาท\nเปลี่ยนแปลง : {}\n% เปลี่ยนแปลง : {}\nราคาปิดก่อนหน้า : {} บาท\nราคาเปิดของวันนี้ : {} บาท\nราคาสูงที่สุดของวันนี้ : {} บาท
                        \nราคาต่ำสุดของวัันนี้ : {} บาท\nราคาเฉลี่ย : {} บาท\nปริมาณซื้อขาย (หุ้น) : {} หุ้น\nมูลค่าซื้อขาย ('000 บาท) : {} \nราคาพาร์ (บาท) : {} บาท \nราคา Ceiling  : {}
                        \nราคา Floor : {}\nราคาเสนอซื้อ / ปริมาณเสนอซื้อ : {}\nราคาเสนอขาย / ปริมาณเสนอขาย : {} 
                        """ .format(stock_data["name"],stock_data["current_price"],stock_data["change_rate"],stock_data["change_percent"],stock_data["previous_close"],
                                    stock_data["open_price"],stock_data["highest"],stock_data["lowest"],stock_data["avg_price"],
                                    stock_data["volumn"],stock_data["price"],stock_data["par_price"],stock_data["ceiling_price"],
                                    stock_data["floor_price"],stock_data["buy_offer"],stock_data["sell_offer"])
    elif stock_data != 0:
        hasGraph = True
        answer_str = """สถานะหุ้น {} ณ ขณะนี้\nราคา ณ ขณะนี้ : {} บาท\nเปลี่ยนแปลง : {}\n% เปลี่ยนแปลง : {}\nราคาปิดก่อนหน้า : {} บาท\nราคาเปิดของวันนี้ : {} บาท\nราคาสูงที่สุดของวันนี้ : {} บาท
                        \nราคาต่ำสุดของวัันนี้ : {} บาท\nราคาเฉลี่ย : {} บาท\nปริมาณซื้อขาย (หุ้น) : {} หุ้น\nมูลค่าซื้อขาย ('000 บาท) : {} \nราคาพาร์ (บาท) : {} บาท \nราคา Ceiling  : {}
                        \nราคา Floor : {}\nราคาเสนอซื้อ / ปริมาณเสนอซื้อ : {}\nราคาเสนอขาย / ปริมาณเสนอขาย : {} 
                        """ .format(stock_data["name"],stock_data["current_price"],stock_data["change_rate"],stock_data["change_percent"],stock_data["previous_close"],
                                    stock_data["open_price"],stock_data["highest"],stock_data["lowest"],stock_data["avg_price"],
                                    stock_data["volumn"],stock_data["price"],stock_data["par_price"],stock_data["ceiling_price"],
                                    stock_data["floor_price"],stock_data["buy_offer"],stock_data["sell_offer"])
    else: answer_str = "ไม่พบข้อมูล ณ ขณะนี้ ขออภัยค่ะ"

    if hasGraph:
        return [answer_str, generated_graph]
    else: 
        return [answer_str, ""]

def get_graph_url(stock_name, last_data):
    date = datetime.now().strftime("%d-%m-%Y")
    last_update_time = last_data["time"]
    last_update = last_update_time.split(":")[0] + "-" + last_update_time.split(":")[1]

    file_name = 'main_{}_{}.jpg'.format(date,stock_name)
    print("Getting graph url")

    bucket_name = "somsriversion2.appspot.com"
    bucket = storage.bucket(bucket_name)
    blob = bucket.blob('graphs/main/{}_'.format(last_update) +file_name)
    print(blob.public_url)
    
    return blob.public_url


def get_last_record_from_database(stock_name):
    date = datetime.now().strftime("%d-%m-%Y")
    
    # change 22-10-2020 to date

    doc_ref = db.collection(stock_name).document(date).collection("time")
    docs = doc_ref.get()
    if(len(docs) != 0):
        return docs[len(docs) - 1].__dict__["_data"]
    else:
        return 0

def get_simulated_data(stock_name, number):
    simulated_data = monte_simulation(stock_name, number)
    return simulated_data

if __name__ == '__main__':
    app.run(debug=False)
    #get_graph_url('VGI')
    #print(get_last_record_from_database('VGI'))
