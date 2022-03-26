from minswap_scraper import get_min_swap_prices
from sundae_scraper import get_sundae_swap_prices
import threading
import time
import json
import os

INTERESTED_PAIRS = ["MIN/ADA", "PAVIA/ADA", "MELD/ADA", "LQ/ADA", "WMT/ADA", "SUNDAE/ADA", "cNETA/ADA"]

while True:
    get_min_swap_prices()
    get_sundae_swap_prices()
    with open("./minswap_prices.txt", "r") as f:
        min_prices = f.read()
        min_prices = json.loads(min_prices)

    with open("./sundae_prices.txt", "r") as f:
        sundae_prices = f.read()
        sundae_prices = json.loads(sundae_prices)
    os.system("clear")
    for key in min_prices.keys():
        if key in sundae_prices.keys() and key in INTERESTED_PAIRS:
            sund = sundae_prices[key]
            mins = min_prices[key]
            diff = round(abs(float(100 / mins * sund - 100)), 1)
            print(f"{key} {diff}%")
    time.sleep(60)