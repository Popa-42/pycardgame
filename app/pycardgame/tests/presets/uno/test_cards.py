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
    game.play_card(DrawTwoCard("Red"), player1)

    assert len(player1) == 0
    assert len(player2) == 0
    assert game.draw_count == 2

    game.next_player()
    drawn = game.draw_instead_of_play()

    assert len(drawn) == 2
    assert len(player2) == 2
    assert game.draw_count == 0


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


def test_draw_two_card_stacking():
    hand1 = [DrawTwoCard("Red"), NumberCard("5", "Yellow")]
    hand2 = [DrawTwoCard("Yellow"), NumberCard("6", "Blue")]
    hand3 = [NumberCard("7", "Yellow")]  # No Draw Two card

    player1 = UnoPlayer("Player 1", hand1)
    player2 = UnoPlayer("Player 2", hand2)
    player3 = UnoPlayer("Player 3", hand3)

    deck_cards = [
        NumberCard("1", "Blue"), NumberCard("2", "Green"),
        NumberCard("3", "Red"), NumberCard("4", "Yellow"),
        NumberCard("5", "Blue"), NumberCard("6", "Green"),
        NumberCard("7", "Red"), NumberCard("8", "Yellow"),
        NumberCard("9", "Blue"), NumberCard("1", "Green")
    ]
    deck = UnoDeck(deck_cards)
    game = UnoGame(player1, player2, player3, draw_pile=deck)

    game.discard_cards(NumberCard("4", "Red"))

    game.play_card(DrawTwoCard("Red"))
    assert game.draw_count == 2
    assert len(player1) == 1

    game.next_player()

    game.play_card(DrawTwoCard("Yellow"))
    assert game.draw_count == 4
    assert len(player2) == 1

    game.next_player()

    assert len(player3) == 1

    drawn_cards = game.draw_instead_of_play()

    assert len(drawn_cards) == 4
    assert len(player3) == 5
    assert game.draw_count == 0

    current_player = game.get_current_player()
    initial_hand_size = len(current_player)

    drawn = game.draw_instead_of_play()

    assert len(drawn) == 1
    assert len(current_player) == initial_hand_size + 1
