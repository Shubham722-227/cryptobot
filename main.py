import requests
import json


class CryptoBot:
    def __init__(self, pair):
        self.pair = pair
        self.coin = 90

    def save_crypto_data(self, data):
        with open('data.json', 'w') as f:
            json.dump(data, f, indent=4)

    def load_crypto_data_from_file(self):
        data = {}
        with open('data.json', 'w') as f:
            try:
                data = json.load(f)
                self.coin = int(data[self.pair]['coins'])
            except:
                data = self.make_crypto_data(data)
                self.save_crypto_data(data)
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
    print(btc.coin)
    btc.load_crypto_data_from_file()
    print(btc.coin)
