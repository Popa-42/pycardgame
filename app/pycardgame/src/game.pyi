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
    overload,
    Generic,
    Iterator,
    List,
    Optional,
    Type,
    TypeVar,
    Union,
)

from .base import GenericCard, GenericDeck

_T_C = TypeVar("_T_C", bound=GenericCard)
_T_R = TypeVar("_T_R")
_T_S = TypeVar("_T_S")


class GenericPlayer(Generic[_T_C]):
    """
    A class representing a player in a card game.
    :param name: The name of the player.
    :param hand: The player's hand of cards.
    """

    def __init__(self,
                 name: str,
                 hand: Optional[List[_T_C]] = None,
                 score: int = 0) -> None:
        """
        Constructor for the Player class.
        :param name: The name of the player.
        :param hand: The player's hand of cards.
        :param score: The player's initial score.
        """

        self.name: str = ...
        self.hand: List[_T_C] = ...
        self.score: int = ...

    def add_card(self, *cards: _T_C) -> GenericPlayer[_T_C]:
        """
        Add a card to the player's hand.
        :param cards: The card(s) to add.
        :return: The player object.
        """
        pass

    def remove_card(self, *cards: _T_C) -> GenericPlayer[_T_C]:
        """
        Remove a card from the player's hand.
        :param cards: The card(s) to remove.
        :return: The player object.
        """
        pass

    def play_card(self, *cards: _T_C) -> List[_T_C]:
        """
        Play a card from the player's hand. The card will be removed from the
            hand.
        :param cards: The card(s) to play.
        :return: The card(s) that was/were played.
        """
        pass

    def get_hand(self) -> List[_T_C]:
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

    def set_score(self, score: int) -> GenericPlayer[_T_C]:
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

    def set_name(self, name: str) -> GenericPlayer[_T_C]:
        """
        Set the player's name.
        :param name: The name to set.
        :return: The player object.
        """
        pass

    @overload
    def __getitem__(self, index: int) -> _T_C: ...
    @overload
    def __getitem__(self, s: slice) -> List[_T_C]: ...
    def __getitem__(self, key): ...

    def __eq__(self, other: GenericPlayer[_T_C]) -> bool: ...
    def __lt__(self, other: GenericPlayer[_T_C]) -> bool: ...
    def __le__(self, other: GenericPlayer[_T_C]) -> bool: ...
    def __gt__(self, other: GenericPlayer[_T_C]) -> bool: ...
    def __ge__(self, other: GenericPlayer[_T_C]) -> bool: ...
    def __ne__(self, other: GenericPlayer[_T_C]) -> bool: ...
    def __bool__(self) -> bool: ...
    def __iter__(self) -> Iterator[_T_C]: ...
    def __len__(self) -> int: ...


class GenericGame(Generic[_T_C]):
    """
    The base class for a card game.
    :param card_type: The type of card to use.
    :param deck_type: The type of deck to use.
    :param deck: The predefined deck of cards. If not provided, a new deck will
        be created.
    :param discard_pile: A discard pile for the game. If not provided, a new
        empty discard pile will be created.
    :param trump: The trump suit for the game, if any.
    :param hand_size: The size of each player's hand.
    :param starting_player_index: The index of the starting player.
    :param players: The players in the game.
    """

    def __init__(self,
                 card_type: Type[_T_C],
                 deck_type: Type[GenericDeck[_T_C]],
                 deck: Optional[GenericDeck[_T_C]] = None,
                 discard_pile: Optional[GenericDeck[_T_C]] = None,
                 trump: Optional[Union[_T_C.SuitType, str]] = None,
                 hand_size: int = 4,
                 starting_player_index: int = 0,
                 *players: GenericPlayer[_T_C]) -> None:
        """
        Constructor for the GenericGame class.
        :param card_type: The type of card to use.
        :param deck_type: The type of deck to use.
        :param deck: The predefined deck of cards. If not provided, a new deck
            will be created.
        :param discard_pile: A discard pile for the game. If not provided, a
            new empty discard pile will be created.
        :param trump: The trump suit for the game, if any.
        :param hand_size: The size of each player's hand. Default is 4.
        :param starting_player_index: The index of the starting player. Defaults
            to 0.
        :param players: The players in the game.
        """
        self._card_type: Type[_T_C] = ...
        self._deck_type: Type[GenericDeck[_T_C]] = ...

        self.deck: GenericDeck[_T_C] = ...
        self.discard_pile: GenericDeck[_T_C] = ...

        self.trump: Optional[Union[_T_C.SuitType, str]] = ...
        self.hand_size: int = ...
        self.players: List[GenericPlayer[_T_C]] = ...
        self.current_player_index: int = ...

    def add_players(self, *players: GenericPlayer[_T_C]
                    ) -> GenericGame[_T_C, GenericDeck[_T_C]]:
        """
        Add one or multiple players to the game.
        :param players: The players to add.
        :return: The game object.
        """
        pass

    def remove_players(self, *players: GenericPlayer[_T_C]
                       ) -> GenericGame[_T_C, GenericDeck[_T_C]]:
        """
        Remove one or multiple players from the game.
        :param players: The players to remove.
        :return: The game object.
        """
        pass

    def deal(self, num_cards: int = 1, *players: GenericPlayer[_T_C]
             ) -> GenericGame[_T_C, GenericDeck[_T_C]]:
        """
        Deal cards to a player in the game.
        :param num_cards: The number of cards to deal. Default is 1.
        :param players: The players to deal the cards to. If not provided, all
            players will be dealt to.
        :return: The game object.
        """
        pass

    def shuffle(self) -> GenericGame:
        """
        Shuffle the deck of cards.
        :return: The game object.
        """
        pass

    def play(self, player: GenericPlayer[_T_C] = None, *cards: _T_C
             ) -> GenericGame[_T_C, GenericDeck[_T_C]]:
        """
        Play one or more cards from a player's hand. The cards will be added to
        the discard pile.
        :param player: The player to play the card from. If not provided, the
            current player will play the card.
        :param cards: The card(s) to play.
        :return: The game object.
        """
        pass

    def get_trump(self) -> Optional[Union[_T_C.SuitType, str]]:
        """
        Get the trump suit for the game.
        :return: The trump suit.
        """
        pass

    def set_trump(self, suit: Optional[Union[_T_C.SuitType, str]]
                  ) -> GenericGame[_T_C, GenericDeck[_T_C]]:
        """
        Set the trump suit for the game.
        :param suit: The trump suit to set.
        :return: The game object.
        """
        pass

    def apply_trump(self) -> GenericGame[_T_C, GenericDeck[_T_C]]:
        """
        Apply the trump suit to the deck of cards.
        :return: The game object.
        """
        pass

    def get_current_player(self) -> GenericPlayer[_T_C]:
        """
        Get the current player in the game.
        :return: The current player.
        """
        pass

    def set_current_player(self, player: GenericPlayer[_T_C]
                           ) -> GenericGame[_T_C, GenericDeck[_T_C]]:
        """
        Set the current player in the game.
        :param player: The player to set as the current player.
        :return: The game object.
        """
        pass

    def get_players(self) -> list[GenericPlayer[_T_C]]:
        """
        Get the players in the game.
        :return: The players in the game.
        """
        pass

    def get_deck(self) -> GenericDeck[_T_C]:
        """
        Get the deck of cards in the game.
        :return: The deck of cards.
        """
        pass

    def set_deck(self, deck: GenericDeck[_T_C]
                 ) -> GenericGame[_T_C, GenericDeck[_T_C]]:
        """
        Set the deck of cards in the game.
        :param deck: The deck of cards to set.
        :return: The game object.
        """
        pass
