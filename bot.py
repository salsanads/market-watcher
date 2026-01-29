import os
import discord
import pytz
import asyncio
from datetime import datetime, time, timedelta
from dotenv import load_dotenv

from services.fx import get_idr_rates
from services.stocks import get_ihsg, get_stock_price
from web import start_web_server

load_dotenv()

TOKEN = os.getenv("DISCORD_TOKEN")
CHANNEL_ID = int(os.getenv("DISCORD_CHANNEL_ID"))

intents = discord.Intents.default()
client = discord.Client(intents=intents)

TZ = pytz.timezone("Asia/Singapore")  # UTC+8


async def send_market_update():
    channel = client.get_channel(CHANNEL_ID)
    if channel is None:
        print("Channel not found")
        return

    try:
        fx = await get_idr_rates()
        ihsg = await get_ihsg()

        now = datetime.now(TZ)
        date_str = now.strftime("%A, %d %B %Y")

        # Build Discord message
        message = f"**📊 Daily Market Update - {date_str}**\n\n"
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


async def scheduler():
    await client.wait_until_ready()
    while not client.is_closed():
        now = datetime.now(TZ)
        target = datetime.combine(now.date(), time(10, 0), tzinfo=TZ)
        if now >= target:
            target += timedelta(days=1)
        sleep_seconds = (target - now).total_seconds()
        await asyncio.sleep(sleep_seconds)
        await send_market_update()


@client.event
async def on_ready():
    print(f"Logged in as {client.user}")
    start_web_server()
    await send_market_update()
    client.loop.create_task(scheduler())


client.run(TOKEN)
