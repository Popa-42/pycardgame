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

from typing import (
    Any,
    overload,
    Generic,
    Iterator,
    List,
    Literal,
    Optional,
    Type,
    TypeVar,
    Union,
)

_RankT = TypeVar("_RankT")
_SuitT = TypeVar("_SuitT")


class GenericCard(Generic[_RankT, _SuitT]):
    """
    A playing card.
    :param rank: The rank of the card.
    :param suit: The suit of the card.
    :param trump: Whether the card is a trump card.
    """
    RANKS: List[_RankT] = ...
    SUITS: List[_SuitT] = ...

    def __init__(self, rank: Optional[Union[_RankT, int]],
                 suit: Optional[Union[_SuitT, int]], trump: bool = False
                 ) -> None:
        """
        Creates a new card instance.
        :param rank: The card’s rank, provided either as a string (e.g.,
            `"Ace"`) or an integer index.
        :param suit: The card’s suit, provided either as a string (e.g.,
            `"Hearts"`) or an integer index.
        :param trump: Whether the card is a trump card.
        :raise ValueError: If the given rank or suit is not found or the index
            is out of range.
        """
        self.rank: Optional[int] = ...
        self.suit: Optional[int] = ...
        self.trump: bool = ...

    @staticmethod
    def _set_value(value: Optional[Union[_RankT, _SuitT, int]],
                   values_list: List[Union[_RankT, _SuitT]], value_name: str
                   ) -> Optional[int]: ...

    def get_rank(self, as_index: bool = False) -> Optional[Union[_RankT, int]]:
        """
        Returns the card’s rank.
        :param as_index: If `True`, the rank is returned as an integer index;
            otherwise, as a string.
        :return: The rank of the card.
        """
        pass

    def set_rank(self, rank: Optional[Union[_RankT, int]]
                 ) -> GenericCard[_RankT, _SuitT]:
        """
        Sets the card’s rank. Accepts a rank name or an integer index.
        :param rank: The rank to set.
        :return: The card with the rank set.
        :raise ValueError: If the given string is not found in `rank_names` or
            the index is out of range.
        """
        pass

    def get_suit(self, as_index: bool = False) -> Optional[Union[_SuitT, int]]:
        """
        Returns the card’s suit.
        :param as_index: If `True`, returns the suit as an integer index;
            otherwise, as a string.
        :return: The suit of the card.
        """
        pass

    def set_suit(self, suit: Optional[Union[_SuitT, int]]
                 ) -> GenericCard[_RankT, _SuitT]:
        """
        Sets the card’s suit. Accepts a suit name or an integer index.
        :param suit: The suit to set.
        :return: The card instance with the updated suit.
        :raise ValueError: If the given string is not found in `suit_names` or
            the index is out of range.
        """
        pass

    def get_trump(self) -> bool:
        """
        Returns whether the card is marked as a trump card.
        :return: `True` if the card is a trump card; otherwise, `False`.
        """
        pass

    def set_trump(self, trump: bool) -> GenericCard[_RankT, _SuitT]:
        """
        Set whether the card is a trump card.
        :param trump: Whether the card is a trump card.
        :return: The card with the trump status set.
        """
        pass

    def __copy__(self) -> GenericCard[_RankT, _SuitT]:
        """
        Creates a shallow copy of the card.
        :return: A new card instance with the same rank, suit, and trump status.
        """
        pass

    def __lt__(self, other: GenericCard[_RankT, _SuitT]) -> bool: ...
    @overload
    def __eq__(self, other: GenericCard[_RankT, _SuitT]) -> bool: ...
    @overload
    def __eq__(self, other: object) -> bool: ...
    def __gt__(self, other: GenericCard[_RankT, _SuitT]) -> bool: ...
    def __le__(self, other: GenericCard[_RankT, _SuitT]) -> bool: ...
    def __ge__(self, other: GenericCard[_RankT, _SuitT]) -> bool: ...
    @overload
    def __ne__(self, other: GenericCard[_RankT, _SuitT]) -> bool: ...
    @overload
    def __ne__(self, other: object) -> bool: ...


_CardT = TypeVar("_CardT", bound=GenericCard)  # type: ignore


class GenericDeck(Generic[_CardT]):
    """
    A deck of cards.
    :param cards: A custom list of `Card` objects. If omitted, a full deck is
        created using the `reset()` method.
    """
    _card_type: Type[_CardT]

    def __init__(self, cards: Optional[List[_CardT]] = None) -> None:
        """
        Creates a new deck instance.
        :param cards: A custom list of `Card` objects. If omitted, a full deck
            is created using the `reset()` method.
        """
        self.cards: List[_CardT] = ...

    def reset(self) -> GenericDeck[_CardT]:
        """
        Creates a full deck by iterating over every combination of suit and rank
            from the `Card` class, then sorts the deck.
        :return: The deck instance.
        """
        pass

    def count(self, card: Union[_CardT, _RankT, _SuitT]) -> int:
        """
        Counts the number of occurrences of a specific card, rank, or
        suit in the deck.
        :param card: Either a card instance, a rank (as a `string`), or a suit
            (as a `string`).
        :return: The number of occurrences of the specified card, rank, or suit
            in the deck.
        :raise ValueError: If the given card is not a valid card instance, rank,
            or suit.
        :raise TypeError: If the given input is not a valid type.
        """
        pass

    def sort(self, by: Literal["suit", "rank"] = "suit") -> GenericDeck[_CardT]:
        """
        Sorts and returns the deck.
        :param by: The attribute to sort by.
        :return: The sorted deck.
        :raise ValueError: If the `by` parameter is not a valid attribute.
        """
        pass

    def shuffle(self) -> GenericDeck[_CardT]:
        """
        Randomly shuffles the cards in the deck.
        :return: The deck instance.
        """
        pass

    def draw(self, n: int = 1) -> List[_CardT]:
        """
        Draw `n` cards from the top of the deck.
        :param n: The number of cards to draw. Defaults to `1`.
        :return: A list of drawn cards.
        """
        pass

    def add(self, *cards: _CardT) -> GenericDeck[_CardT]:
        """
        Adds one or more cards to the bottom of the deck.
        :param cards: The cards to be added to the deck.
        :return: The deck instance.
        """
        pass

    def remove(self, *cards: _CardT) -> GenericDeck[_CardT]:
        """
        The cards to be removed from the deck.
        :param cards: The cards to remove from the deck.
        :return: The deck instance.
        :raise ValueError: If any card is not found in the deck.
        """
        pass

    def get_index(self, card: _CardT) -> List[int]:
        """
        Returns the indices of all occurrences of a given card in the deck.
        :param card: The card to search for in the deck.
        :return: A list of indices where the card is found. If the card
            is not found, an empty list is returned.
        """
        pass

    def get_cards(self) -> List[_CardT]:
        """
        Retrieves the entire list of cards in the deck.
        :return: A list of all cards in the deck.
        """
        pass

    def get_top_card(self) -> Optional[_CardT]:
        """
        Returns the card at the top of the deck without removing it.
        :return: The top card of the deck if the deck is not empty; otherwise,
            `None`.
        """
        pass

    def __copy__(self) -> GenericDeck[_CardT]:
        """
        Creates a shallow copy of the deck.
        :return: A new deck instance with the same cards.
        """
        pass

    @overload
    def __getitem__(self, index: int) -> _CardT: ...
    @overload
    def __getitem__(self, s: slice) -> List[_CardT]: ...

    def __len__(self) -> int: ...
    def __iter__(self) -> Iterator[_CardT]: ...

    @overload
    def __eq__(self, other: GenericDeck[_CardT]) -> bool: ...
    @overload
    def __eq__(self, other: object) -> bool: ...

    @overload
    def __ne__(self, other: GenericDeck[_CardT]) -> bool: ...
    @overload
    def __ne__(self, other: object) -> bool: ...


class CardMeta(type):
    """A metaclass for automatically creating custom card classes."""
    def __new__(cls, name: str, bases: tuple[Any, ...],
                class_dict: dict[str, Any], rank_type: Type[_RankT],
                suit_type: Type[_SuitT]) -> CardMeta:
        """
        Creates a new card class with the given rank and suit types.
        :param name: The name of the class.
        :param bases: The base classes of the new class.
        :param class_dict: The class dictionary.
        :param rank_type: The type of the card rank.
        :param suit_type: The type of the card suit.
        :return: The new card class.
        """
        pass


class DeckMeta(type):
    """A metaclass for automatically creating custom deck classes."""
    def __new__(cls, name: str, bases: tuple[Any, ...],
                class_dict: dict[str, Any], card_type: Type[_CardT]) -> DeckMeta:
        """
        Creates a new deck class with the given card type.
        :param name: The name of the class.
        :param bases: The base classes of the new class.
        :param class_dict: The class dictionary.
        :param card_type: The type of the card to use in the deck.
        :return: The new deck class.
        """
        pass
