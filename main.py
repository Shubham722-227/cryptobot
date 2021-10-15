import requests
import json


class CryptoBot:
    def __init__(self, pair):
        self.pair = pair
        self.coin = 0
        self.crypto_data = self.load_crypto_data()
        self.trades = self.load_trades()

    def save_crypto_data(self, data):
        with open('data.json', 'w') as f:
            json.dump(data, f, indent=4)

    def load_crypto_data(self):
        data = {}
        try:
            with open('data.json', 'r') as f:
                data = json.load(f)
                data = data[self.pair]
        except:
            data = self.make_crypto_data(data)
            self.save_crypto_data(data)
            data = data[self.pair]
        self.coin = data.get("coins")
        return data

    def make_crypto_data(self, data):
        data[self.pair] = {
            'high': [],
            'low': [],
            'close': [],
            'prices': [],
            'coins': 0.0
        }
        return data

    def load_trades(self):
        trades = {}
        try:
            with open('trades.json', 'r') as f:
                trades = json.load(f)
                trades = trades[self.pair]
        except:
            trades[self.pair] = []
            self.save_trade_data(trades)
            trades = trades[self.pair]
        return trades

    def save_trade_data(self, data):
        with open('trades.json', 'w') as f:
            json.dump(data, f, indent=4)


if __name__ == "__main__":
    btc = CryptoBot("I-BTC_INR")
    print(btc.crypto_data, btc.trades)

    zil = CryptoBot("zil")
    print(zil.crypto_data, zil.trades)
