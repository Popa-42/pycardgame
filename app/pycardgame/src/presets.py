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

from typing import Literal

from .. import (
    CardMeta,
    DeckMeta,
    GenericCard,
    GenericDeck,
    GenericGame,
    GenericPlayer,
)

T_Ranks = Literal["2", "3", "4", "5", "6", "7", "8", "9", "10", "Jack",
                  "Queen", "King", "Ace"]
T_Suits = Literal["Diamonds", "Hearts", "Spades", "Clubs"]


class PokerCard(
    GenericCard[T_Ranks, T_Suits],
    metaclass=CardMeta,
    rank_type=T_Ranks,
    suit_type=T_Suits
):
    ...


class PokerDeck(
    GenericDeck[PokerCard],
    metaclass=DeckMeta,
    card_type=PokerCard
):
    ...


class PokerPlayer(GenericPlayer[PokerCard]):
    def __init__(self, name, bankroll=1000):
        super().__init__(name, [])
        self.bankroll = bankroll

    def bet(self, amount):
        if amount > self.bankroll:
            raise ValueError("Bet exceeds bankroll")
        self.bankroll -= amount
        return self

    def win(self, amount):
        self.bankroll += amount
        return self


class PokerGame(GenericGame[PokerCard]):
    def __init__(self, starting_player_index=0, *players):
        super().__init__(PokerCard, PokerDeck, None, None, None, 2,
                         starting_player_index, *players)
        self.trash_pile = []
        self.trash_pile_limit = 2
        self.trash_pile_index = 0
        self.pot = 0
        self.current_bet = 0
