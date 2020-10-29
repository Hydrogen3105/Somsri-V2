import requests
from bs4 import BeautifulSoup
from datetime import datetime
import json
# stock name
stocks_name = ['ADVANC','AOT','AWC','BBL','BDMS','BEM','BGRIM','BH','BJC','BPP',
                'BTS','CBG','CPALL','CPF','CPN','CRC','DTAC','EA','EGCO','GLOBAL',
                'GPSC','GULF','HMPRO','INTUCH','IRPC','IVL','KBANK','KTB','KTC','LH',
                'MINT','MTC','OSP','PTT','PTTEP','PTTGC','RATCH','SAWAD','SCB','SCC',
                'TCAP','TISCO','TMB','TOA','TOP','TRUE','TTW','TU','VGI','WHA',]

#check market status
def isMarketOpen(stock_name):
    url = "https://www.settrade.com/C04_01_stock_quote_p1.jsp?txtSymbol={}&ssoPageId=9&selectPage=1".format(stock_name)
    resp = requests.get(url)

    soup = BeautifulSoup(resp.text, 'html.parser')
    div_status = soup.findAll("div",{"class":"flex-item text-left padding-8"})
    span_status = div_status[0].findAll("span")
    market_status = span_status[1].text.strip()

    if market_status == "Closed" or market_status == 'Intermission':
        return False
    return True

# get data
def getStockData(stock_name):
    time = datetime.now().strftime("%H:%M:%S")
    date = datetime.now().strftime("%d-%m-%Y")

    # web scrapping data
    url = "https://www.settrade.com/C04_01_stock_quote_p1.jsp?txtSymbol={}&ssoPageId=9&selectPage=1".format(stock_name)
    resp = requests.get(url)

    # prettify
    soup = BeautifulSoup(resp.text, 'html.parser')
    changes = soup.findAll("div",{"class": "col-xs-6"})
    tables = soup.findAll("table",{"class":"table table-info"})

   
    #print(changes[2].find("h1").text.strip(), changes[3].find("h1").text.strip(), changes[4].find("h1").text.strip())

    data_1 = tables[0].findAll("td")[1::2]
    data_2 = tables[1].findAll("td")[1::2]
    data_3 = tables[2].findAll("td")[1::2]
        
    name = stock_name
    current_price = changes[2].find("h1").text.strip()
    change_rate = changes[3].find("h1").text.strip()
    change_percent = changes[4].find("h1").text.strip()

    previous_close = data_1[0].text.strip()
    open_price = data_1[1].text.strip()
    highest = data_1[2].text.strip()
    lowest = data_1[3].text.strip()
    avg_price = data_1[4].text.strip()

    volumn = data_2[0].text.strip()
    price = data_2[1].text.strip()
    par_price = data_2[2].text.strip()
    ceiling_price = data_2[3].text.strip()
    floor_price = data_2[4].text.strip()

    buy_offer = data_3[0].text.strip()
    sell_offer = data_3[1].text.strip()

    stock_data = {
        "date": date,
        "time": time,
        "name": name,
        "current_price": current_price,
        "change_rate": change_rate,
        "change_percent": change_percent,
        "previous_close": previous_close,
        "open_price": open_price,
        "highest": highest,
        "lowest": lowest,
        "avg_price": avg_price,
        "volumn": volumn,
        "price": price,
        "par_price": par_price,
        "ceiling_price": ceiling_price,
        "floor_price": floor_price,
        "buy_offer" : buy_offer,
        "sell_offer": sell_offer,
    }
    return stock_data

if __name__ == "__main__":
    #print(getStockData("ADVANC"))
    pass