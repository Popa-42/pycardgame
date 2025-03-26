from typing import Literal, get_args

from ... import GenericCard, GenericPlayer

ranks = Literal["7", "8", "9", "10", "J", "Q", "K", "A"]
suits = Literal["Diamonds", "Hearts", "Spades", "Clubs"]


class TestingCard(GenericCard[ranks, suits]):
    RANKS = list(get_args(ranks))
    SUITS = list(get_args(suits))


class TestingPlayer(GenericPlayer[TestingCard]): ...


def test_player_init():
    cards = [TestingCard("10", "Hearts"), TestingCard("J", "Diamonds")]
    player = TestingPlayer("Alice", cards, 10)
    assert player.name == "Alice"
    assert player.hand == cards
    assert player.score == 10


def test_player_add_card():
    player = TestingPlayer("Alice")
    card = TestingCard("10", "Hearts")
    player.add_card(card)
    assert player.hand == [card]
    player.add_card(card, card)
    assert player.hand == [card, card, card]


def test_player_remove_card():
    card = TestingCard("10", "Hearts")
    player = TestingPlayer("Alice", [card, card, card])
    player.remove_card(card)
    assert player.hand == [card, card]
    player.remove_card(card, card)
    assert player.hand == []


def test_player_play_card():
    card1 = TestingCard("10", "Hearts")
    card2 = TestingCard("J", "Diamonds")
    player = TestingPlayer("Alice", [card1, card2])
    assert player.play_card() == [card2]
    assert player.hand == [card1]
    assert player.play_card(card1) == [card1]
    assert player.hand == []


def test_player_get_hand():
    cards = [TestingCard("10", "Hearts"), TestingCard("J", "Diamonds")]
    player = TestingPlayer("Alice", cards)
    assert player.get_hand() == cards


def test_player_get_score():
    player = TestingPlayer("Alice", [], 10)
    assert player.get_score() == 10


def test_player_set_score():
    player = TestingPlayer("Alice")
    player.set_score(10)
    assert player.score == 10
    player.set_score(20)
    assert player.score == 20


def test_player_get_name():
    player = TestingPlayer("Alice")
    assert player.get_name() == "Alice"


def test_player_set_name():
    player = TestingPlayer("Alice")
    player.set_name("Bob")
    assert player.name == "Bob"


def test_player_getitem():
    cards = [TestingCard("10", "Hearts"), TestingCard("J", "Diamonds")]
    player = TestingPlayer("Alice", cards)
    assert player[0] == cards[0]
    assert player[1:-1:-1] == cards[1:-1:-1]


def test_player_str():
    player = TestingPlayer("Alice", [TestingCard("10", "Hearts")])
    assert str(player) == "Player Alice (1 card(s))"


def test_player_repr():
    player = TestingPlayer("Alice", [TestingCard("10", "Hearts")])
    player_repr = repr(player)
    assert player_repr.startswith("TestingPlayer('Alice', hand=[")
    assert "TestingCard(rank=3, suit=1)" in player_repr
    assert player_repr.endswith(", score=0)")


def test_player_equalities():
    player1 = TestingPlayer("Alice", [TestingCard("10", "Hearts")])
    player2 = TestingPlayer("Alice", [TestingCard("10", "Hearts")])
    assert player1 == player2
    assert player1 != TestingPlayer("Bob", [TestingCard("10", "Hearts")])
    assert player1 != TestingPlayer("Alice", [TestingCard("J", "Diamonds")])
    assert player1 != TestingPlayer("Alice", [TestingCard("10", "Hearts")], 10)
