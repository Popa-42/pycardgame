import pytest

from ..src.base import Card, Deck
from ..src.game import Player, Game


# =========================|     Test Player class    |=========================

def test_player_init():
    card = Card(1, 2)
    player = Player("Alice", [card], 10, extra="extra")
    assert player.name == "Alice"
    assert player.hand == [card]
    assert player.score == 10
    assert player.extra == "extra"


def test_player_add_card():
    player = Player("Alice")
    card1 = Card("Ace", "Hearts")
    card2 = Card("King", "Spades")
    player.add_card(card1, card2)
    assert player.hand == [card1, card2]


def test_player_remove_card():
    player = Player("Alice")
    card1 = Card("Ace", "Hearts")
    card2 = Card("King", "Spades")
    player.add_card(card1, card2)
    player.remove_card(card1)
    assert player.hand == [card2]


def test_player_play_card():
    player = Player("Alice")
    card1 = Card("Ace", "Hearts")
    card2 = Card("King", "Spades")
    player.add_card(card1, card2)

    played = player.play_card(card1)
    assert played == [card1]
    assert player.hand == [card2]

    played = player.play_card()
    assert played == [card2]
    assert player.hand == []


def test_player_get_hand():
    player = Player("Alice")
    card1 = Card("Ace", "Hearts")
    card2 = Card("King", "Spades")
    player.add_card(card1, card2)
    assert player.get_hand() == [card1, card2]


def test_player_get_score():
    player = Player("Alice", score=10)
    assert player.get_score() == 10


def test_player_set_score():
    player = Player("Alice")
    player.set_score(10)
    assert player.score == 10


def test_player_get_name():
    player = Player("Alice")
    assert player.get_name() == "Alice"


def test_player_set_name():
    player = Player("Alice")
    player.set_name("Bob")
    assert player.name == "Bob"


def test_player_getitem():
    player = Player("Alice", [Card("Ace", "Hearts"), Card("King", "Spades")])
    assert player[0] == Card("Ace", "Hearts")
    assert player[1] == Card("King", "Spades")


def test_player_str():
    player = Player("Alice", [Card("Ace", "Hearts")], 10)
    assert str(player) == "Player Alice (1 card(s))"


def test_player_repr():
    player = Player("Alice", [Card("Ace", "Hearts")], 10, extra="extra")
    assert repr(player) == ("Player('Alice', hand=[Card(rank=12, suit=2)], "
                            "score=10, extra='extra')")


def test_player_comparison():
    player1 = Player("Alice", score=10)
    player2 = Player("Bob", score=10)
    player3 = Player("Charlie", score=20)

    assert player1 == player1
    assert player1 != player2

    assert player1 < player3
    assert player3 > player1
    assert player1 <= player2
    assert player1 <= player3
    assert player2 >= player1
    assert player3 >= player1


def test_player_bool():
    player = Player("Alice", [Card("Ace", "Hearts")], 10)
    assert bool(player) is True

    player = Player("Alice", [], 10)
    assert bool(player) is False


def test_player_iter():
    player = Player("Alice", [Card("Ace", "Hearts"), Card("King", "Spades")],
                    10)
    assert list(player) == [Card("Ace", "Hearts"), Card("King", "Spades")]


def test_player_len():
    player = Player("Alice", [Card("Ace", "Hearts"), Card("King", "Spades")])
    assert len(player) == 2


# ==========================|     Test Game class    |==========================

def test_game_init():
    player1 = Player("Alice")
    player2 = Player("Bob")
    deck = Deck()
    game = Game(deck, "Hearts", 4, player1, player2, extra="extra")
    assert len(game.deck) == 44
    assert game.trump == "Hearts"
    assert game.hand_size == 4
    assert game.players == [player1, player2]
    assert game.extra == "extra"

    with pytest.raises(ValueError):
        Game(deck, "InvalidTrump")


def test_game_add_players():
    player1 = Player("Alice")
    player2 = Player("Bob")
    game = Game().add_players(player1, player2)
    assert game.players == [player1, player2]


def test_game_remove_players():
    player1 = Player("Alice")
    player2 = Player("Bob")
    game = Game().add_players(player1, player2)
    game.remove_players(player1)
    assert game.players == [player2]


def test_game_deal():
    player1 = Player("Alice")
    player2 = Player("Bob")
    game = Game().add_players(player1, player2)
    game.deal(1)
    assert len(player1) == 1
    assert len(player2) == 1

    game.deal(2, player1, player2)
    assert len(player1) == 3
    assert len(player2) == 3

    game.deal(2, player1)
    assert len(player1) == 5
    assert len(player2) == 3


def test_game_shuffle():
    game = Game()
    game.shuffle()
    assert len(game.deck) == 52


def test_game_play():
    player1 = Player("Alice")
    player2 = Player("Bob")
    game = Game(Deck()).add_players(player1, player2)
    game.deal(1, player1)
    game.play(player1)
    assert len(player1) == 0
    assert len(game.discard_pile) == 1

    game.deal(2)
    game.play(player2, *player2.get_hand())
    assert len(player1) == 2
    assert len(player2) == 0
    assert len(game.discard_pile) == 3


def test_game_get_trump():
    game = Game(trump="Hearts")
    assert game.get_trump() == "Hearts"


def test_game_set_trump():
    game = Game()
    game.set_trump("Hearts")
    assert game.trump == "Hearts"

    with pytest.raises(ValueError):
        game.set_trump("InvalidTrump")


def test_game_apply_trump():
    game = Game()
    game.set_trump("Hearts")
    game.apply_trump()
    for card in game.deck:
        if card.get_suit() == "Hearts":
            assert card.get_trump() is True
        else:
            assert card.get_trump() is False


def test_game_get_current_player():
    player1 = Player("Alice")
    player2 = Player("Bob")
    game = Game().add_players(player1, player2)
    assert game.get_current_player() == player1


def test_game_set_current_player():
    player1 = Player("Alice")
    player2 = Player("Bob")
    game = Game().add_players(player1, player2)
    game.set_current_player(player2)
    assert game.get_current_player() == player2


def test_game_get_players():
    player1 = Player("Alice")
    player2 = Player("Bob")
    game = Game().add_players(player1, player2)
    assert game.get_players() == [player1, player2]


def test_game_get_deck():
    game = Game()
    assert game.get_deck() == game.deck


def test_game_set_deck():
    game = Game()
    deck = Deck()
    game.set_deck(deck)
    assert game.deck == deck


def test_game_str():
    player1 = Player("Alice")
    player2 = Player("Bob")
    game = Game(players=[player1, player2])
    assert str(game) == "Game of 2 players"


def test_game_repr():
    player1 = Player("Alice")
    player2 = Player("Bob")
    game = Game(Deck(), "Hearts", 4, players=[player1, player2], extra="extra")
    game_repr = repr(game)
    assert game_repr.startswith("Game(")
    assert "deck=Deck(cards=[" in game_repr
    assert "Card(rank=0, suit=0)," in game_repr
    assert "discard_pile=Deck(cards=[])" in game_repr
    assert "trump='Hearts'" in game_repr
    assert "hand_size=4" in game_repr
    assert ("players=[Player('Alice', hand=[], score=0), "
            "Player('Bob', hand=[], score=0)]") in game_repr
    assert "current_player_index=0" in game_repr
    assert "extra='extra'" in game_repr
