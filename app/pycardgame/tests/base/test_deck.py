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

from typing import Literal

import pytest

from ... import CardMeta, DeckMeta, GenericCard, GenericDeck

T_Ranks = Literal["7", "8", "9", "10", "J", "Q", "K", "A"]
T_Suits = Literal["Diamonds", "Hearts", "Spades", "Clubs"]


class DummyCard(
    GenericCard[T_Ranks, T_Suits],
    metaclass=CardMeta,
    rank_type=T_Ranks,
    suit_type=T_Suits
):
    ...


class DummyDeck(
    GenericDeck[DummyCard],
    metaclass=DeckMeta,
    card_type=DummyCard
):
    ...


def test_deck_init():
    deck1 = DummyDeck()
    assert len(deck1.cards) == 32
    assert all(isinstance(card, DummyCard) for card in deck1)

    cards = [DummyCard(0, 0)]
    deck2 = DummyDeck(cards)
    assert deck2.cards == cards


def test_deck_count():
    deck = DummyDeck()
    assert deck.count(DummyCard(0, 0)) == 1
    assert deck.count("7") == 4
    assert deck.count("Diamonds") == 8

    with pytest.raises(ValueError):
        deck.count("InvalidName")

    with pytest.raises(TypeError):
        deck.count(DummyCard(0, 0).rank)


def test_deck_sort():
    deck = DummyDeck().shuffle()
    deck.sort(by="rank")
    assert deck.cards == sorted(deck.cards, key=lambda c: (
        not c.trump, c.rank if c.rank is not None else -1,
        c.suit if c.suit is not None else -1))

    deck.sort(by="suit")
    assert deck.cards == sorted(deck.cards)

    with pytest.raises(ValueError):
        deck.sort(by="invalid_key")  # type: ignore


def test_deck_shuffle():
    deck = DummyDeck().shuffle()
    assert deck.cards != sorted(deck.cards)


def test_deck_draw():
    deck = DummyDeck()
    cards = deck.draw(5)
    assert len(cards) == 5
    assert len(deck.cards) == 27

    cards = deck.draw()
    assert len(cards) == 1
    assert len(deck.cards) == 26


def test_deck_add():
    deck = DummyDeck()
    cards = [DummyCard(0, 0), DummyCard(1, 1)]
    deck.add(*cards)
    assert deck.cards[-1] == cards[-1]


def test_deck_remove():
    deck = DummyDeck()
    card = DummyCard(0, 0)
    deck.remove(card)
    assert card not in deck.cards

    with pytest.raises(ValueError):
        deck.remove(DummyCard(10, 10))


def test_deck_get_index():
    deck = DummyDeck()
    card = DummyCard(0, 0)
    assert deck.get_index(card) == [0]

    with pytest.raises(ValueError):
        deck.get_index(DummyCard(10, 10))

    with pytest.raises(TypeError):
        deck.get_index("Ace of Diamonds")  # type: ignore


def test_deck_get_cards():
    deck = DummyDeck()
    assert deck.get_cards() == deck.cards


def test_deck_get_top_card():
    deck = DummyDeck()
    assert deck.get_top_card() == deck.cards[0]


def test_deck_str():
    deck = DummyDeck()
    assert str(deck) == "Deck of 32 cards. Top card: 7 of Diamonds"


def test_deck_repr():
    deck = DummyDeck()
    deck_repr = repr(deck)
    assert deck_repr.startswith("DummyDeck(card_type=<class")
    assert "cards=[DummyCard(rank=0, suit=0)," in deck_repr
    assert deck_repr.endswith("DummyCard(rank=7, suit=3)])")


def test_deck_copy():
    deck1 = DummyDeck()
    deck2 = deck1.__copy__()
    assert deck1 is not deck2
    assert deck1.cards == deck2.cards
    assert deck1.cards is not deck2.cards
    assert isinstance(deck2, DummyDeck)


def test_deck_getitem():
    deck = DummyDeck()
    assert deck[0] == deck.cards[0]
    assert deck[1:-1:-1] == deck.cards[1:-1:-1]
