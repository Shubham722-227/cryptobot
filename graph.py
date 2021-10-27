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

    return data, avg


def get_slope(data):
    data = np.flipud(data)
    slope = []
    last = data[0]
    for id in range(1, len(data), 10):
        m = id/(last - data[id])
        slope.append(m)
    return np.flipud(np.array(slope))


def graph(coin, time):
    i = 0
    avg = np.array([])
    while True:
        avg = np.array([])
        closing_data, avg = average(coin, avg, time)
        time_arr = np.arange(start=0, stop=len(closing_data), step=1)

        slopes = get_slope(avg)
        # plt.clf()
        # plt.plot(np.arange(start=0, stop=len(slopes), step=1), slopes)
        # plt.pause(5)
        print(slopes, "\n")
        # print(slopes[-3:])
        check = 0
        for id in range(3):
            if slopes[len(slopes)-id - 1] > 0:
                check += 1
        if check == 3:
            print("BUY\n")

        plt.clf()
        plt.plot(time_arr, closing_data)
        plt.plot(time_arr, avg, c="red", linestyle="--")
        plt.xlabel("Time")
        plt.ylabel("Closing Price")
        plt.title("Closing Price Data")
        plt.pause(5)


if __name__ == "__main__":
    time = 180
    # graph("I-BTC_INR", time)
    graph("I-MATIC_INR", time)
    # get_data("I-BTC_INR")
