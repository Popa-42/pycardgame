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

from ... import GenericCard, GenericPlayer, CardMeta

T_Ranks = Literal["1", "2", "3"]
T_Suits = Literal["Red", "Green", "Blue"]


class DummyCard(
    GenericCard[T_Ranks, T_Suits],
    metaclass=CardMeta,
    rank_type=T_Ranks,
    suit_type=T_Suits
):
    pass


class DummyPlayer(GenericPlayer[DummyCard]):
    pass


def test_player_init():
    cards = [DummyCard("2", "Green"), DummyCard("3", "Blue")]
    player = DummyPlayer("Alice", cards, 10)
    assert player.name == "Alice"
    assert player.hand == cards
    assert player.score == 10


def test_player_add_card():
    player = DummyPlayer("Alice")
    card = DummyCard("2", "Green")
    player.add_card(card)
    assert player.hand == [card]
    player.add_card(card, card)
    assert player.hand == [card, card, card]


def test_player_remove_card():
    card = DummyCard("2", "Green")
    player = DummyPlayer("Alice", [card, card, card])
    player.remove_card(card)
    assert player.hand == [card, card]
    player.remove_card(card, card)
    assert player.hand == []


def test_player_play_card():
    card1 = DummyCard("2", "Green")
    card2 = DummyCard("3", "Blue")
    player = DummyPlayer("Alice", [card1, card2])
    assert player.play_card() == [card2]
    assert player.hand == [card1]
    assert player.play_card(card1) == [card1]
    assert player.hand == []


def test_player_get_hand():
    cards = [DummyCard("2", "Green"), DummyCard("3", "Blue")]
    player = DummyPlayer("Alice", cards)
    assert player.get_hand() == cards


def test_player_get_score():
    player = DummyPlayer("Alice", [], 10)
    assert player.get_score() == 10


def test_player_set_score():
    player = DummyPlayer("Alice")
    player.set_score(10)
    assert player.score == 10
    player.set_score(20)
    assert player.score == 20


def test_player_get_name():
    player = DummyPlayer("Alice")
    assert player.get_name() == "Alice"


def test_player_set_name():
    player = DummyPlayer("Alice")
    player.set_name("Bob")
    assert player.name == "Bob"


def test_player_getitem():
    cards = [DummyCard("2", "Green"), DummyCard("3", "Blue")]
    player = DummyPlayer("Alice", cards)
    assert player[0] == cards[0]
    assert player[1:-1:-1] == cards[1:-1:-1]
    for card in player:
        assert card in cards
    assert len(player) == len(cards)


def test_player_str():
    player = DummyPlayer("Alice", [DummyCard("3", "Blue")])
    assert str(player) == "Player Alice (1 card(s))"


def test_player_repr():
    player = DummyPlayer("Alice", [DummyCard("3", "Blue")])
    player_repr = repr(player)
    assert player_repr.startswith("DummyPlayer('Alice', hand=[")
    assert "DummyCard(rank=2, suit=2)" in player_repr
    assert player_repr.endswith(", score=0)")


def test_player_equalities():
    player1 = DummyPlayer("Alice", [DummyCard("2", "Green")])
    player2 = DummyPlayer("Alice", [DummyCard("2", "Green")])
    assert player1 == player2
    assert player1 != DummyPlayer("Bob", [DummyCard("2", "Green")])
    assert player1 != DummyPlayer("Alice", [DummyCard("3", "Blue")])
    assert player1 != DummyPlayer("Alice", [DummyCard("2", "Green")], 10)
    assert not player1 == "InvalidType"  # type: ignore


def test_player_comparisons():
    player1 = DummyPlayer("Alice", [DummyCard("2", "Green")], 10)
    player2 = DummyPlayer("Bob", [DummyCard("2", "Green")], 20)
    assert player1 < player2
    assert player1 <= player2
    assert player2 > player1
    assert player2 >= player1
    assert not player1 < DummyPlayer("Alice")
