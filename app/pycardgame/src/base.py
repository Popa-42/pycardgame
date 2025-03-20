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

    def __init__(self, rank: int | str, suit: int | str, trump: bool = False, **kwargs) -> None:
        if type(suit) is str:
            try: suit = Card.suit_names.index(suit)
            except ValueError: raise ValueError(f"Invalid suit name: {suit}")
        if type(rank) is str:
            try: rank = Card.rank_names.index(rank)
            except ValueError: raise ValueError(f"Invalid rank name: {rank}")

        self.suit: int = suit
        self.rank: int = rank
        self.trump: bool = trump

        # Set any additional attributes
        for key, value in kwargs.items():
            setattr(self, key, value)

    def get_suit(self, index: bool = False) -> int | str:
        """
        Return the suit of the card.
        :param index: If True, return the index of the suit.
        """
        return self.suit if index else Card.suit_names[self.suit]

    def get_rank(self, index: bool = False) -> int | str:
        """
        Return the rank of the card.
        :param index: If True, return the index of the rank.
        """
        return self.rank if index else Card.rank_names[self.rank]

    def __str__(self) -> str:
        return f"{Card.rank_names[self.rank]} of {Card.suit_names[self.suit]}{' (trump)' if self.trump else ''}"

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(rank={self.rank}, suit={self.suit}{', trump=True' if self.trump else ''})"

    def __lt__(self, other: Card) -> bool:
        if self.trump and not other.trump:
            return False
        if not self.trump and other.trump:
            return True
        t1 = self.suit, self.rank
        t2 = other.suit, other.rank
        return t1 < t2

    def __eq__(self, other: Card) -> bool:
        return self.suit == other.suit and self.rank == other.rank

    def __gt__(self, other: Card) -> bool:
        return not self.__lt__(other) and not self.__eq__(other)

    def __le__(self, other: Card) -> bool:
        return not self.__gt__(other)

    def __ge__(self, other: Card) -> bool:
        return not self.__lt__(other)

    def __ne__(self, other: Card) -> bool:
        return not self.__eq__(other)


class Deck:
    """
    A deck of cards.
    :param cards: A list of cards to initialize the deck with.
    """

    def __init__(self, cards: list[Card] = None) -> None:
        """
        Initialize the deck with a list of cards.
        :param cards: A list of cards to initialize the deck with.
        """
        if cards is None: self.cards = [Card(rank, suit) for suit in range(len(Card.suit_names)) \
            for rank in range(len(Card.rank_names))]
        else: self.cards = cards

    def shuffle(self) -> Deck:
        """Shuffle the deck."""
        random.shuffle(self.cards)
        return self

    def draw(self) -> Card:
        """Draw a card from the deck."""
        return self.cards.pop()

    def add(self, card: Card) -> Deck:
        """Add a card to the end of deck."""
        self.cards.append(card)
        return self

    def reset(self) -> Deck:
        """Reset the deck to a new deck of cards."""
        self.cards = [Card(rank, suit) for suit in range(len(Card.suit_names)) \
            for rank in range(len(Card.rank_names))]
        return self.sort()

    def sort(self) -> Deck:
        """Sorts and returns the deck."""
        self.cards.sort()
        return self

    def get_index(self, card: Card) -> list[int]:
        """Return the indices of all occurrences of a card in the deck."""
        return [i for i, c in enumerate(self.cards) if c == card]

    def count(self, card: Card) -> int:
        """Return the number of occurrences of a card in the deck."""
        return self.cards.count(card)

    def __getitem__(self, index: int) -> Card:
        return self.cards[index]

    def __len__(self) -> int:
        return len(self.cards)

    def __str__(self) -> str:
        return f"Deck of {len(self)} cards"

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(cards={self.cards})"

    def __iter__(self) -> iter:
        return iter(self.cards)
