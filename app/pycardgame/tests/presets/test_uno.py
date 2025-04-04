import pytest

from ... import DrawTwoCard, NumberCard, UnoCard, UnoDeck, UnoGame, UnoPlayer


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
    card = NumberCard("Draw Two", "Red")
    assert card.rank == 12
    assert card.suit == 0
    assert card.wild is False
    assert str(card) == "Red Draw Two"
    assert repr(card) == "NumberCard(rank=12, suit=0)"

def test_draw_two_card_effect():
    # Check if card.effect() works
    player1 = UnoPlayer("Player 1", [DrawTwoCard("Red")])
    print(player1)
    player2 = UnoPlayer("Player 2")
    deck = UnoDeck()
    game = UnoGame(player1, player2, deck=deck)
    game.start_game()
    game.play_card(DrawTwoCard("Red"))
    print(player1)
    print(player2)
