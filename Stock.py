class Stock:
    
    def __init__(self, date, time, name, _open, high, low, current, change, per_change, buy, sell, volumn, price):
        self.date = date
        self.time = time
        self.name = name
        self.open = _open
        self.high = high    
        self.low = low
        self.current = current
        self.change = change
        self.percent_change = per_change
        self.buy = buy
        self.sell = sell 
        self.volumn = volumn
        self.price = price

if __name__ == "__main__":
    pass