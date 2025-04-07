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

from typing import List, Literal

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
        super().__init__(rank, suit, False)  # type: ignore

        self.wild = False

    def is_wild(self):
        return self.wild

    def effect(self, game, player, *args):  # pragma: no cover
        pass

    def __str__(self):
        if self.get_rank() in ["Wild", "Wild Draw Four"]:
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
        if isinstance(game, UnoGame):
            game.draw_count += 2  # Add 2 to the draw count


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
        if args and args[0] is not None:
            self.change_suit(args[0])
            self.wild = False
        else:
            raise ValueError("A new suit must be provided for Wild card.")
        game.discard_cards(self)


class WildDrawFourCard(UnoCard, metaclass=CardMeta, rank_type=T_UnoRanks,
                       suit_type=T_UnoSuits):
    def __init__(self):
        super().__init__("Wild Draw Four", "Wild")
        self.wild = True

    def effect(self, game, player, *args):
        if args and args[0] is not None:
            self.change_suit(args[0])
            self.wild = False
        else:
            raise ValueError(
                "A new suit must be provided for Wild Draw Four card.")
        game.draw_cards(game.get_next_player(), 4)
        game.next_player()


class UnoDeck(
    GenericDeck[UnoCard],
    metaclass=DeckMeta,
    card_type=UnoCard
):
    def __init__(self, cards=None):
        super().__init__()

        colors: List[T_UnoSuits] = ["Red", "Green", "Blue",  # type: ignore
                                    "Yellow"]
        numbers: List[T_UnoRanks] = (["0"]  # type: ignore
                                     + [str(i) for i in range(1, 10)] * 2)

        # Create the deck with the specialized card types
        card_list = [
            # Create Number Cards (0-9)
            NumberCard(rank, suit) for suit in colors for rank in numbers
        ] + [
            # Create DrawTwo Cards
            DrawTwoCard(suit) for suit in colors for _ in range(2)
        ] + [
            # Create Skip Cards
            SkipCard(suit) for suit in colors for _ in range(2)
        ] + [
            # Create Reverse Cards
            ReverseCard(suit) for suit in colors for _ in range(2)
        ] + [
            # Add Wild Cards
            WildCard() for _ in range(4)
        ] + [
            # Add Wild Draw Four Cards
            WildDrawFourCard() for _ in range(4)
        ]

        self.cards = cards if cards is not None else card_list

    def __str__(self):
        return f"UNO Deck with {len(self.cards)} cards."

    def __repr__(self):
        return f"{self.__class__.__name__}(cards={self.cards!r})"


class UnoPlayer(GenericPlayer[UnoCard]):
    __slots__ = ("uno",)

    def __init__(self, name, hand=None):
        super().__init__(name, hand, 0)
        self.uno = False

    def call_uno(self):
        if len(self.hand) == 1:
            self.uno = True
        return self.uno

    def reset_uno(self):
        self.uno = False
        return self

    def __repr__(self):
        return (f"{self.__class__.__name__}({self.name!r}, "
                f"hand={self.hand!r}, uno={self.uno!r})")


class UnoGame(GenericGame[UnoCard]):
    def __init__(self, *players, draw_pile=None, discard_pile=None,
                 hand_size=7):
        super().__init__(UnoCard, UnoDeck, draw_pile, discard_pile, None,
                         hand_size, 0, True, *players)
        self.draw_pile = draw_pile if draw_pile else UnoDeck().shuffle()
        self.draw_count = 0  # Track accumulated draw count
        self.game_ended = False

    def check_valid_play(self, card1, card2=None):
        if card2 is None:
            card2 = self.get_top_card()

        if card1 is None or card2 is None:
            return False

        # Only Draw Two cards can be stacked on top of each other
        if self.draw_count > 0 and card1.get_rank() != "Draw Two":
            return False

        if card1.is_wild():
            return True
        return card1.rank == card2.rank or card1.suit == card2.suit

    def get_next_player(self):
        return self.players[
            (self.current_player_index + self.direction) % len(self.players)]

    def start_game(self):
        self.deal_initial_cards()
        self.discard_pile.add(self.draw_pile.draw())
        return self

    def draw_instead_of_play(self, player=None):
        player = player or self.get_current_player()

        if self.draw_count > 0:
            drawn_cards = self.draw_cards(player, self.draw_count)
            self.draw_count = 0
        else:
            drawn_cards = self.draw_cards(player, 1)

        return drawn_cards

    def determine_winner(self):
        for player in self.players:
            if len(player) == 0:
                return player
        return None

    def end_game(self, export=None):  # type: ignore
        winner = self.determine_winner()
        if winner is not None:
            print(f"{winner.name} wins the game!")
        else:
            print("Game ended without a winner.")

        self.game_ended = True

        self.draw_pile.clear()
        self.discard_pile.clear()
        for player in self.players:
            player.hand.clear()

        self.players.clear()

        # TODO: Export game statistics to a file or database
        # self.export_statistics(path=export)

        print("Game resources have been cleared and the game is now closed.")

        return winner

    def __str__(self):
        direction = "Clockwise" if self.direction == 1 else "Counter-clockwise"
        return ("UNO Game\n"
                f"Current Player: {self.get_current_player().name}\n"
                f"Draw Pile: {len(self.draw_pile)} card(s)\n"
                f"Discard Pile: {len(self.discard_pile)} card(s)\n"
                f"Direction: {direction}\n"
                f"Top Card: {self.get_top_card()}\n"
                "Players:\n" + "\n".join(
                    [f" - {player.name}: {len(player)} card(s)" for player in
                     self.players]))

    def __repr__(self):
        return (f"{self.__class__.__name__}("
                f"players={self.players!r}, "
                f"draw_pile={self.draw_pile!r}, "
                f"discard_pile={self.discard_pile!r}, "
                f"hand_size={self.hand_size!r}, "
                f"current_player_index={self.current_player_index!r}, "
                f"direction={self.direction!r})")
