"""Launch the spell and inventory manager."""

import Functions as functions


def main():
    """Load a preset and open the application."""
    spell_list, item_list = functions.getPreset()
    while not functions.spellWindow(spell_list, item_list):
        pass


if __name__ == "__main__":
    main()
