from typing import Literal

from ... import GenericCard, GenericPlayer, CardMeta

T_Ranks = Literal["7", "8", "9", "10", "J", "Q", "K", "A"]
T_Suits = Literal["Diamonds", "Hearts", "Spades", "Clubs"]


class DummyCard(
    GenericCard[T_Ranks, T_Suits],
    metaclass=CardMeta,
    rank_type=T_Ranks,
    suit_type=T_Suits
):
    ...


class DummyPlayer(GenericPlayer[DummyCard]):
    ...


def test_player_init():
    cards = [DummyCard("10", "Hearts"), DummyCard("J", "Diamonds")]
    player = DummyPlayer("Alice", cards, 10)
    assert player.name == "Alice"
    assert player.hand == cards
    assert player.score == 10


def test_player_add_card():
    player = DummyPlayer("Alice")
    card = DummyCard("10", "Hearts")
    player.add_card(card)
    assert player.hand == [card]
    player.add_card(card, card)
    assert player.hand == [card, card, card]


def test_player_remove_card():
    card = DummyCard("10", "Hearts")
    player = DummyPlayer("Alice", [card, card, card])
    player.remove_card(card)
    assert player.hand == [card, card]
    player.remove_card(card, card)
    assert player.hand == []


def test_player_play_card():
    card1 = DummyCard("10", "Hearts")
    card2 = DummyCard("J", "Diamonds")
    player = DummyPlayer("Alice", [card1, card2])
    assert player.play_card() == [card2]
    assert player.hand == [card1]
    assert player.play_card(card1) == [card1]
    assert player.hand == []


def test_player_get_hand():
    cards = [DummyCard("10", "Hearts"), DummyCard("J", "Diamonds")]
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
    cards = [DummyCard("10", "Hearts"), DummyCard("J", "Diamonds")]
    player = DummyPlayer("Alice", cards)
    assert player[0] == cards[0]
    assert player[1:-1:-1] == cards[1:-1:-1]


def test_player_str():
    player = DummyPlayer("Alice", [DummyCard("10", "Hearts")])
    assert str(player) == "Player Alice (1 card(s))"


def test_player_repr():
    player = DummyPlayer("Alice", [DummyCard("10", "Hearts")])
    player_repr = repr(player)
    assert player_repr.startswith("DummyPlayer('Alice', hand=[")
    assert "DummyCard(rank=3, suit=1)" in player_repr
    assert player_repr.endswith(", score=0)")


def test_player_equalities():
    player1 = DummyPlayer("Alice", [DummyCard("10", "Hearts")])
    player2 = DummyPlayer("Alice", [DummyCard("10", "Hearts")])
    assert player1 == player2
    assert player1 != DummyPlayer("Bob", [DummyCard("10", "Hearts")])
    assert player1 != DummyPlayer("Alice", [DummyCard("J", "Diamonds")])
    assert player1 != DummyPlayer("Alice", [DummyCard("10", "Hearts")], 10)
