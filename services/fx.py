import aiohttp

BASE_API = "https://open.er-api.com/v6/latest/{currency}"


async def fetch_rate(session, base_currency, url):
    async with session.get(url, timeout=10) as r:
        data = await r.json()

    if data.get("result") != "success":
        raise Exception("Failed to fetch FX data")

    return data["rates"][base_currency]


async def get_rates(base_currency, currencies):
    rates = {}
    async with aiohttp.ClientSession() as session:
        for currency in currencies:
            value = await fetch_rate(session, base_currency, BASE_API.format(currency=currency))
            rates[currency] = value

    return rates
