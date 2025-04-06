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

from typing import Any, Literal, Optional, Sequence, Union

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
T_UnoSuitsWild = Literal["Red", "Green", "Blue", "Yellow"]


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
    __slots__ = ("wild",)

    def __init__(self, rank: Union[T_UnoRanks, int], suit: Union[T_UnoSuits, int
    ]) -> None:
        """
        Initialise the UNO card with a rank and suit.
        :param rank: The rank of the card.
        :param suit: The suit of the card.
        """
        self.wild: bool = ...

    def is_wild(self) -> bool:
        """
        Check if the card is a Wild card.
        :return: True if the card is a Wild card, False otherwise.
        """

    def effect(self,
               game: UnoGame,
               player: UnoPlayer,
               *args: Any) -> None:
        """
        Apply the effect of the card in the game.
        :param game: The game instance.
        :param player: The player who played the card.
        :param args: Additional arguments for the effect.
        """


class NumberCard(UnoCard):
    """A class representing a numbered UNO card."""

    def __init__(self, rank: Union[T_UnoRanks, int], suit: Union[T_UnoSuits, int
    ]) -> None:
        """
        Initialise the numbered UNO card with a rank and suit.
        :param rank: The rank of the card.
        :param suit: The suit of the card.
        """


class DrawTwoCard(UnoCard):
    """A class representing a Draw Two UNO card."""

    def __init__(self, suit: Union[T_UnoSuits, int]) -> None:
        """
        Initialise the Draw Two UNO card with a suit.
        :param suit: The suit of the card.
        """


class SkipCard(UnoCard):
    """A class representing a Skip UNO card."""

    def __init__(self, suit: Union[T_UnoSuits, int]) -> None:
        """
        Initialise the Skip UNO card with a suit.
        :param suit: The suit of the card.
        """


class ReverseCard(UnoCard):
    """A class representing a Reverse UNO card."""

    def __init__(self, suit: Union[T_UnoSuits, int]) -> None:
        """
        Initialise the Reverse UNO card with a suit.
        :param suit: The suit of the card.
        """


class WildCard(UnoCard):
    """A class representing a Wild UNO card."""

    def __init__(self) -> None:
        """Initialise the Wild UNO card."""


class WildDrawFourCard(UnoCard):
    """A class representing a Wild Draw Four UNO card."""

    def __init__(self) -> None:
        """Initialise the Wild Draw Four UNO card."""


class UnoDeck(
    GenericDeck[UnoCard],
    metaclass=DeckMeta,
    card_type=UnoCard
):
    """
    A class representing a UNO deck of cards.
    :param cards: Optional list of cards to initialise the deck with.
    """

    def __init__(self, cards: Optional[Sequence[UnoCard]] = None) -> None:
        """
        Initialise the UNO deck with a standard set of cards.
        :param cards: Optional list of cards to initialise the deck with.
        """


class UnoPlayer(GenericPlayer[UnoCard]):
    """A class representing a UNO player."""
    __slots__ = ("uno",)

    def __init__(self, name: str, hand: Optional[Sequence[UnoCard]] = None) -> \
            None:
        """
        Initialise the UNO player with a name, hand of cards, and score.
        :param name: The name of the player.
        :param hand: The initial hand of cards for the player.
        """
        self.uno: bool = False  # Indicates if the player has called "UNO"

    def call_uno(self) -> bool:
        """
        Call "UNO" when the player has one card left.
        :return: True if the player has called "UNO" correctly, False otherwise.
        """

    def reset_uno(self) -> UnoPlayer:
        """
        Resets the "UNO" state to false
        :return: The player instance
        """


class UnoGame(GenericGame[UnoCard]):
    """A class representing a UNO game."""

    def __init__(self,
                 *players: GenericPlayer[UnoCard],
                 draw_pile: Optional[GenericDeck[UnoCard]] = None,
                 discard_pile: Optional[GenericDeck[UnoCard]] = None,
                 hand_size: int = 7) -> None:
        """
        Initialise the UNO game with a deck, discard pile, hand size, and
        players.
        :param players: The players participating in the game.
        :param draw_pile: The draw pile for the game.
        :param discard_pile: The discard pile for the game.
        :param hand_size: The number of cards each player starts with.
        """
        self.direction: Literal[1, -1] = 1
        self.draw_count: int = 0

    def check_valid_play(self, card1: UnoCard,
                         card2: Optional[UnoCard] = None) -> bool:
        """
        Check if a card can be played on top of another card.
        :param card1: The card being played.
        :param card2: The card on top of the discard pile.
        :return: True if the card can be played, False otherwise.
        """

    def discard_cards(self, *cards: UnoCard) -> UnoGame:
        """
        Add one or more cards to the discard pile.
        :param cards: The card(s) to discard.
        :return: The current game instance with updated discard pile.
        """

    def get_top_card(self) -> Optional[UnoCard]:
        """
        Get the top card from the discard pile.
        :return: The top card from the discard pile or None if empty.
        """

    # TODO: Resolve typing issue
    def get_current_player(self) -> UnoPlayer: ...

    def get_next_player(self) -> UnoPlayer:
        """
        Get the next player in the game based on the current direction.
        :return: The next player.
        """

    def play_card(self,
                  card: UnoCard,
                  player: GenericPlayer[UnoCard] | None = None,
                  *args: Any) -> bool:
        """
        Play a card from the player's hand to the discard pile.
        :param player: The player playing the card. If None, the current player
            is used.
        :param card: The card to play.
        :param args: Additional arguments for the card effect.
        :return: True if the card was played successfully, False otherwise.
        """

    def draw_cards(self, player: GenericPlayer[UnoCard], n: int = 1) -> \
            Optional[Sequence[UnoCard]]:
        """
        Draw a card from the deck and add it to the player's hand.
        :param player: The player drawing the card.
        :param n: The number of cards to draw (default is 1).
        :return: The drawn card or None if the deck is empty.
        """

    def reverse_direction(self) -> UnoGame:
        """
        Reverse the direction of play.
        :return: The current game instance with updated direction.
        """

    def start_game(self) -> UnoGame:
        """
        Start the game by dealing initial cards and setting up the discard pile.
        :return: The game instance.
        """

    def next_player(self) -> UnoGame:
        """
        Move to the next player in the game.
        :return: The game instance with the updated current player.
        """

    def draw_instead_of_play(self,
                             player: Optional[GenericPlayer[UnoCard]] = None
                             ) -> Sequence[UnoCard]:
        """
        Called when a player chooses to draw instead of playing a card.
        If there's an accumulated draw count from Draw Two cards, handle that.
        Otherwise, just draw one card and continue play.
        :param player: The player who is drawing a card.
        :return: The drawn cards (list) or an empty list if the draw pile is
            empty.
        """

    def determine_winner(self) -> Optional[GenericPlayer[UnoCard]]:
        """
        Determine the winner of the game based on the players' scores.
        :return: The winning player or None if no winner is determined.
        """

    def end_game(self) -> None:
        """End the game and announce the winner."""
