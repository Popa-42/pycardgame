from typing import Literal

import pytest

from ... import GenericCard, CardMeta

T_Ranks = Literal["7", "8", "9", "10", "J", "Q", "K", "A"]
T_Suits = Literal["Diamonds", "Hearts", "Spades", "Clubs"]


class TestingCard(
    GenericCard[T_Ranks, T_Suits],
    metaclass=CardMeta,
    rank_type=T_Ranks,
    suit_type=T_Suits
):
    ...


def test_card_init():
    card1 = TestingCard("10", "Hearts")
    assert card1.rank == 3
    assert card1.suit == 1
    assert card1.trump is False

    card2 = TestingCard(4, 2, True)
    assert card2.rank == 4
    assert card2.suit == 2
    assert card2.trump is True

    with pytest.raises(ValueError):
        TestingCard("InvalidRank", "Diamonds")  # type: ignore
    with pytest.raises(ValueError):
        TestingCard("10", "InvalidSuit")  # type: ignore


def test_card_get_rank():
    card1 = TestingCard(0, 0)
    assert card1.get_rank() == "7"
    assert card1.get_rank(as_index=True) == 0

    card2 = TestingCard(None, None)
    assert card2.get_rank() is None
    assert card2.get_rank(as_index=True) is None


def test_card_set_rank():
    card = TestingCard(0, 0)
    card.set_rank("K")
    assert card.rank == 6
    card.set_rank(2)
    assert card.rank == 2
    card.set_rank(None)
    assert card.rank is None

    with pytest.raises(ValueError):
        card.set_rank("InvalidRank")  # type: ignore

    with pytest.raises(ValueError):
        card.set_rank(10)


def test_card_get_suit():
    card1 = TestingCard(0, 0)
    assert card1.get_suit() == "Diamonds"
    assert card1.get_suit(as_index=True) == 0

    card2 = TestingCard(None, None)
    assert card2.get_suit() is None
    assert card2.get_suit(as_index=True) is None


def test_card_set_suit():
    card = TestingCard(0, 0)
    card.set_suit("Clubs")
    assert card.suit == 3
    card.set_suit(1)
    assert card.suit == 1
    card.set_suit(None)
    assert card.suit is None

    with pytest.raises(ValueError):
        card.set_suit("InvalidSuit")  # type: ignore

    with pytest.raises(ValueError):
        card.set_suit(10)


def test_card_get_trump():
    card = TestingCard(0, 0, True)
    assert card.get_trump() is True


def test_card_set_trump():
    card = TestingCard(0, 0)
    card.set_trump(True)
    assert card.trump is True

    with pytest.raises(TypeError):
        card.set_trump(1)  # type: ignore


def test_card_copy():
    card1 = TestingCard(0, 0)
    card2 = card1.__copy__()
    assert card1 is not card2
    assert card1 == card2
    assert card1.rank == card2.rank
    assert card1.suit == card2.suit
    assert card1.trump == card2.trump

    card3 = TestingCard(None, None)
    card4 = card3.__copy__()
    assert card3 is not card4
    assert card3 == card4
    assert card3.rank is None
    assert card3.suit is None
    assert card3.trump is False


def test_card_str():
    card1 = TestingCard(0, 0)
    assert str(card1) == "7 of Diamonds"

    card2 = TestingCard(4, 2, True)
    assert str(card2) == "J of Spades (trump)"

    card3 = TestingCard(None, None)
    assert str(card3) == "None of None"


def test_card_repr():
    card1 = TestingCard(0, 0)
    assert repr(card1) == "TestingCard(rank=0, suit=0)"

    card2 = TestingCard(4, 2, True)
    assert repr(card2) == "TestingCard(rank=4, suit=2, trump=True)"

    card3 = TestingCard(None, None)
    assert repr(card3) == "TestingCard(rank=None, suit=None)"


def test_card_comparison():
    card1 = TestingCard(0, 0)
    card2 = TestingCard(0, 0)
    card3 = TestingCard(1, 0)
    card4 = TestingCard(0, 1)
    card5 = TestingCard(0, 0, True)

    assert card1 == card2
    assert card1 != card3
    assert card1 != card4
    assert card1 != card5
    assert card1 < card3
    assert card1 < card4
    assert card1 < card5
    assert card3 > card1
    assert card4 > card1
    assert card5 > card1
