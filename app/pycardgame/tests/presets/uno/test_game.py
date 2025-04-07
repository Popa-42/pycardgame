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

import pytest

from ....src.presets import (
    DrawTwoCard,
    NumberCard,
    UnoCard,
    UnoDeck,
    UnoGame,
    UnoPlayer,
    WildCard,
)


def test_uno_player_init():
    player = UnoPlayer("Player 1", [NumberCard("5", "Red")])
    assert player.name == "Player 1"
    assert len(player) == 1
    assert isinstance(player.hand[0], NumberCard)


def test_uno_player_call_uno():
    player = UnoPlayer("Player 1", [NumberCard("5", "Red")])
    assert player.uno is False
    player.call_uno()
    assert player.uno is True


def test_uno_player_reset_uno():
    player = UnoPlayer("Player 1")
    player.uno = True
    assert player.uno is True
    player.reset_uno()
    assert player.uno is False


def test_uno_player_str():
    player = UnoPlayer("Player 1", [NumberCard("5", "Red")])
    assert str(player) == "Player Player 1 (1 card(s)):\n - Red 5"


def test_uno_player_repr():
    player = UnoPlayer("Player 1", [NumberCard("5", "Red")])
    print(player.score)
    assert repr(player) == ("UnoPlayer('Player 1', "
                            "hand=[NumberCard(rank=5, suit=0)], uno=False)")


def test_uno_game_init():
    player1 = UnoPlayer("Player 1")
    player2 = UnoPlayer("Player 2")
    game = UnoGame(player1, player2)
    assert len(game.players) == 2
    assert isinstance(game.draw_pile, UnoDeck)
    assert isinstance(game.discard_pile, UnoDeck)
    assert game.hand_size == 7
    assert game.direction == 1


def test_uno_game_check_valid_play():
    card1 = NumberCard("5", "Red")
    card2 = NumberCard("5", "Blue")
    card3 = NumberCard("7", "Blue")
    game = UnoGame()

    assert game.check_valid_play(card1) is False
    assert game.check_valid_play(None, card1) is False  # type: ignore

    assert game.check_valid_play(card1, card2) is True
    assert game.check_valid_play(card1, card3) is False
    assert game.check_valid_play(card2, card3) is True

    wild = WildCard()
    cards = [card1, card2, card3, wild]
    assert (game.check_valid_play(card, wild) is True for card in cards)

    game.draw_count = 2
    assert game.check_valid_play(card1, card2) is False


def test_uno_game_discard_cards():
    player = UnoPlayer("Player 1", [NumberCard("5", "Red")])
    game = UnoGame(player)
    game.discard_cards(NumberCard("5", "Red"))
    assert len(game.discard_pile) == 1
    assert game.discard_pile.get_top_card() == NumberCard("5", "Red")


def test_uno_game_get_top_card():
    player = UnoPlayer("Player 1", [NumberCard("5", "Red")])
    game = UnoGame(player)
    game.discard_cards(NumberCard("5", "Red"))
    assert game.get_top_card() == NumberCard("5", "Red")


def test_uno_game_get_next_player():
    player1 = UnoPlayer("Player 1")
    player2 = UnoPlayer("Player 2")
    player3 = UnoPlayer("Player 3")
    game = UnoGame(player1, player2, player3)

    assert game.get_next_player() == player2
    game.direction = -1
    assert game.get_next_player() == player3


def test_uno_game_play_card():
    player1 = UnoPlayer("Player 1", [NumberCard("5", "Red")])
    player2 = UnoPlayer("Player 2", [NumberCard("7", "Blue")])
    game = UnoGame(player1, player2)

    assert game.play_card(NumberCard("5", "Red")) is False

    game.discard_cards(NumberCard("1", "Red"))

    assert game.play_card(NumberCard("5", "Red")) is True
    assert len(player1) == 0
    assert len(game.discard_pile) == 2
    assert game.get_top_card() == NumberCard("5", "Red")
    assert game.play_card(NumberCard("7", "Blue"), player2) is False


def test_uno_game_draw_instead_of_play():
    player1 = UnoPlayer("Player 1", [DrawTwoCard("Red")])
    player2 = UnoPlayer("Player 2", [NumberCard("7", "Blue")])
    game = UnoGame(player1, player2)

    game.draw_pile = UnoDeck()

    game.discard_cards(NumberCard("5", "Red"))
    game.play_card(DrawTwoCard("Red"), player1)
    assert len(player1) == 0
    assert len(player2) == 1
    assert game.draw_count == 2

    game.next_player()
    drawn = game.draw_instead_of_play()
    assert len(drawn) == 2
    assert len(player2) == 3
    assert game.draw_count == 0

    with pytest.raises(RecursionError):
        game.draw_pile = UnoDeck([])
        assert game.draw_instead_of_play(player2) == []


def test_uno_game_draw_cards():
    player = UnoPlayer("Player 1")
    game = UnoGame(player)

    drawn_cards = game.draw_cards(player, 2)
    assert drawn_cards is not None
    assert len(drawn_cards) == 2
    assert len(player) == 2
    assert len(game.draw_pile) == 106

    drawn_card = game.draw_cards(player)
    assert drawn_card is not None
    assert len(drawn_card) == 1
    assert len(player) == 3
    assert len(game.draw_pile) == 105

    with pytest.raises(ValueError):
        game.draw_cards(player, 999)


def test_uno_game_reverse_direction():
    player1 = UnoPlayer("Player 1")
    player2 = UnoPlayer("Player 2")
    game = UnoGame(player1, player2)

    assert game.direction == 1
    game.reverse_direction()
    assert game.direction == -1
    game.reverse_direction()
    assert game.direction == 1


def test_uno_game_start_game():
    player1 = UnoPlayer("Player 1")
    player2 = UnoPlayer("Player 2")
    game = UnoGame(player1, player2)

    game.start_game()
    assert len(player1) == 7
    assert len(player2) == 7
    assert len(game.draw_pile) == 108 - 14 - 1
    assert len(game.discard_pile) == 1
    assert isinstance(game.discard_pile.get_top_card(), UnoCard)


def test_uno_game_next_player():
    player1 = UnoPlayer("Player 1")
    player2 = UnoPlayer("Player 2")
    player3 = UnoPlayer("Player 3")
    game = UnoGame(player1, player2, player3)

    assert game.current_player_index == 0
    game.next_player()
    assert game.current_player_index == 1
    game.next_player()
    assert game.current_player_index == 2
    game.next_player()
    assert game.current_player_index == 0


def test_uno_game_determine_winner():
    player1 = UnoPlayer("Player 1", [NumberCard("5", "Red")])
    player2 = UnoPlayer("Player 2", [NumberCard("7", "Blue")])
    game = UnoGame(player1, player2)

    assert game.determine_winner() is None

    player1.play_cards(NumberCard("5", "Red"))
    assert game.determine_winner() == player1


def test_uno_game_end_game():
    player1 = UnoPlayer("Player 1", [NumberCard("5", "Red")])
    player2 = UnoPlayer("Player 2", [NumberCard("7", "Blue")])
    game1 = UnoGame(player1, player2)

    assert game1.game_ended is False
    assert game1.end_game() is None
    assert game1.game_ended is True
    assert len(game1.draw_pile) == 0
    assert len(game1.discard_pile) == 0
    assert len(game1.players) == 0
    assert len(player1) == 0
    assert len(player2) == 0

    player2.add_cards(NumberCard("5", "Red"))
    game2 = UnoGame(player1, player2)
    assert game2.end_game() is not None


def test_uno_game_str():
    player1 = UnoPlayer("Player 1", [NumberCard("5", "Red")])
    player2 = UnoPlayer("Player 2", [NumberCard("7", "Blue")])
    game = UnoGame(player1, player2)
    game.discard_cards(NumberCard("1", "Red"))

    assert str(game) == ("UNO Game\n"
                         "Current Player: Player 1\n"
                         "Draw Pile: 108 card(s)\n"
                         "Discard Pile: 1 card(s)\n"
                         "Direction: Clockwise\n"
                         "Top Card: Red 1\n"
                         "Players:\n"
                         " - Player 1: 1 card(s)\n"
                         " - Player 2: 1 card(s)")


def test_uno_game_repr():
    player1 = UnoPlayer("Player 1", [NumberCard("5", "Red")])
    player2 = UnoPlayer("Player 2", [NumberCard("7", "Blue")])
    deck = UnoDeck()
    game = UnoGame(player1, player2, draw_pile=deck)

    assert repr(game) == (f"UnoGame(players=[{player1!r}, {player2!r}], "
                          f"draw_pile={UnoDeck()!r}, "
                          f"discard_pile={UnoDeck([])!r}, "
                          f"hand_size=7, current_player_index=0, direction=1)")
