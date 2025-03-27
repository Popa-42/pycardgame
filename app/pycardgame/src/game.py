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
from typing import TypeVar, Generic

from .base import GenericCard

_T_C = TypeVar("_T_C", bound=GenericCard)
_T_R = TypeVar("_T_R")
_T_S = TypeVar("_T_S")


class GenericPlayer(Generic[_T_C]):
    __slots__ = ("name", "hand", "score")

    def __init__(self, name, hand=None, score=0):
        self.name = name
        self.hand = hand or []
        self.score = score

    def add_card(self, *cards):
        self.hand.extend(cards)

    def remove_card(self, *cards):
        for card in cards:
            self.hand.remove(card)
        return self

    def play_card(self, *cards):
        if not cards:
            return [self.hand.pop()]
        for card in cards:
            self.hand.remove(card)
        return list(cards)

    def get_hand(self):
        return self.hand

    def get_score(self):
        return self.score

    def set_score(self, score):
        self.score = score
        return self

    def get_name(self):
        return self.name

    def set_name(self, name):
        self.name = name
        return self

    def __getitem__(self, key): return self.hand[key]

    def __str__(self):
        return f"Player {self.name} ({len(self.hand)} card(s))"

    def __repr__(self):
        return (f"{self.__class__.__name__}({self.name!r}, hand={self.hand!r}, "
                f"score={self.score!r})")

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return (self.score == other.score and self.hand == other.hand and
                self.name == other.name)

    def __ne__(self, other): return not self.__eq__(other)
    def __lt__(self, other): return self.score < other.score
    def __le__(self, other): return self.score <= other.score
    def __gt__(self, other): return self.score > other.score
    def __ge__(self, other): return self.score >= other.score
    def __bool__(self): return bool(self.hand) and self.score >= 0
    def __iter__(self): return iter(self.hand)
    def __len__(self): return len(self.hand)


class GenericGame(Generic[_T_C]):
    def __init__(self, card_type, deck_type, deck=None, discard_pile=None,
                 trump=None, hand_size=4, starting_player_index=0, *players):
        self._card_type = card_type
        self._deck_type = deck_type

        if trump is not None and trump not in self._card_type.SUITS:
            raise ValueError(f"Invalid suit for trump: {trump}")

        self.deck = deck or self._deck_type().shuffle()
        self.discard_pile = discard_pile or \
            self._deck_type(cards=[])

        self.trump = None
        if trump is not None:
            self.set_trump(trump)
        self.apply_trump()

        self.hand_size = hand_size

        self.players = list(players)
        for player in self.players:
            player.add_card(*self.deck.draw(self.hand_size))

        start_idx = starting_player_index
        if start_idx < 0 or start_idx > 0 and start_idx >= len(self.players):
            raise ValueError("Invalid starting player index")
        self.current_player_index = start_idx

    def add_players(self, *players):
        self.players.extend(players)
        return self

    def remove_players(self, *players):
        for player in players:
            self.players.remove(player)
        return self

    def deal(self, num_cards=1, *players):
        players = players or self.players
        for player in players:
            player.add_card(*self.deck.draw(num_cards))
        return self

    def shuffle(self):
        self.deck.shuffle()
        return self

    def play(self, player=None, *cards):
        player = player or self.get_current_player()
        self.discard_pile.add(*player.play_card(*cards))
        return self

    def get_trump(self):
        return self.trump

    def set_trump(self, suit):
        if suit not in self._card_type.SUITS:
            raise ValueError(f"Invalid suit for trump: {suit}")
        self.trump = suit
        return self

    def apply_trump(self):
        for card in self.deck:
            if card.get_suit(as_index=False) == self.trump:
                card.set_trump(True)
            else:
                card.set_trump(False)
        return self

    def get_current_player(self):
        return self.players[self.current_player_index]

    def set_current_player(self, player):
        self.current_player_index = self.players.index(player)
        return self

    def get_players(self):
        return self.players

    def get_deck(self):
        return self.deck

    def set_deck(self, deck):
        self.deck = deck
        return self

    def __str__(self):
        return f"Game of {len(self.players)} players"

    def __repr__(self):
        return (f"{self.__class__.__name__}("
                f"card_type={self._card_type!r}, "
                f"deck_type={self._deck_type!r}, "
                f"deck={self.deck!r}, "
                f"discard_pile={self.discard_pile!r}, "
                f"trump={self.trump!r}, "
                f"hand_size={self.hand_size!r}, "
                f"starting_player_index={self.current_player_index!r}, "
                f"*{self.players!r}")
