import requests
import json
import time
import numpy as np
import pandas as pd


class CryptoBot:
    def __init__(self, pair):
        self.pair = pair
        self.coin = 0
        self.crypto_data = self.load_crypto_data()
        self.trades = []
        self.last_trade = None
        self.balance = 0

    def save_crypto_data(self, data):
        '''
        Saves the data in respective coin. 
        If the file doesn't exist, it creates and fills with default data.
        Updates new data of coin
        '''

        # If file not found, creates file and enters default value
        try:
            with open('data.json', 'r') as f:
                all_data = json.load(f)
        except:
            with open('data.json', 'w') as f:
                all_data = {"balance": 0, "crypto": {}}
                json.dump(all_data, f, indent=4)

        # Enters data to specific coin
        all_data = {}
        with open('data.json', 'r') as f:
            all_data = json.load(f)

        with open('data.json', 'w') as f:
            all_data["crypto"][self.pair] = data
            json.dump(all_data, f, indent=4)

    def load_crypto_data(self):
        '''
        Loads the data for a coin. 
        If not found, it generates a new one for it. 
        '''
        data = {}
        try:
            with open('data.json', 'r') as f:
                data = json.load(f)
                self.balance = data.get("balance")/len(data.get("crypto"))
                data = self.crypto_data = data["crypto"][self.pair]
                self.coin = data.get("coins")
                self.trades = data.get("trades")
        except:
            data = self.make_crypto_data()
            self.save_crypto_data(data)
        return data

    def make_crypto_data(self):
        '''
        Generates new data for new crypto coin
        '''
        data = {
            'trades': [],
            'coins': 0.0,
            "worth": 0.0,
        }
        return data

    def get_coin_data(self):
        try:
            data = requests.get(
                f"https://public.coindcx.com/market_data/candles?pair={self.pair}&interval=1m").json()
            self.last_trade = data[0]
            data = data[1:101]
            data = pd.DataFrame(data)
            data = np.array(data)
            return data
        except:
            return np.array([])

    def get_trend(self):
        coin_data = self.get_coin_data()
        if len(coin_data):
            high_max = (np.max(coin_data, axis=0))[1]
            low_min = (np.min(coin_data, axis=0))[2]
            print(high_max, low_min, self.last_trade.get("close"))
            if self.last_trade.get("high") > high_max:
                return "UPTREND"
            elif self.last_trade.get("low") < low_min:
                return "DOWNTREND"
            else:
                return "NOTREND"

    def get_trade_data(self, trade, amount):
        '''
        Generates and saves Trade data to JSON file. 
        '''
        transaction = {
            "time-stamp": str(int(time.time())),
            "price_inr": self.last_trade.get("close"),
            "trade": trade,
            "amount": amount
        }
        print('TRADE:')
        print(json.dumps(transaction, indent=4))
        return transaction
        # self.crypto_data["trades"].append(transaction)
        # if trade == "BUY":
        #     self.crypto_data["coins"] = self.coin + \
        #         (amount/self.last_trade.get("close"))
        #     self.crypto_data["worth"] = self.crypto_data.get("worth") + amount
        #     self.balance = self.balance - amount
        # elif trade == "SELL":
        #     self.crypto_data["coins"] = self.coin - \
        #         (amount/self.last_trade.get("close"))
        #     self.crypto_data["worth"] = self.crypto_data.get(
        #         "worth") - (self.crypto_data["coins"]*self.last_trade.get("close"))
        #     self.balance = self.balance + self.crypto_data["coins"] * \
        #         self.last_trade.get("close")
        # self.save_crypto_data(self.crypto_data)

        # with open('data.json', 'r') as f:
        #     all_data = json.load(f)

        # with open('data.json', 'w') as f:
        #     all_data["balance"] = self.balance

    def set_buy_data(self, tansaction):
        pass

    def buy_crypto(self):
        transaction = self.get_trade_data("BUY", self.balance)
        self.set_buy_data(transaction)

    def sell_crypto(self):
        self.get_trade_data("SELL", 0.0)

    def driver(self):
        while True:
            crypto_data = self.load_crypto_data()
            trend = self.get_trend()
            print(trend)
            if trend == "UPTREND" and self.coin == 0.0:
                # Buy
                self.buy_crypto()
            elif trend == "DOWNTREND" and self.coin > 0.0:
                # Sell
                self.sell_crypto()
            time.sleep(20)


if __name__ == "__main__":
    btc = CryptoBot("I-BTC_INR")
    # print(btc.crypto_data)
    btc.driver()
