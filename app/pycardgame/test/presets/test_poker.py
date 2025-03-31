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
