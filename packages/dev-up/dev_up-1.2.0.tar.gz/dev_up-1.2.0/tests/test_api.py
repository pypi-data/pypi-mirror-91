import os
from unittest import TestCase

from dev_up import DevUpAPI, models


class TestDevUpAPI(TestCase):

    def setUp(self) -> None:
        TOKEN = os.environ['TOKEN']
        self.api = DevUpAPI(TOKEN)

    def test_make_request(self):
        result = self.api.make_request("profile.get", dict())
        self.assertIn('response', result)

    def test_profile_get(self):
        profile = self.api.profile.get()
        self.assertIsInstance(profile, models.ProfileGetResponse)

    def test_vk_get_stickers(self):
        stickers = self.api.vk.get_stickers(1)
        self.assertIsInstance(stickers, models.VkGetStickersResponse)

    def test_vk_get_apps(self):
        apps = self.api.vk.get_apps(1)
        self.assertIsInstance(apps, models.VkGetAppsResponse)

    def test_vk_get_groups(self):
        groups = self.api.vk.get_groups(1)
        self.assertIsInstance(groups, models.VkGetGroupsResponse)





