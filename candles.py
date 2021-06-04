from binance.client import Client
import matplotlib.pyplot as plt
import pandas as pd
import mplfinance as fplt
import matplotlib.dates as mpl_dates
import pandas as pd
client = Client('HZ3AN1L9gmhplgZ2j2catnI3jUZqmAbTxiHZtNzcPkIWhydNRF1M03OeHIzIzgv9',
                '2jZht4qtaJM43wXHBQfgYHcU7iFyIt8jF7TltnfH1JyfTECwoBUk49NYsq62dbje', testnet=True)
candles = client.get_klines(
    symbol='ETHUSDT', interval=Client.KLINE_INTERVAL_30MINUTE)
print(candles)
fplt.plot(
    apple_df,
    type='candle',
    title='ETHUSDT, March - 2020',
    ylabel='Price ($)'
)
