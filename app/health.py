import os

from aiohttp import web


async def healthz(_request: web.Request) -> web.Response:
    return web.json_response({"status": "ok"})


async def start_health_server() -> web.AppRunner:
    app = web.Application()
    app.router.add_get("/healthz", healthz)

    runner = web.AppRunner(app)
    await runner.setup()

    port = int(os.getenv("HEALTH_PORT", "8080"))
    site = web.TCPSite(runner, host="0.0.0.0", port=port)
    await site.start()

    return runner
