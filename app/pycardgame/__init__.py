"""
PyCardGame — A base library for creating card games in Python

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

from .src.base import GenericCard, GenericDeck, CardMeta, DeckMeta
from .src.game import GenericGame, GenericPlayer
from .src.presets import PokerCard, PokerDeck, PokerPlayer, PokerGame
# , SkatCard, SkatDeck, UnoCard, UnoDeck

__all__ = [
    "CardMeta",
    "DeckMeta",
    "GenericCard",
    "GenericDeck",
    "GenericGame",
    "GenericPlayer",
    "PokerCard",
    "PokerDeck",
    "PokerPlayer",
    "PokerGame",
]

print("""
    PyCardGame  Copyright (C) 2025  Popa-42
    This program comes with ABSOLUTELY NO WARRANTY; for details type `show w'.
    This is free software, and you are welcome to redistribute it
    under certain conditions; type `show c' for details.
""")
