# PrepareSpells

A Python desktop companion for managing tabletop role-playing spells and inventory.

## Features

- Create and remove spells, or look up spell descriptions through the D&D 5e API.
- Track spell slots and restore saved maximum slots after a rest.
- Track hit points, temporary hit points and damage.
- Manage inventory quantities and save spells and inventory to JSON presets.

## Run locally

Requires Python 3, Requests, and a compatible PySimpleGUI installation with a working desktop/Tk environment.

```sh
python -m venv .venv
# Activate the virtual environment using your platform's instructions.
python -m pip install -r requirements.txt
python MainApp.py
```

PySimpleGUI compatibility has not been pinned or verified across platforms. If the installed distribution does not expose the expected GUI API, use a compatible installation before launching; the automated tests below do not validate the desktop dependency.

Choose `preset.json` in the opening file picker to try the included sample, or cancel to start with empty lists. Use **Save As** to save spells and inventory. Hit points and spell-slot settings are session state and are not included in presets.

## Structure

| File | Purpose |
| --- | --- |
| `MainApp.py` | Application entry point |
| `Functions.py` | Models, dialogs, inventory and spell API integration |
| `preset.json` | Example spell and inventory data |
| `tests/` | Regression tests using mocked GUI and HTTP modules |

## Checks

```sh
python -m unittest discover -s tests -v
python -m compileall -q MainApp.py Functions.py tests
```

Tests run without a display, network access or third-party dependencies. Manually check the GUI when changing dialogs. API lookup requires an internet connection; this project does not implement the complete game rules or character progression.
