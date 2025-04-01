import pytest

from ... import UnoCard, UnoDeck, UnoGame, UnoPlayer


def test_uno_card():
    card = UnoCard("5", "Red")
    assert card.rank == 5
    assert card.suit == 0
    assert str(card) == "Red 5"
    assert repr(card) == "UnoCard(rank=5, suit=0)"


def test_uno_deck():
    deck = UnoDeck()
    assert len(deck.cards) == 108
    assert str(deck) == "UNO Deck with 108 cards"
    assert repr(deck) == f"UnoDeck(cards={deck.cards!r})"
    assert isinstance(deck.cards[0], UnoCard)
    assert deck.cards[0].get_rank() in ["0", "1", "2", "3", "4", "5", "6", "7",
                                        "8", "9", "Skip", "Reverse", "Draw Two"]
    assert deck.cards[0].get_suit() in ["Red", "Green", "Blue", "Yellow"]


def test_uno_player():
    player = UnoPlayer("Alice")
    assert player.name == "Alice"
    assert len(player.hand) == 0
    assert player.score == 0
    assert str(player) == "Player Alice with 0 cards"
    assert repr(player) == "UnoPlayer('Alice', hand=[], score=0)"


def test_uno_game():
    deck = UnoDeck()
    player1 = UnoPlayer("Alice")
    player2 = UnoPlayer("Bob")
    game = UnoGame(deck, None, 7, player1, player2)

    assert game.deck is deck
    assert game.discard_pile.cards == []
    assert game.hand_size == 7
    assert game.current_player_index == 0
    assert game.players == [player1, player2]
