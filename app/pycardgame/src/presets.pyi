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

from typing import Literal, List, Type

from .. import GenericCard, GenericDeck, GenericPlayer, GenericGame

_RanksT = Literal["2", "3", "4", "5", "6", "7", "8", "9", "10", "Jack",
"Queen", "King", "Ace"]
_SuitsT = Literal["Diamonds", "Hearts", "Spades", "Clubs"]


class PokerCard(GenericCard[_RanksT, _SuitsT]):
    """
    A card for a standard 52-card deck.
    :param rank: The rank of the card.
    :param suit: The suit of the card
    """
    RANKS: List[_RanksT] = ...
    SUITS: List[_SuitsT] = ...

    def __init__(self, rank: _RanksT, suit: _SuitsT) -> None:
        """
        Initialize the card.
        :param rank: The rank of the card.
        :param suit: The suit of the card.
        """
        pass


class PokerDeck(GenericDeck[PokerCard]):
    """
    A deck of cards for a standard 52-card deck.
    :param cards: The cards in the deck.
    :param card_type: The type of card to use.
    """

    def __init__(self, cards: List[PokerCard] = None,  # type: ignore
                 card_type: Type[PokerCard] = PokerCard) -> None:
        """
        Initialize the deck.
        :param cards: The cards in the deck.
        :param card_type: The type of card to use.
        """
        pass


class PokerPlayer(GenericPlayer[PokerCard]):
    """
    A player for a standard game of poker.
    :param name: The player's name.
    :param bankroll: The player's bankroll. Default is 1000.
    """

    def __init__(self, name: str, bankroll: float = 1000) -> None:
        """
        Initialize the player.
        :param name: The player's name.
        :param bankroll: The player's bankroll. Default is 1000.
        """
        self.bankroll: float = ...

    def bet(self, amount: float) -> PokerPlayer:
        """
        Place a bet.
        :param amount: The amount to bet.
        :return: The player who placed the bet, with the bet amount deducted
            from their bankroll.
        """
        pass

    def win(self, amount: float) -> PokerPlayer:
        """
        Win a bet.
        :param amount: The amount won.
        :return: The player who won the bet, with the amount added to their
            bankroll.
        """
        pass


class PokerGame(GenericGame[PokerCard]):
    """
    The base class for a game of poker.
    :param starting_player_index: The index of the starting player.
    :param players: The players in the game.
    """

    def __init__(self, starting_player_index: int = 0,
                 *players: PokerPlayer) -> None:
        """
        Initialize the game.
        :param starting_player_index: The index of the starting player.
        :param players: The players in the game.
        """
        self.trash_pile: List[PokerCard] = ...
        self.trash_pile_limit: int = ...
        self.trash_pile_index: int = ...
        self.pot: float = ...
        self.current_bet: float = ...

    def start_round(self) -> None:
        """Start a new round."""
        pass

    def betting_round(self) -> None:
        """Conduct a betting round."""
        pass

    def showdown(self) -> None:
        """Conduct a showdown."""
        pass
