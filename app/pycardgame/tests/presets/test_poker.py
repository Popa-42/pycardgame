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

from ... import PokerCard, PokerDeck, PokerPlayer, PokerGame


def test_deck_init():
    deck1 = PokerDeck()
    assert len(deck1.cards) == 52
    assert all(isinstance(card, PokerCard) for card in deck1)


def test_player_init():
    player1 = PokerPlayer("Player 1")
    assert player1.name == "Player 1"
    assert len(player1.hand) == 0
    assert player1.bankroll == 1000


def test_player_bet():
    player1 = PokerPlayer("Player 1", 1000)
    player1.bet(100)
    assert player1.bankroll == 900

    with pytest.raises(ValueError):
        player1.bet(2000)


def test_player_win():
    player1 = PokerPlayer("Player 1", 900)
    player1.win(100)
    assert player1.bankroll == 1000


def test_game_init():
    game1 = PokerGame(0)
    assert game1.current_player_index == 0
    assert len(game1.players) == 0
    assert game1.deck is not None
    assert game1.discard_pile is not None
    assert game1.trash_pile is not None
    assert game1.trash_pile_limit == 2
    assert game1.trash_pile_index == 0
