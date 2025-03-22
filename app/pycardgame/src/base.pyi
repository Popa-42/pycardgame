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

    suit_names: list[Suit | str]
    rank_names: list[Rank | str]

    def __init__(self, rank: Rank | int | str | None, suit: Suit | int | str | None, trump: bool = False, **kwargs) -> None:
        """
        Initialize a card with a rank, suit, and trump status.
        :param rank: The rank of the card.
        :param suit: The suit of the card.
        :param trump: Whether the card is a trump card.
        :param kwargs: Additional attributes for the card.
        """
        self.rank: int | None = ...
        self.suit: int | None = ...
        self.trump: bool = ...

    def get_suit(self, as_index: bool = False) -> Suit | int | str:
        """
        Return the suit of the card.
        :param as_index: If True, return the index of the suit.
        """
        pass

    def set_suit(self, suit: Suit | int | str) -> Card:
        """
        Set the suit of the card.
        :param suit: The suit to set.
        :return: The card with the suit set.
        """
        pass

    def get_rank(self, as_index: bool = False) -> Rank | int | str:
        """
        Return the rank of the card.
        :param as_index: If True, return the index of the rank.
        """
        pass

    def set_rank(self, rank: Rank | int | str) -> Card:
        """
        Set the rank of the card.
        :param rank: The rank to set.
        :return: The card with the rank set.
        """
        pass

    def get_trump(self) -> bool:
        """
        Return whether the card is a trump card.
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

    def draw(self, n: int = 1) -> list[Card]:
        """
        Draw `n` cards from the deck.
        The drawn cards are removed from the deck.
        :param n: The number of cards to draw.
        :return: A list of drawn cards.
        """
        pass

    def add(self, *cards: Card) -> Deck:
        """
        Add cards at the end of the deck.
        :param cards: The cards to add to the deck.
        :return: The deck with the card added.
        """
        pass

    def remove(self, card: Card) -> None:
        """
        Remove a card from the deck.
        :param card: The card to remove from the deck.
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

    def get_top_card(self) -> Card | None:
        """
        Return the top card of the deck.
        :return: The top card of the deck, or None if the deck is empty.
        """
        pass

    def __getitem__(self, index) -> Card: ...
    def __len__(self) -> int: ...
    def __iter__(self) -> Iterator[Card]: ...
