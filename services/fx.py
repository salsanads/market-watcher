import aiohttp

BASE_API = "https://open.er-api.com/v6/latest/{currency}"


async def fetch_rate(session, url):
    async with session.get(url, timeout=10) as r:
        data = await r.json()

    if data.get("result") != "success":
        raise Exception("Failed to fetch FX data")

    return data["rates"]["IDR"]


async def get_idr_rates(currencies):
    rates = {}
    async with aiohttp.ClientSession() as session:
        for currency in currencies:
            value = await fetch_rate(session, BASE_API.format(currency=currency))
            rates[currency] = value

    return rates
