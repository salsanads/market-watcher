import aiohttp

USD_API = "https://open.er-api.com/v6/latest/USD"
SGD_API = "https://open.er-api.com/v6/latest/SGD"


async def fetch_rate(session, url):
    async with session.get(url, timeout=10) as r:
        data = await r.json()

    if data.get("result") != "success":
        raise Exception("Failed to fetch FX data")

    return data["rates"]["IDR"]


async def get_idr_rates():
    async with aiohttp.ClientSession() as session:
        usd_idr = await fetch_rate(session, USD_API)
        sgd_idr = await fetch_rate(session, SGD_API)

    return {
        "USD": usd_idr,  # 1 USD = X IDR
        "SGD": sgd_idr   # 1 SGD = X IDR
    }