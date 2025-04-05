import pytest

from .... import (
    DrawTwoCard,
    NumberCard,
    ReverseCard,
    SkipCard,
    UnoCard,
    UnoDeck,
    UnoGame,
    UnoPlayer,
    WildCard,
    WildDrawFourCard,
)


def test_uno_card_init():
    card1 = UnoCard("5", "Red")
    card2 = UnoCard(5, "Red")
    card3 = UnoCard("5", 0)
    assert card1.rank == 5
    assert card1.suit == 0
    assert str(card1) == "Red 5"
    assert repr(card1) == "UnoCard(rank=5, suit=0)"
    assert card1 == card2 == card3

    with pytest.raises(ValueError):
        UnoCard(["InvalidRankType"], "Red")  # type: ignore

    with pytest.raises(ValueError):
        UnoCard("5", ["InvalidSuitType"])  # type: ignore


def test_uno_card_is_wild():
    card = UnoCard("2", "Green")
    assert not card.is_wild()


def test_uno_card_str():
    card1 = UnoCard("2", "Green")
    assert str(card1) == "Green 2"

    card2 = UnoCard("Wild Draw Four", "Wild")
    card2.wild = True
    assert str(card2) == "Wild Draw Four"

    card3 = UnoCard("Skip", "Red")
    assert str(card3) == "Red Skip"


def test_number_card_init():
    card = NumberCard("5", "Red")
    assert card.rank == 5
    assert card.suit == 0
    assert card.wild is False
    assert str(card) == "Red 5"
    assert repr(card) == "NumberCard(rank=5, suit=0)"


def test_draw_two_card_init():
    card = DrawTwoCard("Red")
    assert card.rank == 12
    assert card.suit == 0
    assert card.wild is False
    assert str(card) == "Red Draw Two"
    assert repr(card) == "DrawTwoCard(rank=12, suit=0)"


def test_draw_two_card_effect():
    player1 = UnoPlayer("Player 1", [DrawTwoCard("Red")])
    player2 = UnoPlayer("Player 2")
    deck = UnoDeck()
    game = UnoGame(player1, player2, draw_pile=deck)
    game.discard_cards(UnoCard("5", "Red"))
    game.play_card(DrawTwoCard("Red"))
    assert len(player1) == 0
    assert len(player2) == 2


def test_skip_card_init():
    card = SkipCard("Red")
    assert card.rank == 10
    assert card.suit == 0
    assert card.wild is False
    assert str(card) == "Red Skip"
    assert repr(card) == "SkipCard(rank=10, suit=0)"


def test_skip_card_effect():
    player1 = UnoPlayer("Player 1", [SkipCard("Red")])
    player2 = UnoPlayer("Player 2")
    deck = UnoDeck()
    game = UnoGame(player1, player2, draw_pile=deck)
    game.discard_cards(UnoCard("5", "Red"))
    game.play_card(SkipCard("Red"))
    assert game.current_player_index == 1


def test_reverse_card_init():
    card = ReverseCard("Red")
    assert card.rank == 11
    assert card.suit == 0
    assert card.wild is False
    assert str(card) == "Red Reverse"
    assert repr(card) == "ReverseCard(rank=11, suit=0)"


def test_reverse_card_effect():
    player1 = UnoPlayer("Player 1", [ReverseCard("Red")])
    player2 = UnoPlayer("Player 2")
    deck = UnoDeck()
    game = UnoGame(player1, player2, draw_pile=deck)
    game.discard_cards(UnoCard("5", "Red"))
    game.play_card(ReverseCard("Red"))
    assert game.direction == -1


def test_wild_card_init():
    card = WildCard()
    assert card.rank == 13
    assert card.suit == 4
    assert card.wild is True
    assert str(card) == "Wild"
    assert repr(card) == "WildCard(rank=13, suit=4)"


def test_wild_card_effect():
    player1 = UnoPlayer("Player 1", [WildCard()] * 2)
    player2 = UnoPlayer("Player 2")
    deck = UnoDeck()
    game = UnoGame(player1, player2, draw_pile=deck)
    game.discard_cards(UnoCard("5", "Red"))
    game.play_card(WildCard(), player1, "Blue")
    assert game.discard_pile.cards[0].suit == 2

    with pytest.raises(ValueError):
        game.play_card(WildCard(), player1)


def test_wild_draw_four_card_init():
    card = WildDrawFourCard()
    assert card.rank == 14
    assert card.suit == 4
    assert card.wild is True
    assert str(card) == "Wild Draw Four"
    assert repr(card) == "WildDrawFourCard(rank=14, suit=4)"


def test_wild_draw_four_card_effect():
    player1 = UnoPlayer("Player 1", [WildDrawFourCard()] * 2)
    player2 = UnoPlayer("Player 2")
    deck = UnoDeck()
    game = UnoGame(player1, player2, draw_pile=deck)
    game.discard_cards(UnoCard("5", "Red"))
    game.play_card(WildDrawFourCard(), player1, "Blue")
    assert game.discard_pile.cards[0].suit == 2
    assert len(player2) == 4

    with pytest.raises(ValueError):
        game.play_card(WildDrawFourCard(), player1)
