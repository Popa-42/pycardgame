# PyCardGame - A base library for creating card games in Python
# Copyright (C) 2025  Popa-42
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

from copy import copy

from ....src.base import Card
from ....src.presets import (
    DrawTwoCard,
    NumberCard,
    ReverseCard,
    SkipCard,
    UnoCard,
    UnoDeck,
    WildCard,
    WildDrawFourCard,
)


def test_uno_deck_init():
    deck = UnoDeck()

    assert len(deck.cards) == 108
    assert all(isinstance(card, Card) for card in deck.cards)
    assert all(isinstance(card, UnoCard) for card in deck.cards)

    assert all(isinstance(card, NumberCard) for card in deck.cards[0:76])
    assert all(isinstance(card, DrawTwoCard) for card in deck.cards[76:84])
    assert all(isinstance(card, SkipCard) for card in deck.cards[84:92])
    assert all(isinstance(card, ReverseCard) for card in deck.cards[92:100])
    assert all(isinstance(card, WildCard) for card in deck.cards[100:104])
    assert all(
        isinstance(card, WildDrawFourCard) for card in deck.cards[104:108])


def test_uno_deck_shuffle():
    deck = UnoDeck()
    original_order = copy(deck.cards)
    deck.shuffle()
    assert deck.cards != original_order
    assert len(deck.cards) == 108
    assert all(isinstance(card, UnoCard) for card in deck.cards)


def test_uno_deck_str():
    deck = UnoDeck()
    assert str(deck) == f"UNO Deck with {len(deck.cards)} cards."
    assert repr(deck) == f"UnoDeck(cards={deck.cards!r})"


def test_uno_deck_repr():
    deck = UnoDeck()
    assert repr(deck) == f"UnoDeck(cards={deck.cards!r})"
