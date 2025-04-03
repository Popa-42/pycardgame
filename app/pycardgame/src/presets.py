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

    def is_wild(self):
        return self.get_suit() == "Wild"

    def __str__(self):
        if self.is_wild():
            return f"{self.get_rank()}"
        return f"{self.get_suit()} {self.get_rank()}"


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
        return f"UNO Deck with {len(self.cards)} cards."

    def __repr__(self):
        return f"{self.__class__.__name__}(cards={self.cards!r})"


class UnoPlayer(GenericPlayer[UnoCard]):
    def __init__(self, name, hand=None, score=0):
        super().__init__(name, hand, score)
        self.uno = False  # Indicates if the player has called "UNO"

    def call_uno(self):
        if len(self.hand) == 1:
            self.uno = True
        return self.uno

    def __str__(self):
        return f"Player {self.name} with {len(self.hand)} cards"


class UnoGame(GenericGame[UnoCard]):
    def __init__(self, *players, deck=None, discard_pile=None, hand_size=7):
        super().__init__(UnoCard, UnoDeck, deck, discard_pile, None,
                         hand_size, 0, False, *players)
        self.deck = deck or UnoDeck().shuffle()
        self.discard_pile = discard_pile or UnoDeck([])
        self.direction = 1  # 1 for clockwise, -1 for counter-clockwise

    @staticmethod
    def check_valid_play(card1, card2):
        if card1.get_suit() == "Wild" or card2.get_suit() == "Wild":
            return True
        return card1.rank == card2.rank or card1.suit == card2.suit

    def discard_card(self, *cards):
        self.discard_pile.add(*cards, to_top=True)
        return self

    def get_top_card(self):
        return self.discard_pile.get_top_card()

    def get_next_player(self):
        return self.players[
            (self.current_player_index + self.direction) % len(self.players)]

    def play_card(self, player, card, new_suit=None):
        if self.check_valid_play(card, self.discard_pile.get_top_card()):
            if card.get_rank() == "Wild":
                card.set_suit(new_suit)
            self.discard_card(card)
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

    def apply_effects(self, player, card):
        if card.get_rank() == "Draw Two":
            self.draw_card(player, 2)
        elif card.get_rank() == "Skip":
            self.next_player()
        elif card.get_rank() == "Reverse":
            self.reverse_direction()
        elif card.get_rank() == "Wild Draw Four":
            self.draw_card(player, 4)
            self.next_player()

    def end_turn(self):
        top_card = self.get_top_card()
        if top_card.get_rank() in ["Skip", "Reverse"]:
            self.apply_effects(self.get_current_player(), top_card)
        elif top_card.get_rank() == "Draw Two":
            self.apply_effects(self.get_next_player(), top_card)
        elif top_card.get_rank() == "Wild Draw Four":
            self.apply_effects(self.get_next_player(), top_card)

    def next_player(self):
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
        return (f"UNO Game with {len(self.players)} players. "
                f"Current top card: {self.get_top_card()}")

    def __repr__(self):
        return (f"{self.__class__.__name__}(deck={self.deck!r}, "
                f"discard_pile={self.discard_pile!r}, "
                f"{self.players!r})")
