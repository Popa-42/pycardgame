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

from typing import List, Literal, Optional

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
    """A class representing a UNO card."""
    pass


class UnoDeck(
    GenericDeck[UnoCard],
    metaclass=DeckMeta,
    card_type=UnoCard
):
    """A class representing a UNO deck."""

    def __init__(self, cards=None) -> None:
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


class UnoGame(GenericGame[UnoCard]):
    """A class representing a UNO game."""

    def __init__(self, deck: Optional[UnoDeck], discard_pile: Optional[
        UnoDeck], hand_size: int = 7, *players: UnoPlayer) -> None:
        """
        Initialize the UNO game with a deck, discard pile, hand size, and
        players.
        :param deck: The deck of cards for the game.
        :param discard_pile: The discard pile for the game.
        :param hand_size: The number of cards each player starts with.
        :param players: The players participating in the game.
        """
        pass
