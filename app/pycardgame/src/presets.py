from typing import Type

from .base import Deck, Card


class PokerDeck(Deck):
    def __init__(self, cards=None):
        super().__init__(cards)


class SkatCard(Card):
    RANKS = ["7", "8", "9", "10", "Jack", "Queen", "King", "Ace"]
    SUITS = ["Diamonds", "Hearts", "Spades", "Clubs"]

    def __init__(self, rank, suit):
        if rank not in self.RANKS:
            raise ValueError(f"Invalid rank for Skat card: {rank}")
        if suit not in self.SUITS:
            raise ValueError(f"Invalid suit for Skat card: {suit}")
        self.rank = rank
        self.suit = suit
        super().__init__(rank, suit)


class SkatDeck(Deck):
    def __init__(self, cards=None):
        super().__init__(cards, card_type=SkatCard)


class UnoCard(Card):
    RANKS = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "Skip",
             "Reverse", "Draw Two", "Wild", "Wild Draw Four"]
    SUITS = ["Red", "Green", "Blue", "Yellow", "Wild"]

    def __init__(self, rank, suit):
        super().__init__(rank, suit)

    def __str__(self):
        return f"{self.get_suit()} {self.get_rank()}"


class UnoDeck(Deck):
    def __init__(self, cards=None):
        super().__init__(cards, card_type=UnoCard)

    def reset(self):
        # Clear the current cards list
        self.cards = []
        colors = [suit for suit in UnoCard.SUITS if suit != "Wild"]

        for color in colors:
            # Add one 0 card
            self.cards.append(UnoCard(suit=color, rank="0"))
            # Add two of each number card from 1 to 9
            for num in range(1, 13):
                self.cards.append(UnoCard(suit=color, rank=num))
                self.cards.append(UnoCard(suit=color, rank=num))

        # Add Wild and Wild Draw Four cards (color is "Wild")
        self.cards.extend([UnoCard(suit="Wild", rank="Wild")] * 4)
        self.cards.extend([UnoCard(suit="Wild", rank="Wild Draw Four")] * 4)

        return self.sort()


class SixNimmtCard(Card):
    RANKS = [i for i in range(1, 105)]

    def __init__(self, value):
        self.value = value
        self.bull_heads = self.calculate_bull_heads(value)
        super().__init__(None, value)

    @staticmethod
    def calculate_bull_heads(value):
        if value == 55:
            return 7
        elif value % 11 == 0:
            return 5
        elif value % 10 == 0:
            return 3
        elif value % 5 == 0:
            return 2
        else:
            return 1

    def __str__(self): return f"{self.value} ({self.bull_heads} bull heads)"
    def __repr__(self): return f"{self.__class__.__name__}({self.value})"


class SixNimmtDeck(Deck):
    def __init__(self, cards=None):
        super().__init__(cards, card_type=SixNimmtCard)

    def reset(self):
        self.cards = [SixNimmtCard(value) for value in SixNimmtCard.RANKS]
        return self.sort()
