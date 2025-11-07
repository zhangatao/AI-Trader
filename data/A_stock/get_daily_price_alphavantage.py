import os

import requests
from dotenv import load_dotenv

load_dotenv()
import json

sse_50_codes = [
    "600519.SHH",
    "601318.SHH",
    "600036.SHH",
    "601899.SHH",
    "600900.SHH",
    "601166.SHH",
    "600276.SHH",
    "600030.SHH",
    "603259.SHH",
    "688981.SHH",
    "688256.SHH",
    "601398.SHH",
    "688041.SHH",
    "601211.SHH",
    "601288.SHH",
    "601328.SHH",
    "688008.SHH",
    "600887.SHH",
    "600150.SHH",
    "601816.SHH",
    "601127.SHH",
    "600031.SHH",
    "688012.SHH",
    "603501.SHH",
    "601088.SHH",
    "600309.SHH",
    "601601.SHH",
    "601668.SHH",
    "603993.SHH",
    "601012.SHH",
    "601728.SHH",
    "600690.SHH",
    "600809.SHH",
    "600941.SHH",
    "600406.SHH",
    "601857.SHH",
    "601766.SHH",
    "601919.SHH",
    "600050.SHH",
    "600760.SHH",
    "601225.SHH",
    "600028.SHH",
    "601988.SHH",
    "688111.SHH",
    "601985.SHH",
    "601888.SHH",
    "601628.SHH",
    "601600.SHH",
    "601658.SHH",
    "600048.SHH"
]


def get_daily_price(SYMBOL: str):
    FUNCTION = "TIME_SERIES_DAILY"
    OUTPUTSIZE = "compact"
    APIKEY = os.getenv("ALPHAADVANTAGE_API_KEY")
    url = (
        f"https://www.alphavantage.co/query?function={FUNCTION}&symbol={SYMBOL}&outputsize={OUTPUTSIZE}&apikey={APIKEY}"
    )
    r = requests.get(url)
    data = r.json()
    print(data)
    if data.get("Note") is not None or data.get("Information") is not None:
        print(f"Error")
        exit()
        return
    with open(f"./A_stock_data/daily_prices_{SYMBOL}.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
    if SYMBOL == "000016.SHH":
        with open(f"./A_stock_data/Adaily_prices_{SYMBOL}.json", "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)


if __name__ == "__main__":
    for symbol in sse_50_codes:
        get_daily_price(symbol)
    get_daily_price("000016.SHH")
