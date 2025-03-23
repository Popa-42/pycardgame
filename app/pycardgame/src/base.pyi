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

from typing import Literal, Iterator, Iterable

from .types import Suit, Rank


class Card:
    """
    A playing card.
    :param rank: The rank of the card.
    :param suit: The suit of the card.
    :param trump: Whether the card is a trump card.
    """

    rank_names: list[Rank | str]
    suit_names: list[Suit | str]

    def __init__(self,
                 rank: Rank | int | str | None,
                 suit: Suit | int | str | None,
                 trump: bool = False, **kwargs) -> None:
        """
        Creates a new card instance.
        :param rank: The card’s rank, provided either as a string
            (e.g., `"Ace"`) or an integer index.
        :param suit: The card’s suit, provided either as a string
            (e.g., `"Hearts"`) or an integer index.
        :param trump: Whether the card is a trump card.
        :param kwargs: Additional attributes to set on the card.
        :raise ValueError: If the given rank or suit is not found or the
            index is out of range.
        """
        self.rank: int | None = ...
        self.suit: int | None = ...
        self.trump: bool = ...

    def get_suit(self, as_index: bool = False) -> Suit | int | str:
        """
        Returns the card’s suit.
        :param as_index: If `True`, returns the suit as an integer
            index; otherwise, as a string.
        :return: The suit of the card.
        """
        pass

    def set_suit(self, suit: Suit | int | str) -> Card:
        """
        Sets the card’s suit. Accepts a suit name or an integer index.
        :param suit: The suit to set.
        :return: The card instance with the updated suit.
        :raise ValueError: If the given string is not found in
            `suit_names` or the index is out of range.
        """
        pass

    def get_rank(self, as_index: bool = False) -> Rank | int | str:
        """
        Returns the card’s rank.
        :param as_index: If `True`, the rank is returned as an integer
            index; otherwise, as a string.
        :return: The rank of the card.
        """
        pass

    def set_rank(self, rank: Rank | int | str) -> Card:
        """
        Sets the card’s rank. Accepts a rank name or an integer index.
        :param rank: The rank to set.
        :return: The card with the rank set.
        :raise ValueError: If the given string is not found in
            `rank_names` or the index is out of range.
        """
        pass

    def get_trump(self) -> bool:
        """
        Returns whether the card is marked as a trump card.
        :return: `True` if the card is a trump card; otherwise, `False`.
        """
        pass

    def set_trump(self, trump: bool) -> Card:
        """
        Set whether the card is a trump card.
        :param trump: Whether the card is a trump card.
        :return: The card with the trump status set.
        """
        pass

    def __lt__(self, other: Card) -> bool: ...

    def __eq__(self, other: Card) -> bool: ...

    def __gt__(self, other: Card) -> bool: ...

    def __le__(self, other: Card) -> bool: ...

    def __ge__(self, other: Card) -> bool: ...

    def __ne__(self, other: Card) -> bool: ...


class Deck:
    """
    A deck of cards.
    :param cards: A list of cards to initialize the deck with.
    """

    def __init__(self, cards: list[Card] = None) -> None:
        """
        Creates a new deck instance.
        :param cards: A custom list of `Card` objects. If omitted, a
            full deck is created using the `reset()` method.
        """
        self.cards: list[Card] = cards

    def reset(self) -> Deck:
        """
        Creates a full deck by iterating over every combination of suit
        and rank from the `Card` class, then sorts the deck.
        :return: The deck instance.
        """
        pass

    def count(self, card: Card | Rank | Suit | str) -> int:
        """
        Counts the number of occurrences of a specific card, rank, or
        suit in the deck.
        :param card: Either a card instance, a rank (as a `string`), or
            a suit (as a `string`).
        :return: The number of occurrences of the specified card, rank,
            or suit in the deck.
        :raise ValueError: If the given card is not a valid card
            instance, rank, or suit.
        """
        pass

    def sort(self, by: Literal["suit", "rank"] = "suit") -> Deck:
        """
        Sorts and returns the deck.
        :param by: The attribute to sort by.
        :return: The sorted deck.
        :raise ValueError: If the `by` parameter is not a valid
            attribute.
        """
        pass

    def shuffle(self) -> Deck:
        """
        Randomly shuffles the cards in the deck.
        :return: The deck instance.
        """
        pass

    def draw(self, n: int = 1) -> list[Card]:
        """
        Draw `n` cards from the top of the deck.
        :param n: The number of cards to draw. Defaults to `1`.
        :return: A list of drawn cards.
        """
        pass

    def add(self, *cards: Card) -> Deck:
        """
        Adds one or more cards to the bottom of the deck.
        :param cards: The cards to be added to the deck.
        :return: The deck instance.
        """
        pass

    def remove(self, *cards: Card) -> Deck:
        """
        The cards to be removed from the deck.
        :param cards: The cards to remove from the deck.
        :return: The deck instance.
        :raise ValueError: If any card is not found in the deck.
        """
        pass

    def get_index(self, card: Card) -> list[int]:
        """
        Returns the indices of all occurrences of a given card in the
        deck.
        :param card: The card to search for in the deck.
        :return: A list of indices where the card is found. If the card
            is not found, an empty list is returned.
        """
        pass

    def get_cards(self) -> list[Card]:
        """
        Retrieves the entire list of cards in the deck.
        :return: A list of all cards in the deck.
        """
        pass

    def get_top_card(self) -> Card | None:
        """
        Returns the card at the top of the deck without removing it.
        :return: The top card of the deck if the deck is not empty;
            otherwise, `None`.
        """
        pass

    def __getitem__(self, key) -> Card: ...

    def __len__(self) -> int: ...

    def __iter__(self) -> Iterator[Card]: ...
