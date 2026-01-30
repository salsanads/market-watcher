import yfinance as yf
import asyncio

TROY_OUNCE_IN_GRAMS = 31.1035


async def get_price(asset: str):
    def fetch():
        stock = yf.Ticker(asset)
        hist = stock.history(period="1d")
        if hist.empty:
            return {"asset": asset, "price": None}
        price_oz = hist["Close"].iloc[-1]
        price = price_oz / TROY_OUNCE_IN_GRAMS
        return {"asset": asset, "price": price}

    return await asyncio.to_thread(fetch)


async def get_commodities(assets, base_currency):
    commodities = {}
    usd_in_base = yf.Ticker(f"USD{base_currency}=X").history(period="1d")['Close'].iloc[-1]
    for asset in assets:
        commodity = await get_price(asset)
        commodity["price"] = commodity["price"] * usd_in_base
        commodities[asset] = commodity
    return commodities
