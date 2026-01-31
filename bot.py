import asyncio
import os
import discord
import pytz
from datetime import datetime
from dotenv import load_dotenv

from services.fx import get_rates
from services.stocks import get_stocks
from services.commodities import get_commodities

load_dotenv()

TOKEN = os.getenv("DISCORD_TOKEN", "").strip()
CHANNEL_ID = os.getenv("DISCORD_CHANNEL_ID", "").strip()
if not TOKEN or not CHANNEL_ID:
    raise ValueError("DISCORD_TOKEN and DISCORD_CHANNEL_ID must be set")
CHANNEL_ID = int(CHANNEL_ID)

BASE_CURRENCY = os.getenv("BASE_CURRENCY", "").strip()
if not BASE_CURRENCY:
    BASE_CURRENCY = "IDR"

CURRENCIES = os.getenv("CURRENCIES", "").strip()
if not CURRENCIES:
    CURRENCIES = "USD,SGD,MYR,AUD,EUR,GBP"
CURRENCIES = [c.strip() for c in CURRENCIES.split(",") if c.strip()]

SYMBOLS = os.getenv("SYMBOLS", "").strip()
if not SYMBOLS:
    SYMBOLS = "^JKSE,^GSPC"
SYMBOLS = [s.strip() for s in SYMBOLS.split(",") if s.strip()]

goods_env = os.getenv("GOODS", "").strip()
if not goods_env:
    goods_env = "Gold:GC=F,Silver:SI=F"
GOODS = dict(
    item.strip().split(":")
    for item in goods_env.split(",") if item.strip()
)

TIMEZONE = os.getenv("TIMEZONE", "").strip()
if not TIMEZONE:
    TIMEZONE = "Asia/Jakarta"
TZ = pytz.timezone(TIMEZONE)

intents = discord.Intents.default()
client = discord.Client(intents=intents)


async def send_market_update():
    channel = await client.fetch_channel(CHANNEL_ID)
    if channel is None:
        print("Channel not found")
        return

    try:
        fx = await get_rates(BASE_CURRENCY, CURRENCIES)
        stocks = await get_stocks(SYMBOLS)
        commodities = await get_commodities(GOODS.values(), BASE_CURRENCY)

        now = datetime.now(TZ)
        date_str = now.strftime("%A, %d %B %Y")

        # Build Discord message
        message = f"**📊 Daily Market Update\n{date_str}**\n\n"
        message += f"**💱 FX Rates**\n"

        for currency in CURRENCIES:
            message += f"1 {currency} = {fx[currency]:,.2f} {BASE_CURRENCY}\n"
        message += "\n"
        
        message += f"**📈 Stocks**\n"
        for symbol in SYMBOLS:
            if stocks[symbol]["price"] is None:
                message += f"{symbol}: N/A\n"
            else:
                message += f"{symbol}: {stocks[symbol]['price']:,.2f}\n"
        message += "\n"

        message += f"**⛏️ Commodities**\n"
        for good_name in GOODS:
            good_code = GOODS[good_name]
            if commodities[good_code]["price"] is None:
                message += f"{good_name}: N/A\n"
            else:
                message += f"{good_name}: {commodities[good_code]['price']:,.2f} {BASE_CURRENCY}\n"

        await channel.send(message)

    except Exception as e:
        print("Failed to fetch or send market data:", e)


async def main():
    await client.login(TOKEN)
    await send_market_update()
    await client.close()

asyncio.run(main())
