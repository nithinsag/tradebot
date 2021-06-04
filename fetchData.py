import pytz
import dateparser
import time
from binance.client import Client
import matplotlib.pyplot as plt
import pandas as pd
import mplfinance as fplt
import matplotlib.dates as mpl_dates
import pandas as pd
from datetime import datetime, timedelta


def interval_to_milliseconds(interval):
    """Convert a Binance interval string to milliseconds
    :param interval: Binance interval string 1m, 3m, 5m, 15m, 30m, 1h, 2h, 4h, 6h, 8h, 12h, 1d, 3d, 1w
    :type interval: str
    :return:
         None if unit not one of m, h, d or w
         None if string not in correct format
         int value of interval in milliseconds
    """
    ms = None
    seconds_per_unit = {
        "m": 60,
        "h": 60 * 60,
        "d": 24 * 60 * 60,
        "w": 7 * 24 * 60 * 60
    }

    unit = interval[-1]
    if unit in seconds_per_unit:
        try:
            ms = int(interval[:-1]) * seconds_per_unit[unit] * 1000
        except ValueError:
            pass
    return ms


def date_to_milliseconds(date_str):
    """Convert UTC date to milliseconds
    If using offset strings add "UTC" to date string e.g. "now UTC", "11 hours ago UTC"
    See dateparse docs for formats http://dateparser.readthedocs.io/en/latest/
    :param date_str: date in readable format, i.e. "January 01, 2018", "11 hours ago UTC", "now UTC"
    :type date_str: str
    """
    # get epoch value in UTC
    epoch = datetime.utcfromtimestamp(0).replace(tzinfo=pytz.utc)
    # parse our date string
    d = dateparser.parse(date_str)
    # if the date is not timezone aware apply UTC timezone
    if d.tzinfo is None or d.tzinfo.utcoffset(d) is None:
        d = d.replace(tzinfo=pytz.utc)

    # return the difference in time
    return int((d - epoch).total_seconds() * 1000.0)


if __name__ == "__main__":
    yesterday = datetime.today() - timedelta(days=10)
    symbol = "ETHUSDT"
    start_str = "2 weeks ago UTC"
    end_str = "1 hour ago UTC"
    # df = get_historical_klines('BTCUSDT', Client.KLINE_INTERVAL_15MINUTE,
    #    "2 day ago", "5 minutes ago")
    client = Client('HZ3AN1L9gmhplgZ2j2catnI3jUZqmAbTxiHZtNzcPkIWhydNRF1M03OeHIzIzgv9',
                    '2jZht4qtaJM43wXHBQfgYHcU7iFyIt8jF7TltnfH1JyfTECwoBUk49NYsq62dbje')

    out = client.get_historical_klines(symbol, Client.KLINE_INTERVAL_15MINUTE, date_to_milliseconds(
        start_str), date_to_milliseconds(end_str))
    df = pd.DataFrame(out)
    df.columns = ['Opentime', 'Open', 'High', 'Low', 'Close', 'Volume', 'Closetime',
                  'Quote asset volume', 'Number of trades', 'Taker by base', 'Taker buy quote', 'Ignore']
    df.reset_index(drop=True, inplace=True)
    df = df.set_index(pd.DatetimeIndex(
        pd.to_datetime(df['Opentime'], unit='ms')))
    df = df.drop('Opentime', axis=1)
    print(df.head())
    df.to_csv("./{}_{}_{}.csv".format(symbol,
              start_str.replace(" ", "_"),  end_str.replace(" ", "_")))
