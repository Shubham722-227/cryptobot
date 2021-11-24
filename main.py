import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime as dt
from time import sleep
import requests
import json
import os


class CryptoBot:
    def __init__(self, coin, timeInterval, balance, loss_margin, profit_margin):
        self.coin = coin
        self.balance = balance
        self.timeInterval = timeInterval
        self.loss_margin = loss_margin
        self.profit_margin = profit_margin
        self.load_crypto_data()
        self.last_transaction = self.set_last_transaction()

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
            "amount": amount,
            "value": price*amount
        }
        return transaction

    def get_coin_data(self):
        data = requests.get(
            f"https://public.coindcx.com/market_data/candles?pair={self.coin}&interval=1m&limit={self.timeInterval*2}").json()
        data = pd.DataFrame(data, columns=["close"])
        data = np.array(data)
        data = data.flatten()
        return np.flipud(data)

    def get_coin_mean(self, data):
        avg = np.array([])
        for id in range(self.timeInterval):
            arr = data[id:id+self.timeInterval]
            avg = np.append(avg, np.mean(arr), axis=None)
        data = data[self.timeInterval - 1: -1]
        return avg

    def get_mean_slope(self, data):
        data = np.flipud(data)
        slope = []
        last = data[0]
        for id in range(1, len(data), 10):
            m = id/(last - data[id])
            slope.append(m)
        return np.flipud(np.array(slope))

    def check_buy(self, coin_mean_slope, coinData):
        coin_data = self.load_crypto_data()
        check = 0
        currSlope = []
        currSlope.append((coinData[-1] - coinData[-5])/5)
        currSlope.append((coinData[-5] - coinData[-10])/5)
        for id in range(3):
            if coin_mean_slope[len(coin_mean_slope)-id - 1] > 0:
                check += 1
        if check == 3 and coin_data.get("balance") > 0.0 and not self.last_transaction == "BUY" and all(slope >= 0 for slope in currSlope):
            return "BUY"
        return "IDLE"

    def check_sell(self, current_price):
        coin_data = self.load_crypto_data()
        if not len(coin_data["trades"]) > 0:
            return

        last_trade = coin_data.get("trades")[-1]
        last_price = last_trade.get("price_inr")

        stop_loss = last_price - ((self.loss_margin/100) * last_price)
        profit_margin = last_price + ((self.profit_margin/100) * last_price)
        print("\nCurrent Trade: \nStop Loss: ", stop_loss, "\nProfit Margin: ",
              profit_margin)
        if current_price <= stop_loss or current_price >= profit_margin:
            return "SELL"
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
        plt.pause(10)

    def set_last_transaction(self):
        coin_data = self.load_crypto_data()
        if not coin_data:
            return "SELL"
        if not len(coin_data["trades"]) > 0:
            return "SELL"

        last_trade = coin_data.get("trades")[-1]
        return last_trade.get("trade")

    def make_buy(self, price):
        coin_data = self.load_crypto_data()
        if not coin_data:
            return
        balance = coin_data.get("balance")
        self.last_transaction = "BUY"
        amount = float(balance/price)
        trade = self.make_trade_data(price, "BUY", amount)

        prev_trades = coin_data.get("trades")
        prev_trades.append(trade)
        coin_data["trades"] = prev_trades
        coin_data["coins"] = amount
        coin_data["balance"] = coin_data.get("balance") - balance
        print(coin_data)
        self.save_crypto_data(coin_data)

    def make_sell(self, price):
        coin_data = self.load_crypto_data()
        if not coin_data:
            return

        self.last_transaction = "SELL"
        prev_trades = coin_data.get("trades")
        amount = prev_trades[-1].get("amount")
        trade = self.make_trade_data(price, "SELL", amount)

        prev_trades.append(trade)
        coin_data["trades"] = prev_trades
        coin_data["coins"] = coin_data.get("coins") - amount
        coin_data["balance"] = coin_data.get("balance") + amount*price
        print(coin_data)
        self.save_crypto_data(coin_data)

    def driver(self):
        while True:
            coin_data = self.get_coin_data()
            coin_avg = self.get_coin_mean(coin_data)
            coin_avg_slope = self.get_mean_slope(coin_avg)
            if self.last_transaction == "SELL" and self.check_buy(coin_avg_slope, coin_data) == "BUY":
                self.make_buy(coin_data[-1])

            if self.last_transaction == "BUY" and self.check_sell(coin_data[-1]) == "SELL":
                self.make_sell(coin_data[-1])

            else:
                print("Idling at ", coin_data[-1])
            self.graph(coin_data, coin_avg)
            # sleep(10)


if __name__ == "__main__":
    print("Starting...\n")
    timeSpan = 60
    # coin = "I-BTC_INR"
    coin = "I-MATIC_INR"
    # coin = "I-MANA_INR"
    # coin = "I-SC_INR"
    # coin = "I-BAT_INR"
    # coin = "B-ZIL_BTC"
    balance = 100000.0
    bot = CryptoBot(coin=coin, timeInterval=timeSpan,
                    balance=balance, loss_margin=0.5, profit_margin=1)
    # print(bot.load_crypto_data())
    bot.driver()
