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


class UnoCard(Card):
    """
    A UNO card implementation extending the base Card class. Defines
    UNO-specific ranks and suits.
    """

    RankType = Literal["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "Skip",
    "Reverse", "Draw Two", "Wild", "Wild Draw Four"]
    SuitType = Literal["Red", "Yellow", "Green", "Blue"]
    RANKS: List[RankType]
    SUITS: List[SuitType]

    def __init__(self,
                 suit: Union[SuitType, int],
                 rank: Union[RankType, int]) -> None:
        """
        Initialize a `UnoCard` with a suit and a rank.
        :param suit: The suit of the Uno card (e.g., "Red", "Green", etc.).
        :param rank: The rank of the Uno card (e.g., "0", "Skip", 5, etc.).
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
