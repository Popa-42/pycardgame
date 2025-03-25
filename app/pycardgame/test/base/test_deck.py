from typing import Literal, get_args

import pytest

from ...src.base import GenericCard, GenericDeck

ranks = Literal["7", "8", "9", "10", "J", "Q", "K", "A"]
suits = Literal["Diamonds", "Hearts", "Spades", "Clubs"]


class PlayingCard(GenericCard[ranks, suits]):
    RANKS = list(get_args(ranks))
    SUITS = list(get_args(suits))


class PlayingDeck(GenericDeck[PlayingCard]): ...


def test_deck_init():
    deck1 = PlayingDeck(PlayingCard)
    assert len(deck1.cards) == 32
    assert all(isinstance(card, PlayingCard) for card in deck1)

    cards = [PlayingCard(0, 0)]
    deck2 = PlayingDeck(PlayingCard, cards)
    assert deck2.cards == cards


def test_deck_count():
    deck = PlayingDeck(PlayingCard)
    assert deck.count(PlayingCard(0, 0)) == 1
    assert deck.count("7") == 4
    assert deck.count("Diamonds") == 8

    with pytest.raises(ValueError):
        deck.count("InvalidName")

    with pytest.raises(TypeError):
        deck.count(PlayingCard(0, 0).rank)


def test_deck_sort():
    deck = PlayingDeck(PlayingCard).shuffle()
    deck.sort(by="rank")
    assert deck.cards == sorted(deck.cards, key=lambda c: (
        not c.trump, c.rank if c.rank is not None else -1,
        c.suit if c.suit is not None else -1))

    deck.sort(by="suit")
    assert deck.cards == sorted(deck.cards)

    with pytest.raises(ValueError):
        deck.sort(by="invalid_key")


def test_deck_shuffle():
    deck = PlayingDeck(PlayingCard).shuffle()
    assert deck.cards != sorted(deck.cards)


def test_deck_draw():
    deck = PlayingDeck(PlayingCard)
    cards = deck.draw(5)
    assert len(cards) == 5
    assert len(deck.cards) == 27

    cards = deck.draw()
    assert len(cards) == 1
    assert len(deck.cards) == 26


def test_deck_add():
    deck = PlayingDeck(PlayingCard)
    cards = [PlayingCard(0, 0), PlayingCard(1, 1)]
    deck.add(*cards)
    assert deck.cards[-1] == cards[-1]


def test_deck_remove():
    deck = PlayingDeck(PlayingCard)
    card = PlayingCard(0, 0)
    deck.remove(card)
    assert card not in deck.cards

    with pytest.raises(ValueError):
        deck.remove(PlayingCard(10, 10))


def test_deck_get_index():
    deck = PlayingDeck(PlayingCard)
    card = PlayingCard(0, 0)
    assert deck.get_index(card) == [0]

    with pytest.raises(ValueError):
        deck.get_index(PlayingCard(10, 10))

    with pytest.raises(TypeError):
        deck.get_index("Ace of Diamonds")


def test_deck_get_cards():
    deck = PlayingDeck(PlayingCard)
    assert deck.get_cards() == deck.cards


def test_deck_get_top_card():
    deck = PlayingDeck(PlayingCard)
    assert deck.get_top_card() == deck.cards[0]


def test_deck_str():
    deck = PlayingDeck(PlayingCard)
    assert str(deck) == "Deck of 32 cards. Top card: 7 of Diamonds"


def test_deck_repr():
    deck = PlayingDeck(PlayingCard)
    deck_repr = repr(deck)
    assert deck_repr.startswith("PlayingDeck(cards=[PlayingCard(rank=0, suit=0),")
    assert deck_repr.endswith("PlayingCard(rank=7, suit=3)])")
