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

from ... import (
    CardMeta,
    DeckMeta,
    GenericCard,
    GenericDeck,
    GenericGame,
    GenericPlayer,
)

T_Ranks = Literal["1", "2", "3"]
T_Suits = Literal["Red", "Green", "Blue"]


class DummyCard(
    GenericCard[T_Ranks, T_Suits],
    metaclass=CardMeta,
    rank_type=T_Ranks,
    suit_type=T_Suits
):
    pass


class DummyDeck(
    GenericDeck[DummyCard],
    metaclass=DeckMeta,
    card_type=DummyCard
):
    pass


class DummyPlayer(GenericPlayer[DummyCard]):
    pass


class DummyGame(GenericGame[DummyCard]):
    def __init__(self, *players, deck=None, discard_pile=None, trump=None, hand_size=4,
                 starting_player_index=0):
        super().__init__(DummyCard, DummyDeck, deck, discard_pile, trump,
                         hand_size, starting_player_index, *players)


def test_game_init():
    deck = DummyDeck()
    empty_deck = DummyDeck(cards=[])
    players = [DummyPlayer("Alice"), DummyPlayer("Bob")]

    game = DummyGame(*players, deck=deck, discard_pile=empty_deck,
                     trump="Green", hand_size=2, starting_player_index=1)
    assert game.deck == deck
    assert game.discard_pile == empty_deck
    assert game.trump == "Green"
    assert game.hand_size == 2
    assert game.players == players
    assert game.current_player_index == 1

    # Invalid trump suit
    with pytest.raises(ValueError):
        DummyGame(*players, trump="InvalidSuit")

    # Invalid player count
    with pytest.raises(ValueError):
        DummyGame(*players, starting_player_index=10)


def test_game_deal_initial_cards():
    players = [DummyPlayer("Alice"), DummyPlayer("Bob")]
    deck = DummyDeck()
    game = DummyGame(*players, hand_size=2)
    game.deal_initial_cards()
    assert all(len(player.hand) == 2 for player in players)
    assert len(game.deck) == len(deck)


def test_game_add_players():
    players = [DummyPlayer("Alice"), DummyPlayer("Bob")]
    game = DummyGame(*players, hand_size=2)
    new_players = [DummyPlayer("Charlie"), DummyPlayer("David")]
    game.add_players(*new_players)
    assert game.players == players + new_players


def test_game_remove_players():
    players = [DummyPlayer("Alice"), DummyPlayer("Bob")]
    game = DummyGame(*players, hand_size=2)
    game.remove_players(players[0])
    assert game.players == players[1:]


def test_game_deal():
    players = [DummyPlayer("Alice"), DummyPlayer("Bob")]

    game = DummyGame(*players, hand_size=2)
    game.deal(3)
    assert all(len(player.hand) == 3 for player in game.players)


def test_game_shuffle():
    deck = DummyDeck()
    game = DummyGame(deck)
    game.shuffle()
    assert list(game.deck) != sorted(game.deck)
    assert len(game.deck) == len(deck)
    assert all(card in deck for card in game.deck)


def test_game_play():
    players = [DummyPlayer("Alice"), DummyPlayer("Bob")]
    game = DummyGame(*players, hand_size=2)
    game.deal(2)
    dealt_card = players[0].hand[0]
    game.play(players[0], players[0].hand[0])
    assert len(players[0].hand) == 1
    assert len(game.discard_pile) == 1
    assert (dealt_card in game.discard_pile and dealt_card not in
            players[0].hand)


def test_game_get_trump():
    game1 = DummyGame()
    assert game1.get_trump() is None

    game2 = DummyGame(trump="Red")
    assert game2.get_trump() == "Red"


def test_game_set_trump():
    game = DummyGame()
    game.set_trump("Red")
    assert game.trump == "Red"

    with pytest.raises(ValueError):
        game.set_trump("InvalidSuit")


def test_game_apply_trump():
    game = DummyGame(trump="Red")
    game.apply_trump()
    assert all(card.trump for card in game.deck
               if card.get_suit() == "Red")
    assert not any(card.trump for card in game.deck
                   if card.get_suit() != "Red")
    assert all(card.trump for player in game.players for card in player.hand
               if card.get_suit() == "Red")
    assert not any(card.trump for player in game.players for card in
                   player.hand if card.get_suit() != "Red")


def test_game_get_current_player():
    players = [DummyPlayer("Alice"), DummyPlayer("Bob")]
    game = DummyGame(*players, hand_size=2)
    assert game.get_current_player() == players[0]


def test_game_set_current_player():
    players = [DummyPlayer("Alice"), DummyPlayer("Bob")]
    game = DummyGame(*players, hand_size=2)
    game.set_current_player(players[1])
    assert game.current_player_index == 1


def test_game_get_players():
    players = [DummyPlayer("Alice"), DummyPlayer("Bob")]
    game = DummyGame(*players, hand_size=2)
    assert game.get_players() == players


def test_game_get_deck():
    deck = DummyDeck()
    game = DummyGame(deck)
    assert game.get_deck() == deck


def test_game_set_deck():
    deck = DummyDeck()
    game = DummyGame(deck=DummyDeck([]))
    assert game.deck != deck
    game.set_deck(deck)
    assert game.deck == deck


def test_game_str():
    players = [DummyPlayer("Alice"), DummyPlayer("Bob")]
    game = DummyGame(*players, hand_size=2)
    assert str(game) == "Game of 2 players"


def test_game_repr():
    deck = DummyDeck()
    discard_pile = DummyDeck([])
    players = [DummyPlayer("Alice"), DummyPlayer("Bob")]
    game = DummyGame(*players, deck=deck, discard_pile=discard_pile,
                     trump="Green", hand_size=2, starting_player_index=1)
    game_repr = repr(game)

    assert game_repr.startswith("DummyGame(card_type=<class ")
    assert "deck_type=<class " in game_repr
    assert "deck=DummyDeck(card_type=<class " in game_repr
    assert "cards=[DummyCard(" in game_repr
    assert "DummyCard(rank=0, suit=0)" in game_repr
    assert "discard_pile=DummyDeck(card_type=<class " in game_repr
    assert "trump='Green'" in game_repr
    assert "hand_size=2" in game_repr
    assert "starting_player_index=1" in game_repr
    assert "DummyPlayer('Alice', hand=[], score=0)" in game_repr
    assert "DummyPlayer('Alice', hand=[], score=0)" in game_repr
