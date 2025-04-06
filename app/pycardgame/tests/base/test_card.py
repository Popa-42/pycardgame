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

from ...src.base import CardMeta, GenericCard

T_Ranks = Literal["1", "2", "3"]
T_Suits = Literal["Red", "Green", "Blue"]


class DummyCard(
    GenericCard[T_Ranks, T_Suits],
    metaclass=CardMeta,
    rank_type=T_Ranks,
    suit_type=T_Suits
):
    def effect(self, game, player, *args):  # pragma: no cover
        pass


def test_card_init():
    card1 = DummyCard(rank="2", suit="Blue")
    assert card1.rank == 1
    assert card1.suit == 2
    assert card1.trump is False

    card2 = DummyCard(1, 2, True)
    assert card2.rank == 1
    assert card2.suit == 2
    assert card2.trump is True

    with pytest.raises(ValueError):
        DummyCard("InvalidRank", "Red")  # type: ignore
    with pytest.raises(ValueError):
        DummyCard("1", "InvalidSuit")  # type: ignore


def test_card_get_rank():
    card1 = DummyCard(0, 0)
    assert card1.get_rank() == "1"
    assert card1.get_rank(as_index=True) == 0

    card2 = DummyCard(None, None)
    assert card2.get_rank() is None
    assert card2.get_rank(as_index=True) is None


def test_card_set_rank():
    card = DummyCard(0, 0)
    card.change_rank("2")
    assert card.rank == 1
    card.change_rank(2)
    assert card.rank == 2
    card.change_rank(None)
    assert card.rank is None

    with pytest.raises(ValueError):
        card.change_rank("InvalidRank")  # type: ignore

    with pytest.raises(ValueError):
        card.change_rank(10)


def test_card_get_suit():
    card1 = DummyCard(0, 0)
    assert card1.get_suit() == "Red"
    assert card1.get_suit(as_index=True) == 0

    card2 = DummyCard(None, None)
    assert card2.get_suit() is None
    assert card2.get_suit(as_index=True) is None


def test_card_set_suit():
    card = DummyCard(0, 0)
    card.change_suit("Green")
    assert card.suit == 1
    card.change_suit(2)
    assert card.suit == 2
    card.change_suit(None)
    assert card.suit is None

    with pytest.raises(ValueError):
        card.change_suit("InvalidSuit")  # type: ignore

    with pytest.raises(ValueError):
        card.change_suit(10)


def test_card_get_trump():
    card = DummyCard(0, 0, True)
    assert card.is_trump() is True


def test_card_set_trump():
    card = DummyCard(0, 0)
    card.set_trump(True)
    assert card.trump is True

    with pytest.raises(TypeError):
        card.set_trump(1)  # type: ignore


def test_card_copy():
    card1 = DummyCard(0, 0)
    card2 = card1.__copy__()
    assert card1 is not card2
    assert card1 == card2
    assert card1.rank == card2.rank
    assert card1.suit == card2.suit
    assert card1.trump == card2.trump

    card3 = DummyCard(None, None)
    card4 = card3.__copy__()
    assert card3 is not card4
    assert card3 == card4
    assert card3.rank is None
    assert card3.suit is None
    assert card3.trump is False


def test_card_str():
    card1 = DummyCard(0, 0)
    assert str(card1) == "Red 1"

    card2 = DummyCard(1, 2, True)
    assert str(card2) == "Blue 2 (trump)"

    card3 = DummyCard(None, None)
    assert str(card3) == "None None"


def test_card_repr():
    card1 = DummyCard(0, 0)
    assert repr(card1) == "DummyCard(rank=0, suit=0)"

    card2 = DummyCard(2, 1, True)
    assert repr(card2) == "DummyCard(rank=2, suit=1, trump=True)"

    card3 = DummyCard(None, None)
    assert repr(card3) == "DummyCard(rank=None, suit=None)"


def test_card_comparison():
    card1 = DummyCard(0, 0)
    card2 = DummyCard(0, 0)
    card3 = DummyCard(1, 0)
    card4 = DummyCard(0, 1)
    card5 = DummyCard(0, 0, True)

    assert card1 == card2
    assert card1 != card3
    assert card1 != card4
    assert card1 != card5
    assert card1 < card3
    assert card1 < card4
    assert card1 <= card5
    assert card3 > card1
    assert card4 > card1
    assert card5 >= card1

    assert not card1 == "InvalidType"  # type: ignore
    assert card1 != "InvalidType"  # type: ignore
