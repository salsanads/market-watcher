import yfinance as yf
import asyncio

async def get_stock_price(symbol: str):
    def fetch():
        stock = yf.Ticker(symbol)
        hist = stock.history(period="1d")
        if hist.empty:
            return {"symbol": symbol, "price": None, "change": None}
        last_close = hist["Close"].iloc[-1]
        open_price = hist["Open"].iloc[-1]
        change_percent = ((last_close - open_price) / open_price) * 100
        return {"symbol": symbol, "price": last_close, "change": change_percent}

    return await asyncio.to_thread(fetch)


async def get_stocks(symbols):
    stocks = {}
    for symbol in symbols:
        stock = await get_stock_price(symbol)
        stocks[symbol] = stock
    return stocks
