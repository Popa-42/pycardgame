import pytest

from ..src.base import Card, Deck


# ==========================|     Test Card class    |==========================

def test_card_init():
    card = Card("Ace", "Hearts", trump=False, extra="extra")
    assert card.rank == 12
    assert card.suit == 2
    assert card.trump is False
    assert card.extra == "extra"


def test_card_get_suit():
    card1 = Card("Ace", "Hearts")
    assert card1.get_suit() == "Hearts"
    assert card1.get_suit(as_index=True) == 2

    card2 = Card(None, None)
    assert card2.get_suit() is None
    assert card2.get_suit(as_index=True) is None


def test_card_set_suit():
    card = Card("Ace", "Hearts")
    card.set_suit("Spades")
    assert card.suit == 3

    card.set_suit(1)
    assert card.suit == 1

    card.set_suit("Clubs")
    assert card.suit == 0

    with pytest.raises(ValueError):
        card.set_suit("InvalidSuit")

    with pytest.raises(ValueError):
        card.set_suit(-1)

    with pytest.raises(TypeError):
        invalid_suit = {"name": "InvalidSuit"}
        card.set_suit(invalid_suit)


def test_card_get_rank():
    card1 = Card("Ace", "Hearts")
    assert card1.get_rank() == "Ace"
    assert card1.get_rank(as_index=True) == 12

    card2 = Card(None, None)
    assert card2.get_rank() is None
    assert card2.get_rank(as_index=True) is None


def test_card_set_rank():
    card = Card("Ace", "Hearts")
    card.set_rank("King")
    assert card.rank == 11

    card.set_rank(1)
    assert card.rank == 1

    card.set_rank("Queen")
    assert card.rank == 10

    with pytest.raises(ValueError):
        card.set_rank("InvalidRank")

    with pytest.raises(ValueError):
        card.set_rank(-1)

    with pytest.raises(TypeError):
        invalid_rank_type = {"name": "InvalidRankType"}
        card.set_rank(invalid_rank_type)


def test_card_get_trump():
    card = Card("Ace", "Hearts", trump=True)
    assert card.get_trump() is True


def test_card_set_trump():
    card = Card("Ace", "Hearts")
    card.set_trump(True)
    assert card.trump is True

    card.set_trump(False)
    assert card.trump is False

    with pytest.raises(TypeError):
        card.set_trump("InvalidTrump")


def test_card_str():
    card1 = Card("Ace", "Hearts")
    assert str(card1) == "Ace of Hearts"

    card2 = Card("King", "Spades", trump=True)
    assert str(card2) == "King of Spades (trump)"


def test_card_repr():
    card1 = Card("Ace", "Hearts")
    assert repr(card1) == "Card(rank=12, suit=2)"

    card2 = Card("King", "Spades", trump=True)
    assert repr(card2) == "Card(rank=11, suit=3, trump=True)"


def test_card_compare():
    card1 = Card("2", "Clubs")
    card2 = Card("Ace", "Clubs")
    card3 = Card("2", "Hearts")
    card4 = Card("Ace", "Hearts", trump=True)
    card5 = Card("2", "Spades", trump=True)
    card6 = Card("Ace", "Spades", trump=True)

    assert card1 == card1
    assert card1 != card2
    assert card1 < card2
    assert card2 > card1
    assert not card2 < card1
    assert card1 <= card2
    assert card2 >= card1
    assert card2 < card3
    assert card3 < card4
    assert not card4 < card3
    assert card4 < card5
    assert card5 < card6


# ==========================|     Test Deck class    |==========================

def test_deck_init():
    deck1 = Deck()
    assert len(deck1) == 52

    cards = [Card("Ace", "Hearts"), Card("2", "Clubs")]
    deck2 = Deck(cards)
    assert len(deck2) == 2


def test_deck_reset():
    deck = Deck()
    deck.draw(10)
    assert len(deck) < 52
    deck.reset()
    assert len(deck) == 52


def test_deck_count():
    deck = Deck()
    assert deck.count("Ace") == 4
    assert deck.count("Hearts") == 13
    assert deck.count(Card("Ace", "Hearts")) == 1
    with pytest.raises(ValueError):
        deck.count("InvalidParameter")
    with pytest.raises(TypeError):
        deck.count(42)


def test_deck_sort():
    deck = Deck()
    deck.shuffle()
    deck.sort(by="rank")
    assert deck[0].rank < deck[-1].rank
    deck.sort(by="suit")
    assert deck[0].suit < deck[-1].suit
    with pytest.raises(ValueError):
        deck.sort(by="invalidKey")


def test_deck_shuffle():
    deck = Deck()
    cards = deck.cards.copy()
    deck.shuffle()
    assert deck.cards != cards


def test_deck_draw():
    deck = Deck()
    cards = deck.draw(5)
    assert len(deck) == 47
    assert len(cards) == 5
    for card in cards:
        assert card not in deck


def test_deck_add():
    deck = Deck()
    cards = deck.draw(5)
    deck.add(*cards)
    assert len(deck) == 52
    for card in cards:
        assert card in deck


def test_deck_remove():
    deck = Deck()
    cards = deck[:5].copy()
    deck.remove(*cards)
    assert len(deck) == 47
    for card in cards:
        assert card not in deck


def test_deck_get_index():
    deck = Deck()
    card = deck[10]
    assert deck.get_index(card) == [10]
    assert deck.get_index(Card("2", "Clubs")) == [0]
    with pytest.raises(TypeError):
        deck.get_index(42)


def test_deck_get_top_card():
    deck = Deck()
    assert deck.get_top_card() == deck[0]
    deck.draw(52)
    assert deck.get_top_card() is None


def test_deck_str():
    deck = Deck()
    assert str(deck) == "Deck of 52 cards. Top card: 2 of Clubs"


def test_deck_repr():
    deck = Deck()
    assert repr(deck).startswith("Deck(cards=[Card(rank=0, suit=0)")
    assert repr(deck).endswith("Card(rank=12, suit=3)])")


def test_deck_special():
    deck = Deck()
    assert deck[0] == deck.get_top_card()
    assert len(deck) == 52
    for card in deck:
        assert card in deck.get_cards()
