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
    # Ascending order of suits and ranks
    rank_names = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "Jack", "Queen",
                  "King", "Ace"]
    suit_names = ["Clubs", "Diamonds", "Hearts", "Spades"]

    def __init__(self, rank, suit, trump=False, **kwargs):
        self.rank = None
        self.suit = None

        if rank is not None:
            self.set_rank(rank)
        if suit is not None:
            self.set_suit(suit)

        self.trump = trump

        # Set any additional attributes
        for key, value in kwargs.items():
            setattr(self, key, value)

    def get_suit(self, as_index=False):
        if self.suit is None:
            return None
        return self.suit if as_index else Card.suit_names[self.suit]

    def set_suit(self, suit):
        if isinstance(suit, str):
            if suit not in Card.suit_names:
                raise ValueError(f"Invalid suit name: {suit}")
            suit = Card.suit_names.index(suit)
        elif not isinstance(suit, int):
            raise ValueError("Suit must be None, an int, or a valid suit name")
        if suit < 0 or suit >= len(Card.suit_names):
            raise ValueError(f"Invalid suit index: {suit}")
        self.suit = suit
        return self

    def get_rank(self, as_index=False):
        if self.rank is None:
            return None
        return self.rank if as_index else Card.rank_names[self.rank]

    def set_rank(self, rank):
        if isinstance(rank, str):
            if rank not in Card.rank_names:
                raise ValueError(f"Invalid rank name: {rank}")
            rank = Card.rank_names.index(rank)
        elif not isinstance(rank, int):
            raise ValueError("Rank must be None, an int, or a valid rank name")
        if rank < 0 or rank >= len(Card.rank_names):
            raise ValueError(f"Invalid rank index: {rank}")
        self.rank = rank
        return self

    def get_trump(self):
        return self.trump

    def set_trump(self, trump):
        self.trump = trump
        return self

    def __str__(self):
        rank_str = Card.rank_names[self.rank] if self.rank is not None \
            else "None"
        suit_str = Card.suit_names[self.suit] if self.suit is not None \
            else "None"
        return f"{rank_str} of {suit_str}{' (trump)' if self.trump else ''}"

    def __repr__(self):
        additional = ", ".join(f"{k}={v!r}" for k, v in self.__dict__.items()
                               if k not in ("rank", "suit", "trump"))
        return (f"{self.__class__.__name__}(rank={self.rank!r}, "
                f"suit={self.suit!r}{', trump=True' if self.trump else ''}"
                f"{f', {additional}' if additional else ''})")

    def __lt__(self, other):
        if self.trump and not other.trump:
            return False
        if not self.trump and other.trump:
            return True
        # Define None as -1, so that defined cards are always greater than None
        suit1 = self.suit if self.suit is not None else -1
        suit2 = other.suit if other.suit is not None else -1
        rank1 = self.rank if self.rank is not None else -1
        rank2 = other.rank if other.rank is not None else -1
        return (suit1, rank1) < (suit2, rank2)

    def __eq__(self, other):
        return self.suit == other.suit and self.rank == other.rank

    def __gt__(self, other):
        return not self.__lt__(other) and not self.__eq__(other)

    def __le__(self, other): return not self.__gt__(other)
    def __ge__(self, other): return not self.__lt__(other)
    def __ne__(self, other): return not self.__eq__(other)


class Deck:
    def __init__(self, cards=None):
        if cards is None:
            self.cards = self.reset().get_cards()
        else:
            self.cards = cards

    def reset(self):
        self.cards = [Card(rank, suit) for suit in range(len(Card.suit_names))
                      for rank in range(len(Card.rank_names))]
        return self.sort()

    def count(self, card):
        if isinstance(card, Card):
            return self.cards.count(card)
        elif isinstance(card, str):
            if card in Card.rank_names:
                return sum(1 for c in self.cards if c.get_rank() == card)
            elif card in Card.suit_names:
                return sum(1 for c in self.cards if c.get_suit() == card)
            else:
                raise ValueError(
                    "Invalid card name: must be a rank or suit name")
        else:
            raise ValueError(
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
        random.shuffle(self.cards)
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
        return [i for i, c in enumerate(self.cards) if c == card]

    def get_cards(self):
        return self.cards

    def get_top_card(self):
        return self.cards[-1] if self.cards else None

    def __repr__(self):
        return f"{self.__class__.__name__}(cards={self.cards!r})"

    def __str__(self):
        deck_string = f"Deck of {len(self)} cards."
        top_card = f" Top card: {self[0]}" if self.cards else ""
        return deck_string + top_card

    def __getitem__(self, key): return self.cards[key]
    def __len__(self): return len(self.cards)
    def __iter__(self): return iter(self.cards)
