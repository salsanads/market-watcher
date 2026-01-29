from aiohttp import web
import os
import asyncio

PORT = int(os.getenv("PORT", 10000))  # Render sets $PORT automatically

async def handle(request):
    return web.Response(text="Bot is running!")

def start_web_server():
    app = web.Application()
    app.router.add_get("/", handle)
    # Run in the background
    asyncio.create_task(web._run_app(app, port=PORT))
