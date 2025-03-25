import pytest

from ...src.presets import PokerCard, PokerDeck


def test_deck_init():
    deck1 = PokerDeck()
    assert len(deck1.cards) == 52
    assert all(isinstance(card, PokerCard) for card in deck1)


def test_deck_count():
    deck = PokerDeck()
    assert deck.count(PokerCard(0, 0)) == 1
    assert deck.count("Ace") == 4
    assert deck.count("Diamonds") == 13

    with pytest.raises(ValueError):
        deck.count("InvalidName")

    with pytest.raises(TypeError):
        deck.count(PokerCard(0, 0).rank)


def test_deck_sort():
    deck = PokerDeck().shuffle()
    deck.sort(by="rank")
    assert deck.cards == sorted(deck.cards, key=lambda c: (
        not c.trump, c.rank if c.rank is not None else -1,
        c.suit if c.suit is not None else -1))

    deck.sort(by="suit")
    assert deck.cards == sorted(deck.cards)

    with pytest.raises(ValueError):
        deck.sort(by="invalid_key")


def test_deck_shuffle():
    deck = PokerDeck().shuffle()
    assert deck.cards != sorted(deck.cards)


def test_deck_draw():
    deck = PokerDeck()
    cards = deck.draw(5)
    assert len(cards) == 5
    assert len(deck.cards) == 47

    cards = deck.draw()
    assert len(cards) == 1
    assert len(deck.cards) == 46


def test_deck_add():
    deck = PokerDeck()
    cards = [PokerCard(0, 0), PokerCard(1, 1)]
    deck.add(*cards)
    assert deck.cards[-1] == cards[-1]


def test_deck_remove():
    deck = PokerDeck()
    card = PokerCard(0, 0)
    deck.remove(card)
    assert card not in deck.cards

    with pytest.raises(ValueError):
        deck.remove(PokerCard(10, 10))


def test_deck_get_index():
    deck = PokerDeck()
    card = PokerCard(0, 0)
    assert deck.get_index(card) == [0]

    with pytest.raises(ValueError):
        deck.get_index(PokerCard(10, 10))

    with pytest.raises(TypeError):
        deck.get_index("Ace of Diamonds")


def test_deck_get_cards():
    deck = PokerDeck()
    assert deck.get_cards() == deck.cards


def test_deck_get_top_card():
    deck = PokerDeck()
    assert deck.get_top_card() == deck.cards[0]


def test_deck_str():
    deck = PokerDeck()
    assert str(deck) == "Deck of 52 cards. Top card: 2 of Diamonds"


def test_deck_repr():
    deck = PokerDeck()
    deck_repr = repr(deck)
    assert deck_repr.startswith("PokerDeck(cards=[PokerCard(rank=0, suit=0),")
    assert deck_repr.endswith("PokerCard(rank=12, suit=3)])")
