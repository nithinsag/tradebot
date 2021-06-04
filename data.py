import asyncio
from binance import AsyncClient, BinanceSocketManager
import matplotlib.pyplot as plt
plt.axis([0, 100, 0, 3000])

async def main():
    client = await AsyncClient.create()
    bm = BinanceSocketManager(client)
    # start any sockets here, i.e a trade socket
    ts = bm.trade_socket('ETHUSDT')
    # then start receiving messages
    async with ts as tscm:
        while True:
            res = await tscm.recv()
            print(res)
            plt.pause(0.1)

    await client.close_connection()

if __name__ == "__main__":
    plt.draw()
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())