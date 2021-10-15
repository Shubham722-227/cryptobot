import requests
import json


class CryptoBot:
    def __init__(self, pair):
        self.pair = pair
        self.coin = 0

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
            with open('data.json', 'a') as f:
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
            'coins': 0
        }
        return data


if __name__ == "__main__":
    btc = CryptoBot("I-BTC_INR")
    btc_data = btc.load_crypto_data()
    print(btc_data)

    zil = CryptoBot("zil")
    zil_data = zil.load_crypto_data()
    print(zil_data)
