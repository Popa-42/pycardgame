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
    __slots__ = ("wild",)
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

        self.wild = False

    def is_wild(self):
        return self.wild

    def effect(self, game, player, *args): ...

    def __str__(self):
        if self.is_wild():
            return f"{self.get_rank()}"
        return f"{self.get_suit()} {self.get_rank()}"


class NumberCard(UnoCard, metaclass=CardMeta, rank_type=T_UnoRanks,
                 suit_type=T_UnoSuits):
    def __init__(self, rank, suit):
        super().__init__(rank, suit)
        self.wild = False

    def effect(self, game, player, *args):
        pass


class DrawTwoCard(UnoCard, metaclass=CardMeta, rank_type=T_UnoRanks,
                  suit_type=T_UnoSuits):
    def __init__(self, suit):
        super().__init__("Draw Two", suit)
        self.wild = False

    def effect(self, game, player, *args):
        game.draw_cards(game.get_next_player(), 2)


class SkipCard(UnoCard, metaclass=CardMeta, rank_type=T_UnoRanks,
               suit_type=T_UnoSuits):
    def __init__(self, suit):
        super().__init__("Skip", suit)
        self.wild = False

    def effect(self, game, player, *args):
        game.next_player()


class ReverseCard(UnoCard, metaclass=CardMeta, rank_type=T_UnoRanks,
                  suit_type=T_UnoSuits):
    def __init__(self, suit):
        super().__init__("Reverse", suit)
        self.wild = False

    def effect(self, game, player, *args):
        game.reverse_direction()


class WildCard(UnoCard, metaclass=CardMeta, rank_type=T_UnoRanks,
               suit_type=T_UnoSuits):
    def __init__(self):
        super().__init__("Wild", "Wild")
        self.wild = True

    def effect(self, game, player, *args):
        if args and args[0]:
            self.change_suit(args[0])
        else:
            raise ValueError("A new suit must be provided for Wild card.")
        game.discard_cards(self)


class WildDrawFourCard(UnoCard, metaclass=CardMeta, rank_type=T_UnoRanks,
                       suit_type=T_UnoSuits):
    def __init__(self):
        super().__init__("Wild Draw Four", "Wild")
        self.wild = True

    def effect(self, game, player, *args):
        if args and args[0]:
            self.change_suit(args[0])
        else:
            raise ValueError("A new suit must be provided for Wild Draw Four card.")
        game.draw_cards(game.get_next_player(), 4)
        game.next_player()


class UnoDeck(
    GenericDeck[UnoCard],
    metaclass=DeckMeta,
    card_type=UnoCard
):
    def __init__(self, cards=None):
        super().__init__()

        colors: list[T_UnoSuits] = ["Red", "Green", "Blue", "Yellow"]
        numbers: list[T_UnoRanks] = ["0"] + [str(i) for i in range(1, 10)] * 2  # type: ignore[assignment]

        # Create the deck with the specialized card types
        self.cards = cards if cards is not None else [
            # Create Number Cards (0-9)
            NumberCard(rank, suit) for suit in colors for rank in numbers
        ] + [
            # Create DrawTwo Cards
            DrawTwoCard(suit) for suit in colors
        ] + [
            # Create Skip Cards
            SkipCard(suit) for suit in colors
        ] + [
            # Create Reverse Cards
            ReverseCard(suit) for suit in colors
        ] + [
            # Add Wild Cards and Wild Draw Four Cards
            WildCard(),
            WildDrawFourCard()
        ] * 4  # Wild cards are repeated 4 times

    def __str__(self):
        return f"UNO Deck with {len(self.cards)} cards."

    def __repr__(self):
        return f"{self.__class__.__name__}(cards={self.cards!r})"


class UnoPlayer(GenericPlayer[UnoCard]):
    __slots__ = ("uno",)

    def __init__(self, name, hand=None, score=0):
        super().__init__(name, hand, score)
        self.uno = False  # Indicates if the player has called "UNO"

    def call_uno(self):
        if len(self.hand) == 1:
            self.uno = True
        return self.uno

    def reset_uno(self):
        self.uno = False
        return self


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

    def discard_cards(self, *cards):
        self.discard_pile.add(*cards, to_top=True)
        return self

    def get_top_card(self):
        return self.discard_pile.get_top_card()

    def get_next_player(self):
        return self.players[
            (self.current_player_index + self.direction) % len(self.players)]

    def play_card(self, card, player=None, *args):
        if self.check_valid_play(card, self.discard_pile.get_top_card()):
            self.discard_cards(card)
            if not player:
                player = self.get_current_player()
            player.play_cards(card)

            card.effect(self, player, *args)

            return True
        return False

    def draw_cards(self, player, n=1):
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
        self.get_current_player()
        new_index = (self.current_player_index + self.direction) % len(
            self.players)
        self.set_current_player(new_index)
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
