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

from abc import ABC, ABCMeta, abstractmethod
from typing import (
    Any,
    Generic,
    Iterator,
    List,
    Literal,
    Optional,
    overload,
    Type,
    TypeVar,
    Union,
)

_RankT = TypeVar("_RankT")
_SuitT = TypeVar("_SuitT")


class CardMeta(ABCMeta):
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


class GenericCard(ABC, Generic[_RankT, _SuitT]):
    """
    A playing card.
    :param rank: The rank of the card.
    :param suit: The suit of the card.
    :param trump: Whether the card is a trump card.
    """
    __slots__ = ("rank", "suit", "trump")

    RANKS: List[_RankT] = ...
    SUITS: List[_SuitT] = ...

    def __init__(self, rank: Optional[Union[_RankT, int]],
                 suit: Optional[Union[_SuitT, int]],
                 trump: bool = False) -> None:
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
                   values_list: List[Union[_RankT, _SuitT]],
                   value_name: str) -> Optional[int]: ...

    @abstractmethod
    def effect(self, game: GenericGame[_CardT],
               player: GenericPlayer[_CardT]) -> None:
        """
        The effect of the card when played. This method should be implemented
        in each specific card class.
        :param game: The game instance where the card is played.
        :param player: The player who played the card.
        """

    def get_rank(self, as_index: bool = False) -> Optional[Union[_RankT, int]]:
        """
        Returns the card’s rank.
        :param as_index: If `True`, the rank is returned as an integer index;
            otherwise, as a string.
        :return: The rank of the card.
        """

    def change_rank(self, rank: Optional[Union[_RankT, int]]) -> GenericCard[
        _RankT, _SuitT]:
        """
        Sets the card’s rank. Accepts a rank name or an integer index.
        :param rank: The rank to set.
        :return: The card with the rank set.
        :raise ValueError: If the given string is not found in `rank_names` or
            the index is out of range.
        """

    def get_suit(self, as_index: bool = False) -> Optional[Union[_SuitT, int]]:
        """
        Returns the card’s suit.
        :param as_index: If `True`, returns the suit as an integer index;
            otherwise, as a string.
        :return: The suit of the card.
        """

    def change_suit(self, suit: Optional[Union[_SuitT, int]]) -> GenericCard[
        _RankT, _SuitT]:
        """
        Sets the card’s suit. Accepts a suit name or an integer index.
        :param suit: The suit to set.
        :return: The card instance with the updated suit.
        :raise ValueError: If the given string is not found in `suit_names` or
            the index is out of range.
        """

    def is_trump(self) -> bool:
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

    def __copy__(self) -> GenericCard[_RankT, _SuitT]:
        """
        Creates a shallow copy of the card.
        :return: A new card instance with the same rank, suit, and trump status.
        """

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


class DeckMeta(ABCMeta):
    """A metaclass for automatically creating custom deck classes."""

    def __new__(cls, name: str, bases: tuple[Any, ...],
                class_dict: dict[str, Any],
                card_type: Type[_CardT]) -> DeckMeta:
        """
        Creates a new deck class with the given card type.
        :param name: The name of the class.
        :param bases: The base classes of the new class.
        :param class_dict: The class dictionary.
        :param card_type: The type of the card to use in the deck.
        :return: The new deck class.
        """


class GenericDeck(ABC, Generic[_CardT]):
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

    def sort(self, by: Literal["suit", "rank"] = "suit") -> GenericDeck[_CardT]:
        """
        Sorts and returns the deck.
        :param by: The attribute to sort by.
        :return: The sorted deck.
        :raise ValueError: If the `by` parameter is not a valid attribute.
        """

    def shuffle(self, seed: Optional[Union[int, float, str, bytes,
    bytearray]] = None) -> GenericDeck[_CardT]:
        """
        Randomly shuffles the cards in the deck.
        :return: The deck instance.
        """

    @overload
    def draw(self, n: Literal[1] = 1) -> _CardT:
        """
        Draws one or more cards from the top of the deck.
        :param n: The number of cards to draw. Default is 1.
        :return: The drawn card(s).
        :raise ValueError: If `n` is greater than the number of cards in the
            deck.
        """

    @overload
    def draw(self, n: int = 1) -> List[_CardT]:
        """
        Draws one or more cards from the top of the deck.
        :param n: The number of cards to draw. Default is 1.
        :return: The drawn card(s).
        :raise ValueError: If `n` is greater than the number of cards in the
            deck.
        """

    def add(self,
            *cards: _CardT,
            to_top: bool = False) -> GenericDeck[_CardT]:
        """
        Adds one or more cards to the deck.
        :param cards: The cards to be added to the deck.
        :param to_top: If `True`, the cards are added to the top of the deck;
            otherwise, they are added to the bottom.
        :return: The deck instance.
        """

    def remove(self, *cards: _CardT) -> GenericDeck[_CardT]:
        """
        The cards to be removed from the deck.
        :param cards: The cards to remove from the deck.
        :return: The deck instance.
        :raise ValueError: If any card is not found in the deck.
        """

    def get_index(self, card: _CardT) -> List[int]:
        """
        Returns the indices of all occurrences of a given card in the deck.
        :param card: The card to search for in the deck.
        :return: A list of indices where the card is found. If the card
            is not found, an empty list is returned.
        """

    def get_cards(self) -> List[_CardT]:
        """
        Retrieves the entire list of cards in the deck.
        :return: A list of all cards in the deck.
        """

    def get_top_card(self) -> Optional[_CardT]:
        """
        Returns the card at the top of the deck without removing it.
        :return: The top card of the deck if the deck is not empty; otherwise,
            `None`.
        """

    @overload
    def __eq__(self, other: GenericDeck[_CardT]) -> bool: ...

    @overload
    def __eq__(self, other: object) -> bool: ...

    @overload
    def __ne__(self, other: GenericDeck[_CardT]) -> bool: ...

    @overload
    def __ne__(self, other: object) -> bool: ...

    def __copy__(self) -> GenericDeck[_CardT]: ...

    @overload
    def __getitem__(self, index: int) -> _CardT: ...

    @overload
    def __getitem__(self, s: slice) -> List[_CardT]: ...

    def __len__(self) -> int: ...

    def __iter__(self) -> Iterator[_CardT]: ...

    def __contains__(self, item: _CardT) -> bool: ...

    def __bool__(self) -> bool: ...


class GenericPlayer(ABC, Generic[_CardT]):
    """
    A class representing a player in a card game.
    :param name: The name of the player.
    :param hand: The player's hand of cards.
    """
    __slots__ = ("name", "hand", "score")

    def __init__(self, name: str, hand: Optional[List[_CardT]] = None,
                 score: int = 0) -> None:
        """
        Constructor for the Player class.
        :param name: The name of the player.
        :param hand: The player's hand of cards.
        :param score: The player's initial score.
        """
        self.name: str = ...
        self.hand: List[_CardT] = ...
        self.score: int = ...

    def add_cards(self, *cards: _CardT) -> GenericPlayer[_CardT]:
        """
        Add one or more cards to the player's hand.
        :param cards: The card(s) to add.
        :return: The player object.
        """

    def remove_cards(self, *cards: _CardT) -> GenericPlayer[_CardT]:
        """
        Remove one or more cards from the player's hand.
        :param cards: The card(s) to remove.
        :return: The player object.
        """

    def play_cards(self, *cards: _CardT) -> List[_CardT]:
        """
        Play one or more cards from the player's hand. If no cards are provided,
            the player will play all cards in their hand.
        :param cards: The card(s) to play.
        :return: The card(s) that was/were played.
        """

    def get_hand(self) -> List[_CardT]:
        """
        Get the player's hand of cards.
        :return: The player's hand.
        """

    def get_score(self) -> int:
        """
        Get the player's score.
        :return: The player's score.
        """

    def set_score(self, score: int) -> GenericPlayer[_CardT]:
        """
        Set the player's score.
        :param score: The score to set.
        :return: The player object.
        """

    def get_name(self) -> str:
        """
        Get the player's name.
        :return: The player's name.
        """

    def set_name(self, name: str) -> GenericPlayer[_CardT]:
        """
        Set the player's name.
        :param name: The name to set.
        :return: The player object.
        """

    @overload
    def __getitem__(self, index: int) -> _CardT: ...

    @overload
    def __getitem__(self, s: slice) -> List[_CardT]: ...

    @overload
    def __eq__(self, other: GenericPlayer[_CardT]) -> bool: ...

    @overload
    def __eq__(self, other: object) -> bool: ...

    def __lt__(self, other: GenericPlayer[_CardT]) -> bool: ...

    def __le__(self, other: GenericPlayer[_CardT]) -> bool: ...

    def __gt__(self, other: GenericPlayer[_CardT]) -> bool: ...

    def __ge__(self, other: GenericPlayer[_CardT]) -> bool: ...

    @overload
    def __ne__(self, other: GenericPlayer[_CardT]) -> bool: ...

    @overload
    def __ne__(self, other: object) -> bool: ...

    def __bool__(self) -> bool: ...

    def __iter__(self) -> Iterator[_CardT]: ...

    def __len__(self) -> int: ...


class GenericGame(ABC, Generic[_CardT]):
    """
    The base class for a card game.
    :param card_type: The type of card to use.
    :param deck_type: The type of deck to use.
    :param draw_pile: The predefined deck of cards. If not provided, a new deck
        will be created.
    :param discard_pile: A discard pile for the game. If not provided, a new
        empty discard pile will be created.
    :param trump: The trump suit for the game, if any. Must be one of the suits
        defined in card_type.SUITS.
    :param hand_size: The size of each player's hand.
    :param starting_player_index: The index of the starting player.
    :param players: The players in the game.
    """

    def __init__(self,
                 card_type: Type[_CardT],
                 deck_type: Type[GenericDeck[_CardT]],
                 draw_pile: Optional[GenericDeck[_CardT]] = None,
                 discard_pile: Optional[GenericDeck[_CardT]] = None,
                 trump: Optional[_SuitT] = None,
                 hand_size: int = 4,
                 starting_player_index: int = 0,
                 do_not_shuffle: bool = False,
                 *players: GenericPlayer[_CardT]) -> None:
        """
        Constructor for the GenericGame class.
        :param card_type: The type of card to use.
        :param deck_type: The type of deck to use.
        :param draw_pile: The predefined deck of cards. If not provided, a new
            deck will be created.
        :param discard_pile: A discard pile for the game. If not provided, a
            new empty discard pile will be created.
        :param trump: The trump suit for the game, if any. Must be one of the
            suits defined in card_type.SUITS.
        :param hand_size: The size of each player's hand. Default is 4.
        :param starting_player_index: The index of the starting player. Defaults
            to 0.
        :param do_not_shuffle: If True, the deck will not be shuffled.
        :param players: The players in the game.
        :raises ValueError: If trump is not None and not in card_type.SUITS.
        """
        self._card_type: Type[_CardT] = ...
        self._deck_type: Type[GenericDeck[_CardT]] = ...

        self.draw_pile: GenericDeck[_CardT] = ...
        self.discard_pile: GenericDeck[_CardT] = ...

        self.trump: Optional[str] = ...
        self.hand_size: int = ...
        self.players: List[GenericPlayer[_CardT]] = ...
        self.current_player_index: int = ...

    @staticmethod
    @abstractmethod
    def check_valid_play(card1: _CardT, card2: _CardT) -> bool:
        """
        Check if a card can be played on top of another card.
        :param card1: The card to be played.
        :param card2: The card on top of the pile.
        :return: True if the play is valid, False otherwise.
        """

    def deal_initial_cards(self, *players: GenericPlayer[_CardT]) -> (
            GenericGame)[_CardT]:
        """
        Deal initial cards to specified players until they have at least
        hand_size cards. If no players are specified, deals to all players.

        :param players: The players to deal cards to. If not provided, all
            players will be dealt to.
        :return: The game object.
        """

    def add_players(self, *players: GenericPlayer[_CardT]) -> GenericGame[
        _CardT]:
        """
        Add one or multiple players to the game.
        :param players: The players to add.
        :return: The game object.
        """

    def remove_players(self, *players: GenericPlayer[_CardT]) -> GenericGame[
        _CardT]:
        """
        Remove one or multiple players from the game.
        :param players: The players to remove.
        :return: The game object.
        """

    def deal(self, num_cards: int = 1, *players: GenericPlayer[_CardT]) -> \
            GenericGame[_CardT]:
        """
        Deal cards to a player in the game.
        :param num_cards: The number of cards to deal. Default is 1.
        :param players: The players to deal the cards to. If not provided, all
            players will be dealt to.
        :return: The game object.
        """

    def shuffle(self) -> GenericGame[_CardT]:
        """
        Shuffle the deck of cards.
        :return: The game object.
        """

    def play_card(self, card: _CardT,
                  player: Optional[GenericPlayer[_CardT]] = None
                  ) -> GenericGame[_CardT]:
        """
        Play a card from a player's hand. The card will be added to the
        discard pile.
        :param card: The card to play.
        :param player: The player to play the card from. If not provided, the
            current player will play the card.
        :return: The game object.
        """

    def get_trump(self) -> Optional[Any]:
        """
        Get the trump suit for the game.
        :return: The trump suit, which will be one of the suits defined in
            self._card_type.SUITS, or None if no trump suit is set.
        """

    def set_trump(self, suit: Optional[_SuitT]) -> GenericGame[_CardT]:
        """
        Set the trump suit for the game.
        :param suit: The trump suit to set. Must be one of the suits defined in
            self._card_type.SUITS, or None to unset the trump suit.
        :return: The game object.
        :raises ValueError: If suit is not None and not in
            self._card_type.SUITS.
        """

    def apply_trump(self) -> GenericGame[_CardT]:
        """
        Apply the trump suit to all cards in the deck.
        :return: The game object.
        """

    def change_trump(self, suit: Optional[_SuitT]) -> GenericGame[_CardT]:
        """
        Change the trump suit for the game.
        :param suit: The new trump suit to set. Must be a valid suit or None to
            unset the trump suit.
        :return: The game object.
        :raises ValueError: If suit is not None and not one of the vakud suits.
        """

    def get_current_player(self) -> GenericPlayer[_CardT]:
        """
        Get the current player.
        :return: The current player.
        """

    def set_current_player(self, player: Union[GenericPlayer[_CardT], int]) -> (
            GenericGame)[_CardT]:
        """
        Set the current player.
        :param player: The player to set as current. Can be a player object or
            an index.
        :return: The game object.
        """

    def get_players(self) -> List[GenericPlayer[_CardT]]:
        """
        Get all players in the game.
        :return: The list of players.
        """

    def get_draw_pile(self) -> GenericDeck[_CardT]:
        """
        Get the deck of cards.
        :return: The deck of cards.
        """

    def set_draw_pile(self, draw_pile: GenericDeck[_CardT]) -> \
            GenericGame[_CardT]:
        """
        Set the deck of cards.
        :param draw_pile: The deck to set.
        :return: The game object.
        """
