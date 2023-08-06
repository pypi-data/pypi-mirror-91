import asyncio
import os

from aiounittest import AsyncTestCase

from dev_up import DevUpAPI, models


class TestDevUpAPIAsync(AsyncTestCase):
    _loop = None

    @property
    def loop(self):
        if self._loop is None:
            self._loop = asyncio.get_event_loop()
        return self._loop

    def setUp(self) -> None:
        TOKEN = os.environ['TOKEN']
        self.api = DevUpAPI(TOKEN, self.loop)

    def get_event_loop(self):
        return self.loop

    async def test_make_request_async(self):
        result = await self.api.make_request_async("profile.get", dict())
        self.assertIn('response', result, 'any')

    async def test_profile_get_async(self):
        profile = await self.api.profile.get_async()
        self.assertIsInstance(profile, models.ProfileGetResponse)

    async def test_vk_get_stickers_async(self):
        stickers = await self.api.vk.get_stickers_async(1)
        self.assertIsInstance(stickers, models.VkGetStickersResponse)

    async def test_vk_get_apps_async(self):
        apps = await self.api.vk.get_apps_async(1)
        self.assertIsInstance(apps, models.VkGetAppsResponse)

    async def test_vk_get_groups_async(self):
        groups = await self.api.vk.get_groups_async(1)
        self.assertIsInstance(groups, models.VkGetGroupsResponse)
