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
    Optional,
    Type,
    TypeVar,
)

from .base import GenericCard, GenericDeck

_RankT = TypeVar("_RankT")
_SuitT = TypeVar("_SuitT")
_CardT = TypeVar("_CardT", bound=GenericCard)  # type: ignore


class GenericPlayer(Generic[_CardT]):
    """
    A class representing a player in a card game.
    :param name: The name of the player.
    :param hand: The player's hand of cards.
    """

    def __init__(self,
                 name: str,
                 hand: Optional[List[_CardT]] = None,
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

    def add_card(self, *cards: _CardT) -> GenericPlayer[_CardT]:
        """
        Add a card to the player's hand.
        :param cards: The card(s) to add.
        :return: The player object.
        """
        pass

    def remove_card(self, *cards: _CardT) -> GenericPlayer[_CardT]:
        """
        Remove a card from the player's hand.
        :param cards: The card(s) to remove.
        :return: The player object.
        """
        pass

    def play_card(self, *cards: _CardT) -> List[_CardT]:
        """
        Play a card from the player's hand. The card will be removed from the
            hand.
        :param cards: The card(s) to play.
        :return: The card(s) that was/were played.
        """
        pass

    def get_hand(self) -> List[_CardT]:
        """
        Get the player's hand of cards.
        :return: The player's hand.
        """
        pass

    def get_score(self) -> int:
        """
        Get the player's score.
        :return: The player's score.
        """
        pass

    def set_score(self, score: int) -> GenericPlayer[_CardT]:
        """
        Set the player's score.
        :param score: The score to set.
        :return: The player object.
        """
        pass

    def get_name(self) -> str:
        """
        Get the player's name.
        :return: The player's name.
        """
        pass

    def set_name(self, name: str) -> GenericPlayer[_CardT]:
        """
        Set the player's name.
        :param name: The name to set.
        :return: The player object.
        """
        pass

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


class GenericGame(Generic[_CardT]):
    """
    The base class for a card game.
    :param card_type: The type of card to use.
    :param deck_type: The type of deck to use.
    :param deck: The predefined deck of cards. If not provided, a new deck will
        be created.
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
                 deck: Optional[GenericDeck[_CardT]] = None,
                 discard_pile: Optional[GenericDeck[_CardT]] = None,
                 trump: Optional[_SuitT] = None,
                 hand_size: int = 4,
                 starting_player_index: int = 0,
                 *players: GenericPlayer[_CardT]) -> None:
        """
        Constructor for the GenericGame class.
        :param card_type: The type of card to use.
        :param deck_type: The type of deck to use.
        :param deck: The predefined deck of cards. If not provided, a new deck
            will be created.
        :param discard_pile: A discard pile for the game. If not provided, a
            new empty discard pile will be created.
        :param trump: The trump suit for the game, if any. Must be one of the suits
            defined in card_type.SUITS.
        :param hand_size: The size of each player's hand. Default is 4.
        :param starting_player_index: The index of the starting player. Defaults
            to 0.
        :param players: The players in the game.
        :raises ValueError: If trump is not None and not in card_type.SUITS.
        """
        self._card_type: Type[_CardT] = ...
        self._deck_type: Type[GenericDeck[_CardT]] = ...

        self.deck: GenericDeck[_CardT] = ...
        self.discard_pile: GenericDeck[_CardT] = ...

        self.trump: Optional[str] = ...
        self.hand_size: int = ...
        self.players: List[GenericPlayer[_CardT]] = ...
        self.current_player_index: int = ...

    def deal_initial_cards(self, *players: GenericPlayer[_CardT]
                          ) -> GenericGame[_CardT]:
        """
        Deal initial cards to specified players until they have at least
        hand_size cards. If no players are specified, deals to all players.
        
        :param players: The players to deal cards to. If not provided, all
            players will be dealt to.
        :return: The game object.
        """
        pass

    def add_players(self, *players: GenericPlayer[_CardT]
                    ) -> GenericGame[_CardT]:
        """
        Add one or multiple players to the game.
        :param players: The players to add.
        :return: The game object.
        """
        pass

    def remove_players(self, *players: GenericPlayer[_CardT]
                       ) -> GenericGame[_CardT]:
        """
        Remove one or multiple players from the game.
        :param players: The players to remove.
        :return: The game object.
        """
        pass

    def deal(self, num_cards: int = 1, *players: GenericPlayer[_CardT]
             ) -> GenericGame[_CardT]:
        """
        Deal cards to a player in the game.
        :param num_cards: The number of cards to deal. Default is 1.
        :param players: The players to deal the cards to. If not provided, all
            players will be dealt to.
        :return: The game object.
        """
        pass

    def shuffle(self) -> GenericGame[_CardT]:
        """
        Shuffle the deck of cards.
        :return: The game object.
        """
        pass

    def play(self, player: Optional[GenericPlayer[_CardT]] = None, *cards: _CardT
             ) -> GenericGame[_CardT]:
        """
        Play one or more cards from a player's hand. The cards will be added to
        the discard pile.
        :param player: The player to play the card from. If not provided, the
            current player will play the card.
        :param cards: The card(s) to play.
        :return: The game object.
        """
        pass

    def get_trump(self) -> Optional[Any]:
        """
        Get the trump suit for the game.
        :return: The trump suit, which will be one of the suits defined in
            self._card_type.SUITS, or None if no trump suit is set.
        """
        pass

    def set_trump(self, suit: Optional[_SuitT]) -> GenericGame[_CardT]:
        """
        Set the trump suit for the game.
        :param suit: The trump suit to set. Must be one of the suits defined in
            self._card_type.SUITS, or None to unset the trump suit.
        :return: The game object.
        :raises ValueError: If suit is not None and not in self._card_type.SUITS.
        """
        pass

    def apply_trump(self) -> GenericGame[_CardT]:
        """
        Apply the trump suit to all cards in the deck.
        :return: The game object.
        """
        pass

    def get_current_player(self) -> GenericPlayer[_CardT]:
        """
        Get the current player.
        :return: The current player.
        """
        pass

    def set_current_player(self, player: GenericPlayer[_CardT]
                           ) -> GenericGame[_CardT]:
        """
        Set the current player.
        :param player: The player to set as current.
        :return: The game object.
        """
        pass

    def get_players(self) -> List[GenericPlayer[_CardT]]:
        """
        Get all players in the game.
        :return: The list of players.
        """
        pass

    def get_deck(self) -> GenericDeck[_CardT]:
        """
        Get the deck of cards.
        :return: The deck of cards.
        """
        pass

    def set_deck(self, deck: GenericDeck[_CardT]
                 ) -> GenericGame[_CardT]:
        """
        Set the deck of cards.
        :param deck: The deck to set.
        :return: The game object.
        """
        pass
