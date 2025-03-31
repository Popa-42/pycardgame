from typing import Literal

import pytest

from ... import CardMeta, DeckMeta, GenericCard, GenericDeck

T_Ranks = Literal["7", "8", "9", "10", "J", "Q", "K", "A"]
T_Suits = Literal["Diamonds", "Hearts", "Spades", "Clubs"]


class TestingCard(
    GenericCard[T_Ranks, T_Suits],
    metaclass=CardMeta,
    rank_type=T_Ranks,
    suit_type=T_Suits
):
    ...


class TestingDeck(
    GenericDeck[TestingCard],
    metaclass=DeckMeta,
    card_type=TestingCard
):
    ...


def test_deck_init():
    deck1 = TestingDeck()
    assert len(deck1.cards) == 32
    assert all(isinstance(card, TestingCard) for card in deck1)

    cards = [TestingCard(0, 0)]
    deck2 = TestingDeck(cards)
    assert deck2.cards == cards


def test_deck_count():
    deck = TestingDeck()
    assert deck.count(TestingCard(0, 0)) == 1
    assert deck.count("7") == 4
    assert deck.count("Diamonds") == 8

    with pytest.raises(ValueError):
        deck.count("InvalidName")

    with pytest.raises(TypeError):
        deck.count(TestingCard(0, 0).rank)


def test_deck_sort():
    deck = TestingDeck().shuffle()
    deck.sort(by="rank")
    assert deck.cards == sorted(deck.cards, key=lambda c: (
        not c.trump, c.rank if c.rank is not None else -1,
        c.suit if c.suit is not None else -1))

    deck.sort(by="suit")
    assert deck.cards == sorted(deck.cards)

    with pytest.raises(ValueError):
        deck.sort(by="invalid_key")  # type: ignore


def test_deck_shuffle():
    deck = TestingDeck().shuffle()
    assert deck.cards != sorted(deck.cards)


def test_deck_draw():
    deck = TestingDeck()
    cards = deck.draw(5)
    assert len(cards) == 5
    assert len(deck.cards) == 27

    cards = deck.draw()
    assert len(cards) == 1
    assert len(deck.cards) == 26


def test_deck_add():
    deck = TestingDeck()
    cards = [TestingCard(0, 0), TestingCard(1, 1)]
    deck.add(*cards)
    assert deck.cards[-1] == cards[-1]


def test_deck_remove():
    deck = TestingDeck()
    card = TestingCard(0, 0)
    deck.remove(card)
    assert card not in deck.cards

    with pytest.raises(ValueError):
        deck.remove(TestingCard(10, 10))


def test_deck_get_index():
    deck = TestingDeck()
    card = TestingCard(0, 0)
    assert deck.get_index(card) == [0]

    with pytest.raises(ValueError):
        deck.get_index(TestingCard(10, 10))

    with pytest.raises(TypeError):
        deck.get_index("Ace of Diamonds")  # type: ignore


def test_deck_get_cards():
    deck = TestingDeck()
    assert deck.get_cards() == deck.cards


def test_deck_get_top_card():
    deck = TestingDeck()
    assert deck.get_top_card() == deck.cards[0]


def test_deck_str():
    deck = TestingDeck()
    assert str(deck) == "Deck of 32 cards. Top card: 7 of Diamonds"


def test_deck_repr():
    deck = TestingDeck()
    deck_repr = repr(deck)
    assert deck_repr.startswith("TestingDeck(card_type=<class")
    assert "cards=[TestingCard(rank=0, suit=0)," in deck_repr
    assert deck_repr.endswith("TestingCard(rank=7, suit=3)])")


def test_deck_copy():
    deck1 = TestingDeck()
    deck2 = deck1.__copy__()
    assert deck1 is not deck2
    assert deck1.cards == deck2.cards
    assert deck1.cards is not deck2.cards
    assert isinstance(deck2, TestingDeck)


def test_deck_getitem():
    deck = TestingDeck()
    assert deck[0] == deck.cards[0]
    assert deck[1:-1:-1] == deck.cards[1:-1:-1]
