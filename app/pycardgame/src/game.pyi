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

from typing import Iterator

from .base import Card, Deck
from .types import Suit


class Player:
    """
    A class representing a player in a card game.
    :param name: The name of the player.
    :param hand: The player's hand of cards.
    :param kwargs: Additional attributes to set on the player.
    """

    def __init__(self,
                 name: str,
                 hand: list[Card] = None,
                 score: int = 0, **kwargs) -> None:
        """
        Constructor for the Player class.
        :param name: The name of the player.
        :param hand: The player's hand of cards.
        :param score: The player's initial score.
        :param kwargs: Additional attributes to set on the player.
        """

        self.name: str = ...
        self.hand: list[Card] = ...
        self.score: int = ...

    def add_card(self, *cards: Card) -> Player:
        """
        Add a card to the player's hand.
        :param cards: The card(s) to add.
        :return: The player object.
        """
        pass

    def remove_card(self, *cards: Card) -> Player:
        """
        Remove a card from the player's hand.
        :param cards: The card(s) to remove.
        :return: The player object.
        """
        pass

    def play_card(self, *cards: Card) -> list[Card]:
        """
        Play a card from the player's hand. The card will be removed
        from the hand.
        :param cards: The card(s) to play.
        :return: The card(s) that was/were played.
        """
        pass

    def get_hand(self) -> list[Card]:
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

    def set_score(self, score: int) -> Player:
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

    def set_name(self, name: str) -> Player:
        """
        Set the player's name.
        :param name: The name to set.
        :return: The player object.
        """
        pass

    def __getitem__(self, item: int | slice) -> Card | list[Card]: ...
    def __eq__(self, other: Player) -> bool: ...
    def __lt__(self, other: Player) -> bool: ...
    def __le__(self, other: Player) -> bool: ...
    def __gt__(self, other: Player) -> bool: ...
    def __ge__(self, other: Player) -> bool: ...
    def __ne__(self, other: Player) -> bool: ...
    def __bool__(self) -> bool: ...
    def __iter__(self) -> Iterator[Card]: ...
    def __len__(self) -> int: ...


class Game:
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
        deck: Deck = None,
        trump: Suit | str | None = None,
        hand_size: int = 4,
        *players: Player,
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
        self.deck: Deck = ...
        self.discard_pile: Deck = ...

        self.trump: Suit | str | None = ...
        self.hand_size: int = ...
        self.players: list[Player] = ...
        self.current_player_index: int = ...

    def add_players(self, *players: Player) -> Game:
        """
        Add one or multiple players to the game.
        :param players: The players to add.
        :return: The game object.
        """
        pass

    def remove_players(self, *players: Player) -> Game:
        """
        Remove one or multiple players from the game.
        :param players: The players to remove.
        :return: The game object.
        """
        pass

    def deal(self, num_cards: int = 1, *players: Player) -> Game:
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

    def play(self, player: Player = None, *cards: Card) -> Game:
        """
        Play one or more cards from a player's hand. The cards will be
        added to the discard pile.
        :param player: The player to play the card from. If not
            provided, the current player will play the card.
        :param cards: The card(s) to play.
        :return: The game object.
        """
        pass

    def get_trump(self) -> Suit | str | None:
        """
        Get the trump suit for the game.
        :return: The trump suit.
        """
        pass

    def set_trump(self, suit: Suit | str | None) -> Game:
        """
        Set the trump suit for the game.
        :param suit: The trump suit to set.
        :return: The game object.
        """
        pass

    def apply_trump(self) -> Game:
        """
        Apply the trump suit to the deck of cards.
        :return: The game object.
        """
        pass

    def get_current_player(self) -> Player:
        """
        Get the current player in the game.
        :return: The current player.
        """
        pass

    def set_current_player(self, player: Player) -> Game:
        """
        Set the current player in the game.
        :param player: The player to set as the current player.
        :return: The game object.
        """
        pass

    def get_players(self) -> list[Player]:
        """
        Get the players in the game.
        :return: The players in the game.
        """
        pass

    def get_deck(self) -> Deck:
        """
        Get the deck of cards in the game.
        :return: The deck of cards.
        """
        pass

    def set_deck(self, deck: Deck) -> Game:
        """
        Set the deck of cards in the game.
        :param deck: The deck of cards to set.
        :return: The game object.
        """
        pass
