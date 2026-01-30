import asyncio
import os
import discord
import pytz
from datetime import datetime
from dotenv import load_dotenv

from services.fx import get_rates
from services.stocks import get_stocks

load_dotenv()

TOKEN = os.getenv("DISCORD_TOKEN")
CHANNEL_ID = int(os.getenv("DISCORD_CHANNEL_ID"))

BASE_CURRENCY = os.getenv("BASE_CURRENCY", "IDR")
CURRENCIES = os.getenv("CURRENCIES").split(",")
SYMBOLS = os.getenv("SYMBOLS").split(",")

TZ = pytz.timezone(os.getenv("TIMEZONE", "Asia/Singapore"))

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
                message += "N/A\n"
            else:
                message += f"{symbol}: {stocks[symbol]['price']:,.2f}\n"

        await channel.send(message)

    except Exception as e:
        print("Failed to fetch or send market data:", e)


async def main():
    await client.login(TOKEN)
    await send_market_update()
    await client.close()

asyncio.run(main())
