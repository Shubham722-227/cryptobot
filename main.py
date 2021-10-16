from numpy.core.records import array
import requests
import json
import time
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

class CryptoBot:
    def __init__(self, pair):
        self.pair = pair
        self.coin = 0
        self.crypto_data = self.load_crypto_data()
        self.trades = []
        self.last_trade = None
        self.balance = 0
        self.closing_pric = []

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
                self.balance = data.get("balance")
                data = self.crypto_data = data["crypto"][self.pair]
                self.coin = data.get("coins")
                self.trades = data.get("trades")
                self.last_trade = data.get("last_trade")

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
            'last_trade': None
        }
        return data

    def get_coin_data(self):
        try:
            data = requests.get(
                f"https://public.coindcx.com/market_data/candles?pair={self.pair}&interval=1m").json()
            data = data[:2]
            data = pd.DataFrame(data)
            data = np.array(data)
            return data
        except:
            return np.array([])

    def get_trend(self):
        coin_data = self.get_coin_data()
        high_max = (np.max(coin_data, axis=0))[1]
        low_min = (np.min(coin_data, axis=0))[2]
        print(high_max, low_min, coin_data[0][4])
        self.closing_pric.append(coin_data[0][4])
        # print(self.closing_pric)
        if coin_data[0][4] > high_max:
            return "UPTREND"
        elif coin_data[0][4] < low_min:
            return "DOWNTREND"
        else:
            return "NOTREND"

    def driver(self):
        for _ in range(20):
            crypto_data = self.load_crypto_data()
            # print(self.balance)
            trend = self.get_trend()
            print(trend)
            if trend == "UPTREND":
                # Buy
                pass
            elif trend == "DOWNTREND":
                # Sell
                pass
            time.sleep(10)

    def plot_graph(self):
        x = np.arange(start = 1, stop = 21, step = 1) 
        y = self.closing_pric

        plt.plot(x,y)
        plt.savefig("plot.png")
        # plt.gcf().autofmt_xdate()
        plt.show()



if __name__ == "__main__":
    btc = CryptoBot("I-BTC_INR")
    eth = CryptoBot("I-ETH_INR")
    # print(btc.crypto_data)
    btc.driver()
    btc.plot_graph()

