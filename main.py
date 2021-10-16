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
        self.trades = self.load_trades()
        self.last_trade = None

    def save_crypto_data(self, data):
        all_data = {}
        with open('data.json', 'w+') as f:
            try:
                all_data = json.load(f)
            except:
                pass
            all_data[self.pair] = data
            json.dump(all_data, f, indent=4)

    def load_crypto_data(self):
        data = {}
        try:
            with open('data.json', 'r') as f:
                data = json.load(f)
                data = data[self.pair]
        except:
            with open('data.json', 'w+') as f:
                try:
                    all_data = json.load(f)
                except:
                    pass
                data = self.make_crypto_data()
                self.save_crypto_data(data)
        self.coin = data.get("coins")
        self.last_trade = data.get("last_trade")
        return data

    def make_crypto_data(self):
        data = {
            'high': [],
            'low': [],
            'close': [],
            'prices': [],
            'coins': 0.0,
            'last_trade': None
        }
        return data

    def load_trades(self):
        trades = {}
        try:
            with open('trades.json', 'r') as f:
                trades = json.load(f)
                crypto_trades = trades[self.pair]
        except:
            with open('trades.json', 'a+') as f:
                try:
                    trades = json.load(f)
                    f.seek(0)
                except:
                    pass
                trades[self.pair] = []
                json.dump(trades, f, indent=4)
            crypto_trades = trades[self.pair]
        return crypto_trades

    def save_trade_data(self, data):
        trades = {}
        with open('trades.json', 'w+') as f:
            try:
                trades = json.load(f)
                # f.seek(0)
            except:
                pass
            try:
                trades[self.pair].append(data)
            except:
                trades[self.pair] = data
            json.dump(trades, f, indent=4)

    def get_coin_data(self):
        try:
            data = requests.get(
                f"https://public.coindcx.com/market_data/candles?pair={self.pair}&interval=1m").json()
            data = data[:20]
            data = pd.DataFrame(data)
            data = np.array(data)
            return data
        except:
            return np.array([])

    def get_call(self):
        coin_data = self.get_coin_data()
        high_max = (np.max(coin_data, axis=0))[1]
        low_min = (np.min(coin_data, axis=0))[2]
        print(high_max, low_min, coin_data[0][4])
        if coin_data[0][4] > high_max:
            return "UPTREND"
        elif coin_data[0][4] < low_min:
            return "DOWNTREND"
        else:
            return "NOTREND"

    def driver(self):
        while True:
            self.trades = self.load_trades()

            call = self.get_call()
            print(call)
            time.sleep(20)


if __name__ == "__main__":
    btc = CryptoBot("I-BTC_INR")
    # print(btc.crypto_data)
    btc.driver()
