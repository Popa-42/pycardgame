from .base import Deck, Card


class PokerDeck(Deck):
    def __init__(self, cards=None):
        super().__init__(cards)


class UnoCard(Card):
    RANKS = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "Skip",
             "Reverse", "Draw Two", "Wild", "Wild Draw Four"]
    SUITS = ["Red", "Green", "Blue", "Yellow", "Wild"]

    def __init__(self, suit, rank):
        super().__init__(rank, suit)

    def __str__(self):
        return f"{self.get_suit()} {self.get_rank()}"


class UnoDeck(Deck):
    def __init__(self, cards=None):
        super().__init__(cards)

    def reset(self):
        # Clear the current cards list
        self.cards = []
        colors = ["Red", "Green", "Blue", "Yellow"]

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
