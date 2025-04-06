from ....src.base import GenericCard
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
    assert all(isinstance(card, GenericCard) for card in deck.cards)
    assert all(isinstance(card, UnoCard) for card in deck.cards)

    assert all(isinstance(card, NumberCard) for card in deck.cards[0:76])
    assert all(isinstance(card, DrawTwoCard) for card in deck.cards[76:84])
    assert all(isinstance(card, SkipCard) for card in deck.cards[84:92])
    assert all(isinstance(card, ReverseCard) for card in deck.cards[92:100])
    assert all(isinstance(card, WildCard) for card in deck.cards[100:108:2])
    assert all(
        isinstance(card, WildDrawFourCard) for card in deck.cards[101:108:2])


def test_uno_deck_shuffle():
    deck = UnoDeck()
    original_order = deck.cards.copy()
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
