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

import random
from typing import Generic, TypeVar, get_args, Type

_RankT = TypeVar("_RankT")
_SuitT = TypeVar("_SuitT")


class GenericCard(Generic[_RankT, _SuitT]):
    __slots__ = ("rank", "suit", "trump")

    RANKS = []
    SUITS = []

    def __init__(self, rank, suit, trump=False):
        self.rank = None
        self.suit = None

        if rank is not None:
            self.set_rank(rank)
        if suit is not None:
            self.set_suit(suit)

        self.trump = trump

    @staticmethod
    def _set_value(value, values_list, value_name):
        if not isinstance(value, int):
            if value is None:
                return None
            elif value not in values_list:
                raise ValueError(f"Invalid {value_name} name: {value}")
            value = values_list.index(value)
        else:
            if value < 0 or value >= len(values_list):
                raise ValueError(f"Invalid {value_name} index: {value}")
        return value

    def get_rank(self, as_index=False):
        if self.rank is None:
            return None
        return self.rank if as_index else self.__class__.RANKS[self.rank]

    def set_rank(self, rank):
        self.rank = self._set_value(rank, self.__class__.RANKS, "rank")
        return self

    def get_suit(self, as_index=False):
        if self.suit is None:
            return None
        return self.suit if as_index else self.__class__.SUITS[self.suit]

    def set_suit(self, suit):
        self.suit = self._set_value(suit, self.__class__.SUITS, "suit")
        return self

    def get_trump(self):
        return self.trump

    def set_trump(self, trump):
        if not isinstance(trump, bool):
            raise TypeError("Trump must be a boolean value")
        self.trump = trump
        return self

    def __copy__(self):
        return self.__class__(rank=self.rank, suit=self.suit, trump=self.trump)

    def __str__(self):
        rank_str = str(self.get_rank(as_index=False))
        suit_str = str(self.get_suit(as_index=False))
        return f"{rank_str} of {suit_str}{' (trump)' if self.trump else ''}"

    def __repr__(self):
        return (f"{self.__class__.__name__}(rank={self.rank!r}, "
                f"suit={self.suit!r}{', trump=True' if self.trump else ''})")

    def __lt__(self, other):
        if self.trump and not other.trump:
            return False
        if not self.trump and other.trump:
            return True
        # Defined cards are always greater than None
        suit1 = self.suit if self.suit is not None else -1e9
        suit2 = other.suit if other.suit is not None else -1e9
        rank1 = self.rank if self.rank is not None else -1e9
        rank2 = other.rank if other.rank is not None else -1e9
        return (suit1, rank1) < (suit2, rank2)

    def __eq__(self, other):
        return (self.suit == other.suit and self.rank == other.rank and
                self.trump == other.trump)

    def __gt__(self, other):
        return not self.__lt__(other) and not self.__eq__(other)

    def __le__(self, other): return not self.__gt__(other)
    def __ge__(self, other): return not self.__lt__(other)
    def __ne__(self, other): return not self.__eq__(other)


_CardT = TypeVar("_CardT", bound=GenericCard)


class GenericDeck(Generic[_CardT]):
    _card_type: Type[_CardT]
    __hash__ = None  # Mutable type, so hash is not defined

    def __init__(self, cards=None):
        if cards is None:
            self.cards = self.reset().get_cards()
        else:
            self.cards = cards

    def reset(self):
        self.cards = [self._card_type(rank, suit)
                      for suit in range(len(self._card_type.SUITS))
                      for rank in range(len(self._card_type.RANKS))]
        return self.sort()

    def count(self, card):
        if isinstance(card, self._card_type):
            return self.cards.count(card)
        elif isinstance(card, str):
            if card in self._card_type.RANKS:
                return sum(1 for c in self.cards if c.get_rank() == card)
            elif card in self._card_type.SUITS:
                return sum(1 for c in self.cards if c.get_suit() == card)
            else:
                raise ValueError(
                    "Invalid card name: must be a rank or suit name")
        else:
            raise TypeError(
                "Invalid card type: must be a Card object, a suit, or a rank")

    def sort(self, by="suit"):
        if by == "rank":
            self.cards.sort(key=lambda c: (
                not c.trump, c.rank if c.rank is not None else -1,
                c.suit if c.suit is not None else -1))
        elif by == "suit":
            self.cards.sort()
        else:
            raise ValueError("Invalid sort key: must be 'rank' or 'suit'")
        return self

    def shuffle(self):
        while True:
            random.shuffle(self.cards)
            if self.cards != sorted(self.cards):
                break
        return self

    def draw(self, n=1):
        return [self.cards.pop(0) for _ in range(n)]

    def add(self, *cards):
        self.cards.extend(cards)
        return self

    def remove(self, *cards):
        for card in cards:
            self.cards.remove(card)
        return self

    def get_index(self, card):
        if not isinstance(card, self._card_type):
            raise TypeError("Invalid card type: must be a Card object")
        return [i for i, c in enumerate(self.cards) if c == card]

    def get_cards(self):
        return self.cards

    def get_top_card(self):
        return self.cards[0] if self.cards else None

    def __str__(self):
        deck_string = f"Deck of {len(self)} cards."
        top_card = f" Top card: {self[0]}" if self.cards else ""
        return deck_string + top_card

    def __repr__(self):
        return (f"{self.__class__.__name__}("
                f"card_type={self._card_type!r}, "
                f"cards={self.cards!r})")

    def __copy__(self):
        return self.__class__(self.cards.copy())

    def __getitem__(self, key): return self.cards[key]
    def __len__(self): return len(self.cards)
    def __iter__(self): return iter(self.cards)

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self.cards == other.cards

    def __ne__(self, other): return not self.__eq__(other)


class CardMeta(type):
    def __new__(cls, name, bases, class_dict, rank_type, suit_type):
        class_dict["RANKS"] = list(get_args(rank_type))
        class_dict["SUITS"] = list(get_args(suit_type))
        return super().__new__(cls, name, bases, class_dict)


class DeckMeta(type):
    def __new__(cls, name, bases, class_dict, card_type):
        class_dict["_card_type"] = card_type
        return super().__new__(cls, name, bases, class_dict)
