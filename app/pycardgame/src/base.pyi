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

from typing import Literal, Iterator

from .types import Suit, Rank


class Card:
    """
    A playing card.
    :param rank: The rank of the card.
    :param suit: The suit of the card.
    :param trump: Whether the card is a trump card.
    """

    suit_names: list[Suit | str]
    rank_names: list[Rank | str]

    def __init__(self, rank: int | str, suit: int | str, trump: bool = False, **kwargs) -> None:
        """
        Initialize a card with a rank, suit, and trump status.
        :param rank: The rank of the card.
        :param suit: The suit of the card.
        :param trump: Whether the card is a trump card.
        :param kwargs: Additional attributes for the card.
        """
        self.rank: int = ...
        self.suit: int = ...
        self.trump: bool = ...

    def get_suit(self, as_index: bool = False) -> int | str:
        """
        Return the suit of the card.
        :param as_index: If True, return the index of the suit.
        """
        pass

    def get_rank(self, as_index: bool = False) -> int | str:
        """
        Return the rank of the card.
        :param as_index: If True, return the index of the rank.
        """
        pass

    def __str__(self) -> str: ...
    def __repr__(self) -> str: ...
    def __lt__(self, other: Card) -> bool: ...
    def __eq__(self, other: Card) -> bool: ...
    def __gt__(self, other: Card) -> bool: ...
    def __le__(self, other: Card) -> bool: ...
    def __ge__(self, other: Card) -> bool: ...
    def __ne__(self, other: Card) -> bool: ...


class Deck:
    """A deck of cards."""
    def __init__(self, cards: list[Card] = None) -> None:
        """
        Initialize the deck with a list of cards.
        :param cards: A list of cards to initialize the deck with.
        """
        self.cards: list[Card] = cards

    def reset(self) -> Deck:
        """
        Reset the deck to a new deck of cards.
        :return: The deck with a new set of cards.
        """
        pass

    def count(self, card: Card | Suit | Rank | str) -> int:
        """
        Return the number of occurrences of a card, suit, or rank in the deck.
        :param card: The card, suit, or rank to count.
        :return: The number of occurrences of the card, suit, or rank in the deck.
        """
        pass

    def sort(self, by: Literal["suit", "rank"] = "suit") -> Deck:
        """
        Sorts and returns the deck.
        :param by: The attribute to sort by.
        :return: The sorted deck.
        """
        pass

    def shuffle(self) -> Deck:
        """
        Shuffle the deck.
        :return: The shuffled deck.
        """
        pass

    def draw(self, n: int = 1) -> Card | list[Card]:
        """
        Draw `n` cards from the deck.
        :param n: The number of cards to draw.
        :return: A single card if `n` is 1, otherwise a list of cards.
        """
        pass

    def add(self, card: Card) -> Deck:
        """
        Add a card to the end of deck.
        :param card: The card to add to the deck.
        :return: The deck with the card added.
        """
        pass

    def get_index(self, card: Card) -> list[int]:
        """
        Return the indices of all occurrences of a card in the deck.
        :param card: The card to search for.
        :return: A list of indices of the card in the deck
        """
        pass

    def get_cards(self) -> list[Card]:
        """
        Return the list of cards in the deck.
        :return: The list of cards in the deck.
        """
        pass

    def __getitem__(self, index) -> Card: ...
    def __len__(self) -> int: ...
    def __str__(self) -> str: ...
    def __repr__(self) -> str: ...
    def __iter__(self) -> Iterator[Card]: ...
