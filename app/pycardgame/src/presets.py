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

T_UnoRanks = Literal["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "Skip",
                     "Reverse", "Draw Two", "Wild", "Wild Draw Four"]
T_UnoSuits = Literal["Red", "Green", "Blue", "Yellow", "Wild"]


class UnoCard(
    GenericCard[T_UnoRanks, T_UnoSuits],
    metaclass=CardMeta,
    rank_type=T_UnoRanks,
    suit_type=T_UnoSuits
):
    pass


class UnoDeck(
    GenericDeck[UnoCard],
    metaclass=DeckMeta,
    card_type=UnoCard
):
    def __init__(self, cards=None):
        super().__init__()
        self.cards = cards if cards is not None else [
            UnoCard(rank, suit)  # type: ignore
            for suit in ["Red", "Green", "Blue", "Yellow"]
            for rank in ["0"] + [str(i) for i in range(1, 10)] * 2 +
                        ["Skip", "Reverse", "Draw Two"] * 2
        ] + [
            UnoCard("Wild", "Wild"),
            UnoCard("Wild Draw Four", "Wild")
        ] * 4

    def __str__(self) -> str:
        return f"UNO Deck with {len(self.cards)} cards"

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(cards={self.cards!r})"


class UnoPlayer(GenericPlayer[UnoCard]):
    def __init__(self, name, hand=None, score=0):
        super().__init__(name, hand, score)

    def __str__(self) -> str:
        return f"Player {self.name} with {len(self.hand)} cards"


class UnoGame(GenericGame[UnoCard]):
    def __init__(self, deck=None, discard_pile=None,
                 hand_size=7, *players):
        super().__init__(UnoCard, UnoDeck, deck, discard_pile, None,
                         hand_size, 0, *players)
        self.deck = deck or UnoDeck()
        self.discard_pile = discard_pile or UnoDeck([])
