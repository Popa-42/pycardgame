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

T_Ranks = Literal["7", "8", "9", "10", "J", "Q", "K", "A"]
T_Suits = Literal["Diamonds", "Hearts", "Spades", "Clubs"]


class TestingCard(
    GenericCard[T_Ranks, T_Suits],
    metaclass=CardMeta,
    rank_type=T_Ranks,
    suit_type=T_Suits
):
    ...


class TestingDeck(
    GenericDeck[TestingCard],
    metaclass=DeckMeta,
    card_type=TestingCard
):
    ...


class TestingPlayer(GenericPlayer[TestingCard]):
    ...


class TestingGame(GenericGame[TestingCard]):
    def __init__(self, deck=None, discard_pile=None, trump=None, hand_size=4,
                 starting_player_index=0, *players):
        super().__init__(TestingCard, TestingDeck, deck, discard_pile, trump,
                         hand_size, starting_player_index, *players)


def test_game_init():
    deck = TestingDeck()
    empty_deck = TestingDeck(cards=[])
    players = [TestingPlayer("Alice"), TestingPlayer("Bob")]

    game = TestingGame(deck, empty_deck, "Hearts", 6, 1, *players)
    assert game.deck == deck
    assert game.discard_pile == empty_deck
    assert game.trump == "Hearts"
    assert game.hand_size == 6
    assert game.players == players
    assert game.current_player_index == 1

    with pytest.raises(ValueError):
        TestingGame(deck, empty_deck, "InvalidSuit", 6, 1, *players)

    with pytest.raises(ValueError):
        TestingGame(deck, empty_deck, "Hearts", 6, 3, *players)


def test_game_deal_initial_cards():
    players = [TestingPlayer("Alice"), TestingPlayer("Bob")]
    deck = TestingDeck()
    game = TestingGame(deck, None, None, 4, 0, *players)
    game.deal_initial_cards()
    assert all(len(player.hand) == 4 for player in players)
    assert len(game.deck) == len(deck)


def test_game_add_players():
    players = [TestingPlayer("Alice"), TestingPlayer("Bob")]
    game = TestingGame(None, None, None, 4, 0, *players)
    new_players = [TestingPlayer("Charlie"), TestingPlayer("David")]
    game.add_players(*new_players)
    assert game.players == players + new_players


def test_game_remove_players():
    players = [TestingPlayer("Alice"), TestingPlayer("Bob")]
    game = TestingGame(None, None, None, 4, 0, *players)
    game.remove_players(players[0])
    assert game.players == players[1:]


def test_game_deal():
    players = [TestingPlayer("Alice"), TestingPlayer("Bob")]

    game = TestingGame(None, None, None, 6, 0, *players)
    game.deal(2)
    assert all(len(player.hand) == 2 for player in game.players)


def test_game_shuffle():
    deck = TestingDeck()
    game = TestingGame(deck)
    game.shuffle()
    assert list(game.deck) != sorted(game.deck)
    assert len(game.deck) == len(deck)
    assert all(card in deck for card in game.deck)


def test_game_play():
    players = [TestingPlayer("Alice"), TestingPlayer("Bob")]
    game = TestingGame(None, None, None, 4, 0, *players)
    game.deal(2)
    dealt_card = players[0].hand[0]
    game.play(players[0], players[0].hand[0])
    assert len(players[0].hand) == 1
    assert len(game.discard_pile) == 1
    assert dealt_card in game.discard_pile and dealt_card not in players[0].hand


def test_game_get_trump():
    game1 = TestingGame()
    assert game1.get_trump() is None

    game2 = TestingGame(trump="Hearts")
    assert game2.get_trump() == "Hearts"


def test_game_set_trump():
    game = TestingGame()
    game.set_trump("Hearts")
    assert game.trump == "Hearts"

    with pytest.raises(ValueError):
        game.set_trump("InvalidSuit")


def test_game_apply_trump():
    game = TestingGame(TestingDeck(), TestingDeck([]), trump="Hearts")
    game.apply_trump()
    assert all(card.trump for card in game.deck
               if card.get_suit() == "Hearts")
    assert not any(card.trump for card in game.deck
                   if card.get_suit() != "Hearts")
    assert all(card.trump for player in game.players for card in player.hand
               if card.get_suit() == "Hearts")
    assert not any(card.trump for player in game.players for card in player.hand
                   if card.get_suit() != "Hearts")


def test_game_get_current_player():
    players = [TestingPlayer("Alice"), TestingPlayer("Bob")]
    game = TestingGame(None, None, None, 4, 0, *players)
    assert game.get_current_player() == players[0]


def test_game_set_current_player():
    players = [TestingPlayer("Alice"), TestingPlayer("Bob")]
    game = TestingGame(None, None, None, 4, 0, *players)
    game.set_current_player(players[1])
    assert game.current_player_index == 1


def test_game_get_players():
    players = [TestingPlayer("Alice"), TestingPlayer("Bob")]
    game = TestingGame(None, None, None, 4, 0, *players)
    assert game.get_players() == players


def test_game_get_deck():
    deck = TestingDeck()
    game = TestingGame(deck)
    assert game.get_deck() == deck


def test_game_set_deck():
    deck = TestingDeck()
    game = TestingGame(TestingDeck([]))
    assert game.deck != deck
    game.set_deck(deck)
    assert game.deck == deck


def test_game_str():
    players = [TestingPlayer("Alice"), TestingPlayer("Bob")]
    game = TestingGame(None, None, None, 4, 0, *players)
    assert str(game) == "Game of 2 players"


def test_game_repr():
    deck = TestingDeck()
    discard_pile = TestingDeck([])
    players = [TestingPlayer("Alice"), TestingPlayer("Bob")]
    game = TestingGame(deck, discard_pile, "Hearts", 4, 0, *players)
    game_repr = repr(game)

    assert game_repr.startswith("TestingGame(card_type=<class ")
    assert "deck_type=<class " in game_repr
    assert "deck=TestingDeck(card_type=<class " in game_repr
    assert "cards=[TestingCard(" in game_repr
    assert "TestingCard(rank=0, suit=0)" in game_repr
    assert "discard_pile=TestingDeck(card_type=<class " in game_repr
    assert "trump='Hearts'" in game_repr
    assert "hand_size=4" in game_repr
    assert "starting_player_index=0" in game_repr
    assert "TestingPlayer('Alice', hand=[], score=0)" in game_repr
    assert "TestingPlayer('Alice', hand=[], score=0)" in game_repr
