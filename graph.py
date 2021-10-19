from matplotlib import markers
from numpy.lib.function_base import append
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import requests
from pprint import pprint


def get_data(coin, time):
    data = requests.get(
        f"https://public.coindcx.com/market_data/candles?pair={coin}&interval=1m&limit={time*2}").json()
    # data = data[:120]
    data = pd.DataFrame(data, columns=["close"])
    data = np.array(data)
    data = data.flatten()
    return np.flipud(data)


def average(coin, avg, time):
    data = get_data(coin, time)

    for id in range(time):
        arr = data[id:id+time]
        avg = np.append(avg, np.mean(arr), axis=None)

    data = data[time-1:-1]

    return avg, data


def graph(coin, time):
    i = 0
    avg = np.array([])
    while True:
        avg = np.array([])
        avg, closing_data = average(coin, avg, time)
        time_arr = np.arange(start=0, stop=len(closing_data), step=1)

        i += 1
        print(i)
        plt.clf()
        plt.plot(time_arr, closing_data)
        plt.plot(time_arr, avg, c="red", linestyle="--")
        plt.xlabel("Time")
        plt.ylabel("Closing Price")
        plt.title("Closing Price Data")
        plt.pause(10)


if __name__ == "__main__":
    time = 60
    graph("I-BTC_INR", time)
    # graph("B-XTZ_BTC", time)
    # get_data("I-BTC_INR")
