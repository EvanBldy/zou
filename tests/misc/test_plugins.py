# -*- coding: UTF-8 -*-
from tests.base import ApiTestCase


class PluginTestCase(ApiTestCase):
    """
    def test__plugin_modules(self):
        plugins = api.load_plugin_modules("tests/fixtures/plugins")
        self.assertEqual(len(plugins), 1)

        plugin = plugins[0]
        self.assertTrue(hasattr(plugin, "routes"))
    """

    """
    def test_load_plugin(self):
        plugins = api.load_plugin_modules("tests/fixtures/plugins")
        plugin = plugins[0]
        api.load_plugin(app, plugin)
        self.get("/plugins/hello")
    """
