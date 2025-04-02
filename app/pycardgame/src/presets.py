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
    def __init__(self, rank, suit):
        # TODO: Resolve typing issues with _RankT and _SuitT in GenericCard,
        #       and remove the need for this workaround.
        if isinstance(rank, str):
            rank_index = self.RANKS.index(rank)
        elif isinstance(rank, int) or rank is None:
            rank_index = rank
        else:
            raise ValueError("Rank must be a string or an integer.")

        if isinstance(suit, str):
            suit_index = self.SUITS.index(suit)
        elif isinstance(suit, int) or suit is None:
            suit_index = suit
        else:
            raise ValueError("Suit must be a string or an integer.")

        # Initialise the card with rank and suit as integers
        super().__init__(rank_index, suit_index, False)


class UnoDeck(
    GenericDeck[UnoCard],
    metaclass=DeckMeta,
    card_type=UnoCard
):
    def __init__(self, cards=None):
        super().__init__()
        self.cards = cards if cards is not None else [
            UnoCard(rank, suit)  # type: ignore  # TODO: Resolve typing issues
            for suit in ["Red", "Green", "Blue", "Yellow"]
            for rank in ["0"] + [str(i) for i in range(1, 10)] * 2 +
                        ["Skip", "Reverse", "Draw Two"] * 2
        ] + [
            UnoCard("Wild", "Wild"),
            UnoCard("Wild Draw Four", "Wild")
        ] * 4

    def __str__(self):
        return f"UNO Deck with {len(self.cards)} cards"

    def __repr__(self):
        return f"{self.__class__.__name__}(cards={self.cards!r})"


class UnoPlayer(GenericPlayer[UnoCard]):
    def __init__(self, name, hand=None, score=0):
        super().__init__(name, hand, score)

    def __str__(self):
        return f"Player {self.name} with {len(self.hand)} cards"


class UnoGame(GenericGame[UnoCard]):
    def __init__(self, *players, deck=None, discard_pile=None, hand_size=7):
        super().__init__(UnoCard, UnoDeck, deck, discard_pile, None,
                         hand_size, 0, *players)
        self.deck = deck or UnoDeck().shuffle()
        self.discard_pile = discard_pile or UnoDeck([])
        self.direction = 1  # 1 for clockwise, -1 for counter-clockwise

    @staticmethod
    def check_valid_play(card1, card2):
        if card1.rank == "Wild" or card2.rank == "Wild":
            return True
        return card1.rank == card2.rank or card1.suit == card2.suit

    def play_card(self, player, card):
        if self.check_valid_play(card, self.discard_pile.get_top_card()):
            self.discard_pile.add(card)
            player.remove_cards(card)
            return True
        return False

    def draw_card(self, player, n=1):
        if len(self.deck) >= n:
            drawn = self.deck.draw(n)
            if not isinstance(drawn, list):
                drawn = [drawn]
            player.add_cards(*drawn)
            return drawn
        return None

    def reverse_direction(self):
        self.direction *= -1
        return self

    def start_game(self):
        self.deal_initial_cards()
        self.discard_pile.add(self.deck.draw())
        print(f"Game started with {len(self.players)} players.")
        return self

    def next_player(self):
        if self.discard_pile.get_top_card().rank == "Skip":
            self.current_player_index = (self.current_player_index +
                                         self.direction) % len(self.players)

        elif self.discard_pile.get_top_card().rank == "Reverse":
            self.reverse_direction()

        self.current_player_index = (self.current_player_index +
                                     self.direction) % len(self.players)
        return self

    def determine_winner(self):
        for player in self.players:
            if len(player) == 0:
                return player
        return None

    def end_game(self):
        winner = self.determine_winner()
        if winner:
            print(f"{winner.name} wins the game!")

    def __str__(self):
        return f"UNO Game with {len(self.players)} players"

    def __repr__(self):
        return (f"{self.__class__.__name__}(deck={self.deck!r}, "
                f"discard_pile={self.discard_pile!r}, "
                f"{self.players!r})")
