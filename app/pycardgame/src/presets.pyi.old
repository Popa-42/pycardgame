from typing import List, Optional, Union, Literal
from .base import Card, Deck


class PokerDeck(Deck[Card]):
    """
    A deck implementation for Poker games. Inherits from the base Deck class.
    """

    def __init__(self, cards: Optional[List[Card]] = None) -> None:
        """
        Initialize a PokerDeck instance.
        :param cards: Optional list of Card objects to initialize the deck.
        """
        pass


class SkatCard(Card):
    """
    A Skat card implementation extending the base `Card` class. Defines
    Skat-specific ranks and suits.
    """

    RankType = Literal["7", "8", "9", "10", "Jack", "Queen", "King", "Ace"]
    SuitType = Literal["Diamonds", "Hearts", "Spades", "Clubs"]
    RANKS: List[RankType]
    SUITS: List[SuitType]

    def __init__(self,
                 rank: Union[RankType, int],
                 suit: Union[SuitType, int]) -> None:
        """
        Initialize a Skat card with a suit and a rank.
        :param rank: The rank of the Skat card (e.g., "7", "Jack", etc.).
        :param suit: The suit of the Skat card (e.g., "Clubs", "Spades", etc.).
        """
        pass


class SkatDeck(Deck[SkatCard]):
    """
    A deck implementation for Skat games. Inherits from the base Deck class.
    """

    def __init__(self, cards: Optional[List[SkatCard]] = None) -> None:
        """
        Initialize a SkatDeck instance.
        :param cards: Optional list of Card objects to initialize the deck.
        """
        pass


class UnoCard(Card):
    """
    A UNO card implementation extending the base Card class. Defines
    UNO-specific ranks and suits.
    """

    RankType = Literal["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "Skip",
    "Reverse", "Draw Two", "Wild", "Wild Draw Four"]
    SuitType = Literal["Red", "Yellow", "Green", "Blue", "Wild"]
    RANKS: List[RankType]
    SUITS: List[SuitType]

    def __init__(self,
                 rank: Union[RankType, int],
                 suit: Union[SuitType, int]) -> None:
        """
        Initialize a `UnoCard` with a suit and a rank.
        :param rank: The rank of the Uno card (e.g., "0", "Skip", 5, etc.).
        :param suit: The suit of the Uno card (e.g., "Red", "Green", etc.).
        """
        pass


class UnoDeck(Deck[UnoCard]):
    """
    A deck implementation for UNO games. Inherits from the base Deck class and
    customizes it for Uno cards.
    """

    def __init__(self, cards: Optional[List[UnoCard]] = None) -> None:
        """
        Initialize an `UnoDeck` instance.
        :param cards: Optional list of UnoCard objects to initialize the deck.
        """
        pass

    def reset(self) -> UnoDeck:
        """
        Reset the `UnoDeck` instance to its initial state with a full set of Uno
        cards.
        :return: The reset `UnoDeck` instance.
        """
        pass


class SixNimmtCard(Card):
    """
    Represents a card in the game "6 Nimmt!".

    Every card has a numeric value between 1 and 104, and a number of bull heads
    associated with it. The number of bull heads is determined by the value of
    the card according to the game rules.
    """
    RankType = Literal[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16,
                       17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30,
                       31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44,
                       45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58,
                       59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72,
                       73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86,
                       87, 88, 89, 90, 91, 92, 93, 94, 95, 96, 97, 98, 99, 100,
                       101, 102, 103, 104]
    RANKS: List[RankType]

    def __init__(self, value: RankType) -> None:
        """
        Initialize a card with a numeric value and calculate the number of bull
        heads associated with it.
        :param value: The numeric value of the card (between 1 and 104).
        :raises ValueError: If the value is not within the valid range.
        """
        pass

    @staticmethod
    def calculate_bull_heads(value: RankType) -> Literal[7, 5, 3, 2, 1]:
        """
        Calculate the number of bull heads for a card based on the game rules.

        Rules
          - Card 55 has 7 Bull Heads.
          - Cards divisible by 11 have 5 Bull Heads.
          - Cards divisible by 10 have 3 Bull Heads.
          - Cards divisible by 5 have 2 Bull Heads.
          - All other cards have 1 Bull Head.

        :param value: The numeric value of the card.
        :return: The number of bull heads associated with the card.
        """
        pass


class SixNimmtDeck(Deck[SixNimmtCard]):
    """
    A deck implementation for the game "6 Nimmt!".
    """

    def __init__(self, cards: Optional[List[SixNimmtCard]] = None) -> None:
        """
        Initialize a `SixNimmtDeck` instance.
        :param cards: Optional list of `SixNimmtCard` objects to initialize the
        deck with.
        """
        pass

    def reset(self) -> SixNimmtDeck:
        """
        Reset the deck to its initial state with a full set of "6 Nimmt!" cards.
        :return: The reset `SixNimmtDeck` instance.
        """
        pass
