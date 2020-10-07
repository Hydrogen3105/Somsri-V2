import requests
from bs4 import BeautifulSoup
from Stock import Stock
from datetime import datetime

# web scrapping data
url = "https://marketdata.set.or.th/mkt/sectorquotation.do?sector=SET50&language=th&country=TH"
resp = requests.get(url)

# prettify
soup = BeautifulSoup(resp.text, 'html.parser')
tables = soup.findAll("table",{"class":"table-info"})

#get current time
dt = datetime.now().strftime("%d/%m/%Y")
dt_time = datetime.now().strftime("%H:%M:%S")

# get data
def getStocksData():
    stocks_data = []
    for row in tables[2].findAll("tr")[1:]:
        name = row.findAll("td")[0].find("a").text.strip()
        _open = row.findAll("td")[2].text.strip()
        highest = row.findAll("td")[3].text.strip()
        lowest = row.findAll("td")[4].text.strip()
        current = row.findAll("td")[5].text.strip()
        change = row.findAll("td")[6].text.strip()
        percent_change = row.findAll("td")[7].text.strip()
        buy_offer = row.findAll("td")[8].text.strip()
        sell_offer = row.findAll("td")[9].text.strip()
        volumn = row.findAll("td")[10].text.strip()
        price  = row.findAll("td")[11].text.strip()

        stock_data = Stock(dt, dt_time, name, _open, highest, lowest, current, change, percent_change, buy_offer, sell_offer, volumn, price)
        stocks_data.append(stock_data)
    return stocks_data

if __name__ == "__main__":
    pass