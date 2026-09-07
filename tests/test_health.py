import os
from unittest import IsolatedAsyncioTestCase
from unittest.mock import AsyncMock, patch

from app.health import healthz, start_health_server


class HealthEndpointTest(IsolatedAsyncioTestCase):
    async def test_healthz_returns_success(self):
        response = await healthz(None)

        self.assertEqual(response.status, 200)
        self.assertEqual(response.text, '{"status": "ok"}')

    async def test_server_uses_configured_port(self):
        runner = AsyncMock()
        site = AsyncMock()

        with (
            patch("app.health.web.AppRunner", return_value=runner),
            patch("app.health.web.TCPSite", return_value=site) as tcp_site,
            patch.dict(os.environ, {"HEALTH_PORT": "9090"}),
        ):
            result = await start_health_server()

        self.assertIs(result, runner)
        runner.setup.assert_awaited_once_with()
        tcp_site.assert_called_once_with(runner, host="0.0.0.0", port=9090)
        site.start.assert_awaited_once_with()
