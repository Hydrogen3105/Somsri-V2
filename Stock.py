class Stock:
    
    def __init__(self, name, _open, high, low, current, change, per_change, buy, sell, volumn, price):
        self.name = name
        self.open = _open
        self.high = high    
        self.low = low
        self.current = current
        self.change = change
        self.percent_change = per_change
        self.buy = buy
        self.sell = sell 
        self.volum = volumn
        self.price = price