import asyncio
import os
import discord
import pytz
from datetime import datetime
from dotenv import load_dotenv

from services.fx import get_idr_rates
from services.stocks import get_ihsg

load_dotenv()

TOKEN = os.getenv("DISCORD_TOKEN")
CHANNEL_ID = int(os.getenv("DISCORD_CHANNEL_ID"))

intents = discord.Intents.default()
client = discord.Client(intents=intents)

TZ = pytz.timezone("Asia/Singapore")  # UTC+8


async def send_market_update():
    channel = await client.fetch_channel(CHANNEL_ID)
    if channel is None:
        print("Channel not found")
        return

    try:
        fx = await get_idr_rates()
        ihsg = await get_ihsg()

        now = datetime.now(TZ)
        date_str = now.strftime("%A, %d %B %Y")

        # Build Discord message
        message = f"**📊 Daily Market Update\n{date_str}**\n\n"
        message += f"**💱 FX Rates**\n"
        message += f"1 USD = {fx['USD']:,.0f} IDR\n"
        message += f"1 SGD = {fx['SGD']:,.0f} IDR\n\n"
        message += f"**📈 Stocks**\n"
        if ihsg["price"] is None:
            message += "N/A\n\n"
        else:
            message += f"IHSG: {ihsg['price']:,.2f}"

        await channel.send(message)

    except Exception as e:
        print("Failed to fetch or send market data:", e)


async def main():
    await client.login(TOKEN)
    await send_market_update()
    await client.close()

asyncio.run(main())
