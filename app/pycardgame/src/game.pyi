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

from typing import Iterator, TypeVar, Generic, List, Optional, Union

from .base import Card, Deck

T = TypeVar("T", bound=Card)


class Player(Generic[T]):
    """
    A class representing a player in a card game.
    :param name: The name of the player.
    :param hand: The player's hand of cards.
    :param kwargs: Additional attributes to set on the player.
    """

    def __init__(self,
                 name: str,
                 hand: Optional[List[T]] = None,
                 score: int = 0, **kwargs) -> None:
        """
        Constructor for the Player class.
        :param name: The name of the player.
        :param hand: The player's hand of cards.
        :param score: The player's initial score.
        :param kwargs: Additional attributes to set on the player.
        """

        self.name: str = ...
        self.hand: List[T] = ...
        self.score: int = ...

    def add_card(self, *cards: T) -> Player[T]:
        """
        Add a card to the player's hand.
        :param cards: The card(s) to add.
        :return: The player object.
        """
        pass

    def remove_card(self, *cards: T) -> Player[T]:
        """
        Remove a card from the player's hand.
        :param cards: The card(s) to remove.
        :return: The player object.
        """
        pass

    def play_card(self, *cards: T) -> List[T]:
        """
        Play a card from the player's hand. The card will be removed
        from the hand.
        :param cards: The card(s) to play.
        :return: The card(s) that was/were played.
        """
        pass

    def get_hand(self) -> List[T]:
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

    def set_score(self, score: int) -> Player[T]:
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

    def set_name(self, name: str) -> Player[T]:
        """
        Set the player's name.
        :param name: The name to set.
        :return: The player object.
        """
        pass

    def __getitem__(self, item: Union[int, slice]
                    ) -> Union[T, List[T]]: ...

    def __eq__(self, other: Player) -> bool: ...
    def __lt__(self, other: Player) -> bool: ...
    def __le__(self, other: Player) -> bool: ...
    def __gt__(self, other: Player) -> bool: ...
    def __ge__(self, other: Player) -> bool: ...
    def __ne__(self, other: Player) -> bool: ...
    def __bool__(self) -> bool: ...
    def __iter__(self) -> Iterator[Card]: ...
    def __len__(self) -> int: ...


class Game(Generic[T]):
    """
    A class representing a card game.
    :param deck: The deck of cards to use in the game. If not provided,
        a new deck will be created.
    :param trump: The trump suit for the game.
    :param players: The players in the game.
    :param kwargs: Additional attributes to set on the game.
    """

    def __init__(
        self,
        deck: Optional[Deck[T]] = None,
        trump: Optional[Union[T.SuitType, str]] = None,
        hand_size: int = 4,
        *players: Player[T],
        **kwargs
    ) -> None:
        """
        Constructor for the Game class.
        :param deck: The deck of cards to use in the game. If not
            provided, a new deck will be created.
        :param hand_size: The number of cards to deal to each player.
        :param trump: The trump suit for the game.
        :param players: The players in the game.
        :param kwargs: Additional attributes to set on the game.
        """
        self.deck: Deck[T] = ...
        self.discard_pile: Deck[T] = ...

        self.trump: Optional[Union[T.SuitType, str]] = ...
        self.hand_size: int = ...
        self.players: List[Player[T]] = ...
        self.current_player_index: int = ...

    def add_players(self, *players: Player[T]) -> Game[T, Deck[T]]:
        """
        Add one or multiple players to the game.
        :param players: The players to add.
        :return: The game object.
        """
        pass

    def remove_players(self, *players: Player[T]
                       ) -> Game[T, Deck[T]]:
        """
        Remove one or multiple players from the game.
        :param players: The players to remove.
        :return: The game object.
        """
        pass

    def deal(self, num_cards: int = 1, *players: Player[T]
             ) -> Game[T, Deck[T]]:
        """
        Deal cards to a player in the game.
        :param num_cards: The number of cards to deal. Default is 1.
        :param players: The players to deal the cards to. If not
            provided, all players will be dealt to.
        :return: The game object.
        """
        pass

    def shuffle(self) -> Game:
        """
        Shuffle the deck of cards.
        :return: The game object.
        """
        pass

    def play(self, player: Player[T] = None, *cards: T
             ) -> Game[T, Deck[T]]:
        """
        Play one or more cards from a player's hand. The cards will be
        added to the discard pile.
        :param player: The player to play the card from. If not
            provided, the current player will play the card.
        :param cards: The card(s) to play.
        :return: The game object.
        """
        pass

    def get_trump(self) -> Optional[Union[T.SuitType, str]]:
        """
        Get the trump suit for the game.
        :return: The trump suit.
        """
        pass

    def set_trump(self, suit: Optional[Union[T.SuitType, str]]
                  ) -> Game[T, Deck[T]]:
        """
        Set the trump suit for the game.
        :param suit: The trump suit to set.
        :return: The game object.
        """
        pass

    def apply_trump(self) -> Game[T, Deck[T]]:
        """
        Apply the trump suit to the deck of cards.
        :return: The game object.
        """
        pass

    def get_current_player(self) -> Player[T]:
        """
        Get the current player in the game.
        :return: The current player.
        """
        pass

    def set_current_player(self, player: Player[T]
                           ) -> Game[T, Deck[T]]:
        """
        Set the current player in the game.
        :param player: The player to set as the current player.
        :return: The game object.
        """
        pass

    def get_players(self) -> list[Player[T]]:
        """
        Get the players in the game.
        :return: The players in the game.
        """
        pass

    def get_deck(self) -> Deck[T]:
        """
        Get the deck of cards in the game.
        :return: The deck of cards.
        """
        pass

    def set_deck(self, deck: Deck[T]) -> Game[T, Deck[T]]:
        """
        Set the deck of cards in the game.
        :param deck: The deck of cards to set.
        :return: The game object.
        """
        pass
