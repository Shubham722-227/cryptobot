import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime as dt
from pprint import pprint
import requests
import json
import os


class CryptoBot:
    def __init__(self, coin, time_interval, balance):
        self.coin = coin
        self.balance = balance
        self.time = time_interval
        self.last_transaction = None

    def save_crypto_data(self, data):
        '''
        Saves the data in respective coin.
        If the file doesn't exist, it creates and fills with default data.
        Updates new data of coin
        '''
        # If file not found, creates file and enters default value
        if not os.path.exists('data.json'):
            with open('data.json', 'w') as f:
                empty_data = {}
                json.dump(empty_data, f, indent=4)

        with open('data.json', 'r+') as f:
            all_data = json.load(f)
            if self.coin in all_data:
                all_data[self.coin] = data
            else:
                all_data.update(data)
            f.seek(0)
            json.dump(all_data, f, indent=4)

    def load_crypto_data(self):
        '''
        Loads the data for a coin.
        If not found, it generates a new one for it.
        '''

        if os.path.exists('data.json'):
            with open('data.json', 'r') as f:
                data = json.load(f)
                if self.coin in data:
                    data = data[self.coin]
                else:
                    data = self.make_crypto_data()
                    self.save_crypto_data(data)
        else:
            data = self.make_crypto_data()
            self.save_crypto_data(data)
        return data

    def make_crypto_data(self):
        '''
        Generates new data for new crypto coin
        '''
        data = {}
        data[self.coin] = {
            'trades': [],
            'balance': self.balance,
            'coins': 0.0,
        }
        return data

    def make_trade_data(self, price, trade, amount):
        transaction = {
            "time-stamp": str(dt.now()),
            "price_inr": price,
            "trade": trade,
            "amount": amount
        }
        return transaction

    def get_coin_data(self):
        data = requests.get(
            f"https://public.coindcx.com/market_data/candles?pair={self.coin}&interval=1m&limit={self.time*2}").json()
        data = pd.DataFrame(data, columns=["close"])
        data = np.array(data)
        data = data.flatten()
        return np.flipud(data)

    def get_coin_mean(self, data):
        avg = np.array([])
        for id in range(self.time):
            arr = data[id:id+self.time]
            avg = np.append(avg, np.mean(arr), axis=None)
        data = data[time-1:-1]
        return avg

    def get_mean_slope(self, data):
        data = np.flipud(data)
        slope = []
        last = data[0]
        for id in range(1, len(data), 10):
            m = id/(last - data[id])
            slope.append(m)
        return np.flipud(np.array(slope))

    def check_buy(self, coin_mean_slope):
        check = 0
        for id in range(3):
            if coin_mean_slope[len(coin_mean_slope)-id - 1] > 0:
                check += 1
        if check == 3:
            return "BUY"
        return "IDLE"

    def graph(self, price_data, mean_data):
        plt.clf()
        plt.plot(np.arange(start=0, stop=len(
            price_data), step=1), price_data)
        plt.plot(np.arange(start=0, stop=len(mean_data)*2, step=2),
                 mean_data, c="red", linestyle="--")
        plt.xlabel("Time")
        plt.ylabel("Closing Price")
        plt.title("Closing Price Data")
        plt.pause(5)

    def make_buy(self, price):
        coin_data = self.load_crypto_data()

        self.balance = coin_data.get("balance")
        amount = self.balance/price
        trade = self.make_trade_data(price, "BUY", amount)

        prev_trades = coin_data.get("trades")
        prev_trades.append(trade)
        coin_data["trades"] = prev_trades
        coin_data["coins"] = amount
        coin_data["balance"] = coin_data.get("balance") - self.balance
        print(coin_data)

    def driver(self):
        while True:
            coin_data = self.get_coin_data()
            coin_avg = self.get_coin_mean(coin_data)
            coin_avg_slope = self.get_mean_slope(coin_avg)
            current_state = self.check_buy(coin_avg_slope)
            if current_state == "BUY":
                self.make_buy(coin_data[-1])
            print(current_state)
            self.graph(coin_data, coin_avg)


if __name__ == "__main__":
    print("Starting...\n")
    time = 120
    # coin = "I-BTC_INR"
    # coin = "I-MATIC_INR"
    coin = "I-MANA_INR"
    balance = 1000.0
    bot = CryptoBot(coin, time, balance)
    # print(bot.load_crypto_data())
    bot.driver()
