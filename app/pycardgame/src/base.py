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


class Card:
    suit_names = ["Clubs", "Diamonds", "Hearts", "Spades"]
    rank_names = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "Jack", "Queen", "King", "Ace"]

    def __init__(self, rank, suit, trump=False, **kwargs):
        if type(suit) is str:
            try: suit = Card.suit_names.index(suit)
            except ValueError: raise ValueError(f"Invalid suit name: {suit}")
        if type(rank) is str:
            try: rank = Card.rank_names.index(rank)
            except ValueError: raise ValueError(f"Invalid rank name: {rank}")

        self.rank = rank
        self.suit = suit
        self.trump = trump

        # Set any additional attributes
        for key, value in kwargs.items():
            setattr(self, key, value)

    def get_suit(self, as_index=False):
        return self.suit if as_index else Card.suit_names[self.suit]

    def get_rank(self, as_index=False):
        return self.rank if as_index else Card.rank_names[self.rank]

    def __str__(self):
        return f"{Card.rank_names[self.rank]} of {Card.suit_names[self.suit]}{' (trump)' if self.trump else ''}"

    def __repr__(self):
        return f"{self.__class__.__name__}(rank={self.rank}, suit={self.suit}{', trump=True' if self.trump else ''})"

    def __lt__(self, other):
        if self.trump and not other.trump: return False
        if not self.trump and other.trump: return True
        t1 = self.suit, self.rank
        t2 = other.suit, other.rank
        return t1 < t2

    def __eq__(self, other): return self.suit == other.suit and self.rank == other.rank
    def __gt__(self, other): return not self.__lt__(other) and not self.__eq__(other)
    def __le__(self, other): return not self.__gt__(other)
    def __ge__(self, other): return not self.__lt__(other)
    def __ne__(self, other): return not self.__eq__(other)


class Deck:
    def __init__(self, cards=None):
        if cards is None: self.cards = self.reset().get_cards()
        else: self.cards = cards

    def reset(self):
        self.cards = [Card(rank, suit) for suit in range(len(Card.suit_names)) for rank in range(len(Card.rank_names))]
        return self.sort()

    def count(self, card):
        if isinstance(card, Card):
            return self.cards.count(card)
        elif isinstance(card, int):
            return sum(1 for c in self.cards if c.rank == card or c.suit == card)
        elif isinstance(card, str):
            if card in Card.rank_names:
                rank_index = Card.rank_names.index(card)
                return sum(1 for c in self.cards if c.rank == rank_index)
            elif card in Card.suit_names:
                suit_index = Card.suit_names.index(card)
                return sum(1 for c in self.cards if c.suit == suit_index)
            else:
                raise ValueError(f"Invalid rank or suit name: {card}")
        else:
            raise TypeError("Argument must be of type Card, int, or str")

    def sort(self, by="suit"):
        self.cards.sort(key=lambda c: (c.suit, c.rank) if by == "suit" else lambda c: (c.rank, c.suit))
        return self

    def shuffle(self): random.shuffle(self.cards); return self
    def draw(self, n=1): return [self.cards.pop() for _ in range(n)] if n > 1 else self.cards.pop()
    def add(self, card): self.cards.append(card); return self
    def get_index(self, card): return [i for i, c in enumerate(self.cards) if c == card]
    def get_cards(self): return self.cards

    def __getitem__(self, index): return self.cards[index]
    def __len__(self): return len(self.cards)
    def __str__(self): return f"Deck of {len(self)} cards"
    def __repr__(self): return f"{self.__class__.__name__}(cards={self.cards})"
    def __iter__(self): return iter(self.cards)
