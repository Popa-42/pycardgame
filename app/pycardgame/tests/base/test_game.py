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

from ...src.base import (
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
    def effect(self, game, player, *args):  # pragma: no cover
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
    def __init__(self, *players, draw_pile=None, discard_pile=None, trump=None,
                 hand_size=4, starting_player_index=0, do_not_shuffle=False):
        super().__init__(DummyCard, DummyDeck, draw_pile, discard_pile, trump,
                         hand_size, starting_player_index, do_not_shuffle,
                         *players)

    def check_valid_play(self, card1, card2):
        return card1.suit == card2.suit or card1.rank == card2.rank

    def start_game(self): ...
    def end_game(self): ...


def test_game_init():
    deck = DummyDeck()
    empty_deck = DummyDeck(cards=[])
    players = [DummyPlayer("Alice"), DummyPlayer("Bob")]

    game = DummyGame(*players, draw_pile=deck, discard_pile=empty_deck,
                     trump="Green", hand_size=2, starting_player_index=1)
    assert game.draw_pile == deck
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


def test_game_check_valid_play():
    card1 = DummyCard(0, 0)
    card2 = DummyCard(0, 1)
    card3 = DummyCard(1, 0)
    game = DummyGame()

    assert game.check_valid_play(card1, card2) is True
    assert game.check_valid_play(card1, card3) is True
    assert game.check_valid_play(card2, card3) is False


def test_game_discard_cards():
    game = DummyGame()
    discard_card = DummyCard(0, 0)
    game.discard_cards(discard_card)
    assert discard_card in game.discard_pile


def test_game_get_discard_pile():
    deck = DummyDeck()
    discard_pile = DummyDeck(cards=[])
    players = [DummyPlayer("Alice"), DummyPlayer("Bob")]
    game = DummyGame(*players, draw_pile=deck, discard_pile=discard_pile)
    assert game.get_discard_pile() == discard_pile


def test_game_get_top_card():
    players = [DummyPlayer("Alice"), DummyPlayer("Bob")]
    game = DummyGame(*players)
    top_card = game.get_top_card()
    assert top_card is None
    game.discard_pile.add(DummyCard(0, 0))
    top_card = game.get_top_card()
    assert isinstance(top_card, DummyCard)
    assert top_card in game.draw_pile


def test_game_reshuffle_discard_pile():
    players = [DummyPlayer("Alice"), DummyPlayer("Bob")]
    deck = DummyDeck([])
    discard_pile = DummyDeck([DummyCard(0, 0), DummyCard(1, 1)])
    game = DummyGame(*players, draw_pile=deck, discard_pile=discard_pile)
    game.reshuffle_discard_pile()
    assert len(game.draw_pile) > 0
    assert len(game.discard_pile) == 0
    assert all(card in game.draw_pile for card in discard_pile.cards)


def test_game_draw_cards():
    players = [DummyPlayer("Alice"), DummyPlayer("Bob")]
    deck = DummyDeck([DummyCard(0, 0), DummyCard(1, 1)])
    discard_pile = DummyDeck([DummyCard(2, 2)])
    game = DummyGame(*players, draw_pile=deck, discard_pile=discard_pile)
    game.draw_cards(n=2)
    assert len(players[0].hand) == 2
    assert len(game.draw_pile) == 0
    assert len(game.discard_pile) == 1
    game.draw_cards(players[0])
    assert len(players[0].hand) == 3


def test_game_deal_initial_cards():
    players = [DummyPlayer("Alice"), DummyPlayer("Bob")]
    deck = DummyDeck()
    game = DummyGame(*players, hand_size=2)
    game.deal_initial_cards()
    assert all(len(player.hand) == 2 for player in players)
    assert len(game.draw_pile) < len(deck)


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
    game = DummyGame(draw_pile=deck)
    game.shuffle()
    assert list(game.draw_pile) != sorted(game.draw_pile)
    assert len(game.draw_pile) == len(deck)
    assert all(card in deck for card in game.draw_pile)


def test_game_play():
    player1 = DummyPlayer("Alice", [DummyCard(0, 0)])
    player2 = DummyPlayer("Bob", [DummyCard(1, 1)])
    players = [player1, player2]
    game = DummyGame(*players, hand_size=2)
    dealt_card = player1.hand[0]
    game.discard_cards(dealt_card)
    assert game.play_card(dealt_card, player1) is True
    assert len(player1.hand) == 0
    assert len(game.discard_pile) == 2
    assert (dealt_card in game.discard_pile and dealt_card not in
            player1.hand)

    assert game.play_card(player2.hand[0], player2) is False


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
    player1 = DummyPlayer("Alice", [DummyCard(0, 0)])
    player2 = DummyPlayer("Bob", [DummyCard(1, 1)])
    players = [player1, player2]
    deck = DummyDeck([DummyCard(0, 0), DummyCard(1, 1)])
    discard_pile = DummyDeck([DummyCard(0, 2), DummyCard(1, 2)])
    game = DummyGame(*players, trump="Red", draw_pile=deck,
                     discard_pile=discard_pile)

    game.apply_trump()

    assert all(card.is_trump() for card in game.draw_pile
               if card.get_suit() == "Red")
    assert not any(card.is_trump() for card in game.draw_pile
                   if card.get_suit() != "Red")

    assert all(card.is_trump() for card in game.discard_pile
               if card.get_suit() == "Red")
    assert not any(card.is_trump() for card in game.discard_pile
                   if card.get_suit() != "Red")
    
    assert all(card.trump for player in game.players for card in player.hand
               if card.get_suit() == "Red")
    assert not any(card.trump for player in game.players for card in
                   player.hand if card.get_suit() != "Red")


def test_game_change_trump():
    player1 = DummyPlayer("Alice", [DummyCard(0, 0)])
    player2 = DummyPlayer("Bob", [DummyCard(1, 1)])
    players = [player1, player2]
    deck = DummyDeck([DummyCard(0, 0), DummyCard(1, 1)])
    discard_pile = DummyDeck([DummyCard(0, 2), DummyCard(1, 2)])
    game = DummyGame(*players, trump="Red", draw_pile=deck,
                     discard_pile=discard_pile)

    game.change_trump("Green")
    assert game.trump == "Green"

    assert all(card.trump for card in game.draw_pile
               if card.get_suit() == "Green")
    assert not any(card.trump for card in game.draw_pile
                   if card.get_suit() != "Green")

    assert all(card.trump for card in game.discard_pile
               if card.get_suit() == "Green")
    assert not any(card.trump for card in game.discard_pile
                   if card.get_suit() != "Green")

    assert all(card.trump for player in game.players for card in player.hand
               if card.get_suit() == "Green")
    assert not any(card.trump for player in game.players for card in
                   player.hand if card.get_suit() != "Green")

    with pytest.raises(ValueError):
        game.change_trump("InvalidSuit")


def test_game_get_current_player():
    players = [DummyPlayer("Alice"), DummyPlayer("Bob")]
    game = DummyGame(*players, hand_size=2)
    assert game.get_current_player() == players[0]


def test_game_set_current_player():
    players = [DummyPlayer("Alice"), DummyPlayer("Bob")]
    game = DummyGame(*players, hand_size=2)
    game.set_current_player(players[1])
    assert game.current_player_index == 1

    game.set_current_player(0)
    assert game.current_player_index == 0

    with pytest.raises(ValueError):
        game.set_current_player(10)

    with pytest.raises(TypeError):
        game.set_current_player("InvalidPlayer")  # type: ignore


def test_game_get_players():
    players = [DummyPlayer("Alice"), DummyPlayer("Bob")]
    game = DummyGame(*players, hand_size=2)
    assert game.get_players() == players


def test_game_get_deck():
    deck = DummyDeck()
    game = DummyGame(draw_pile=deck)
    assert game.get_draw_pile() == deck


def test_game_set_deck():
    deck = DummyDeck()
    game = DummyGame(draw_pile=DummyDeck([]))
    assert game.draw_pile != deck
    game.set_draw_pile(deck)
    assert game.draw_pile == deck


def test_game_str():
    players = [DummyPlayer("Alice"), DummyPlayer("Bob")]
    game = DummyGame(*players, hand_size=2)
    assert str(game) == "Game of 2 players"


def test_game_repr():
    deck = DummyDeck()
    discard_pile = DummyDeck([])
    players = [DummyPlayer("Alice"), DummyPlayer("Bob")]
    game = DummyGame(*players, draw_pile=deck, discard_pile=discard_pile,
                     trump="Green", hand_size=2, starting_player_index=1)
    game_repr = repr(game)

    assert game_repr.startswith("DummyGame(card_type=<class ")
    assert "deck_type=<class " in game_repr
    assert "draw_pile=DummyDeck(card_type=<class " in game_repr
    assert "cards=[DummyCard(" in game_repr
    assert "DummyCard(rank=0, suit=0)" in game_repr
    assert "discard_pile=DummyDeck(card_type=<class " in game_repr
    assert "trump='Green'" in game_repr
    assert "hand_size=2" in game_repr
    assert "starting_player_index=1" in game_repr
    assert "DummyPlayer('Alice', hand=[], score=0)" in game_repr
    assert "DummyPlayer('Alice', hand=[], score=0)" in game_repr
