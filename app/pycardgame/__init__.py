"""
PyCardGame — A base library for creating card games in Python.

Overview
--------

This library provides a base for creating card games in Python. It includes
generic classes for cards, decks, games, and players, as well as a preset
UNO game with its cards and deck.

It is designed to be extended and customised for specific games.

License
-------

Copyright (C) 2025  Popa-42

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""

from .src.base import (
    CardMeta,
    DeckMeta,
    Card,
    Deck,
    Game,
    Player,
)

from .src.presets import (
    DrawTwoCard,
    NumberCard,
    ReverseCard,
    SkipCard,
    UnoCard,
    UnoDeck,
    UnoGame,
    UnoPlayer,
    WildCard,
    WildDrawFourCard,
)

__all__ = [
    "Card",
    "CardMeta",
    "Deck",
    "DeckMeta",
    "DrawTwoCard",
    "Game",
    "NumberCard",
    "Player",
    "ReverseCard",
    "SkipCard",
    "UnoCard",
    "UnoDeck",
    "UnoGame",
    "UnoPlayer",
    "WildCard",
    "WildDrawFourCard",
]

print("""
    PyCardGame  Copyright (C) 2025  Popa-42
    This program comes with ABSOLUTELY NO WARRANTY; for details type `show w'.
    This is free software, and you are welcome to redistribute it
    under certain conditions; type `show c' for details.
""")
