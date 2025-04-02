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

from __future__ import annotations

from typing import List, Literal, Optional, TypeVar, Union

from .base import (
    CardMeta,
    DeckMeta,
    GenericCard,
    GenericDeck,
    GenericGame,
    GenericPlayer,
)

T_UnoRanks = Literal["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "Skip",
                     "Reverse", "Draw Two", "Wild", "Wild Draw Four"]
T_UnoSuits = Literal["Red", "Green", "Blue", "Yellow", "Wild"]


class UnoCard(
    GenericCard[T_UnoRanks, T_UnoSuits],
    metaclass=CardMeta,
    rank_type=T_UnoRanks,
    suit_type=T_UnoSuits
):
    """
    A class representing a UNO card.
    :param rank: The rank of the card.
    :param suit: The suit of the card.
    """

    def __init__(self, rank: Union[T_UnoRanks, int], suit: Union[T_UnoSuits, int
    ]) -> None:
        """
        Initialize the UNO card with a rank and suit.
        :param rank: The rank of the card.
        :param suit: The suit of the card.
        """
        pass


class UnoDeck(
    GenericDeck[UnoCard],
    metaclass=DeckMeta,
    card_type=UnoCard
):
    """A class representing a UNO deck."""

    def __init__(self, cards: List[UnoCard] = None) -> None:
        """
        Initialize the UNO deck with a standard set of cards.
        :param cards: Optional list of cards to initialize the deck with.
        """
        pass


class UnoPlayer(GenericPlayer[UnoCard]):
    """A class representing a UNO player."""

    def __init__(self, name: str, hand: Optional[List[UnoCard]] = None,
                 score: int = 0) -> None:
        """
        Initialize the UNO player with a name, hand of cards, and score.
        :param name: The name of the player.
        :param hand: The initial hand of cards for the player.
        :param score: The initial score for the player.
        """
        pass


_UnoDeck = TypeVar("_UnoDeck", bound=GenericDeck[UnoCard])
_UnoPlayer = TypeVar("_UnoPlayer", bound=GenericPlayer[UnoCard])


class UnoGame(GenericGame[UnoCard]):
    """A class representing a UNO game."""

    def __init__(self,
                 *players: _UnoPlayer,
                 deck: Optional[_UnoDeck] = None,
                 discard_pile: Optional[_UnoDeck] = None,
                 hand_size: int = 7) -> None:
        """
        Initialize the UNO game with a deck, discard pile, hand size, and
        players.
        :param players: The players participating in the game.
        :param deck: The deck of cards for the game.
        :param discard_pile: The discard pile for the game.
        :param hand_size: The number of cards each player starts with.
        """
        self.direction: int = ...

    @staticmethod
    def check_valid_play(card1: UnoCard, card2: UnoCard) -> bool:
        """
        Check if a card can be played on top of another card.
        :param card1: The card being played.
        :param card2: The card on top of the discard pile.
        :return: True if the card can be played, False otherwise.
        """
        pass

    def play_card(self, player: _UnoPlayer, card: UnoCard) -> bool:
        """
        Play a card from the player's hand to the discard pile.
        :param player: The player playing the card.
        :param card: The card to play.
        :return: True if the card was played successfully, False otherwise.
        """
        pass

    def draw_card(self, player: _UnoPlayer, n: int = 1) -> Optional[UnoCard]:
        """
        Draw a card from the deck and add it to the player's hand.
        :param player: The player drawing the card.
        :param n: The number of cards to draw (default is 1).
        :return: The drawn card or None if the deck is empty.
        """
        pass

    def reverse_direction(self) -> UnoGame:
        """
        Reverse the direction of play.
        :return: The current game instance with updated direction.
        """
        pass

    def start_game(self) -> UnoGame:
        """
        Start the game by dealing initial cards and setting up the discard pile.
        :return: The game instance.
        """
        pass

    def next_player(self) -> UnoGame:
        """
        Move to the next player in the game.
        :return: The game instance with the updated current player.
        """
        pass

    def determine_winner(self) -> Optional[_UnoPlayer]:
        """
        Determine the winner of the game based on the players' scores.
        :return: The winning player or None if no winner is determined.
        """
        pass

    def end_game(self) -> None:
        """End the game and announce the winner."""
        pass
