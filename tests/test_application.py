"""Regression tests that do not require a display or network."""
import importlib
import sys
import unittest
from unittest.mock import MagicMock, patch


class ApplicationTests(unittest.TestCase):
    def setUp(self):
        self.gui = MagicMock()
        self.http = MagicMock()
        self.http.RequestException = ConnectionError
        self.modules = patch.dict(sys.modules, {"PySimpleGUI": self.gui, "requests": self.http})
        self.modules.start()
        sys.modules.pop("Functions", None)
        sys.modules.pop("MainApp", None)
        self.functions = importlib.import_module("Functions")

    def tearDown(self):
        sys.modules.pop("Functions", None)
        sys.modules.pop("MainApp", None)
        self.modules.stop()

    def test_import_does_not_open_application(self):
        importlib.import_module("MainApp")
        self.gui.popup_get_file.assert_not_called()
        self.gui.Window.assert_not_called()

    def test_cancel_save_does_not_open_file(self):
        self.gui.popup_get_file.return_value = None
        with patch("builtins.open") as file:
            self.functions.savePreset([], [])
        file.assert_not_called()

    def test_api_connection_failure_shows_message(self):
        self.http.get.side_effect = ConnectionError
        self.assertIsNone(self.functions.apiJSONparse("fireball"))
        self.http.get.assert_called_once_with("https://www.dnd5eapi.co/api/spells/fireball", timeout=10)
        self.gui.popup.assert_called_once()

    def test_spell_without_higher_level_description(self):
        self.http.get.return_value.status_code = 200
        self.http.get.return_value.json.return_value = {
            "name": "Light", "desc": ["A light."], "level": 0,
            "ritual": False, "concentration": False,
            "duration": "1 hour", "casting_time": "1 action",
        }
        self.assertEqual(self.functions.apiJSONparse("light").name, "Light")

    def test_close_remove_dialog(self):
        window = self.gui.Window.return_value
        window.read.return_value = (self.gui.WIN_CLOSED, {})
        self.functions.removeSpell([])
        window.__getitem__.assert_not_called()
        window.close.assert_called_once()


if __name__ == "__main__":
    unittest.main()
