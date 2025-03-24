import pytest

from ...src.presets import SkatCard, SkatDeck


# =======================|     Test Skat Card class     |=======================

def test_skat_card_init():
    card = SkatCard("Ace", "Hearts")
    assert card.rank == 7
    assert card.suit == 1

    with pytest.raises(ValueError):
        SkatCard("InvalidRank", "Hearts")

    with pytest.raises(ValueError):
        SkatCard("Ace", "InvalidSuit")


def test_skat_card_get_suit():
    card = SkatCard("Ace", "Hearts")
    assert card.get_suit() == "Hearts"
    assert card.get_suit(as_index=True) == 1


def test_skat_card_set_suit():
    card = SkatCard("Ace", "Hearts")
    card.set_suit("Spades")
    assert card.suit == 2

    card.set_suit(1)
    assert card.suit == 1

    card.set_suit("Clubs")
    assert card.suit == 3

    with pytest.raises(ValueError):
        card.set_suit("InvalidSuit")

    with pytest.raises(ValueError):
        card.set_suit(-1)

    with pytest.raises(TypeError):
        invalid_suit = {"name": "InvalidSuit"}
        card.set_suit(invalid_suit)


def test_skat_card_get_rank():
    card = SkatCard("Ace", "Hearts")
    assert card.get_rank() == "Ace"
    assert card.get_rank(as_index=True) == 7


def test_skat_card_set_rank():
    card = SkatCard("Ace", "Hearts")
    card.set_rank("King")
    assert card.rank == 6

    card.set_rank(1)
    assert card.rank == 1

    card.set_rank("Queen")
    assert card.rank == 5

    with pytest.raises(ValueError):
        card.set_rank("InvalidRank")

    with pytest.raises(ValueError):
        card.set_rank(-1)


# =======================|     Test Skat Deck class     |=======================

def test_skat_deck_init():
    deck = SkatDeck()
    assert len(deck) == 32

    deck = SkatDeck([SkatCard("Ace", "Hearts")])
    assert len(deck) == 1

    with pytest.raises(ValueError):
        SkatDeck([SkatCard("InvalidRank", "Hearts")])

    with pytest.raises(ValueError):
        SkatDeck([SkatCard("Ace", "InvalidSuit")])
