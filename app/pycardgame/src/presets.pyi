from typing import List, Optional, Union, Literal
from .base import Card, Deck


class PokerDeck(Deck[Card]):
    def __init__(self, cards: Optional[List[Card]] = None) -> None: ...


class UnoCard(Card):
    RankType = Literal["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "Skip",
                       "Reverse", "Draw Two", "Wild", "Wild Draw Four"]
    SuitType = Literal["Red", "Yellow", "Green", "Blue"]
    RANKS: List[RankType]
    SUITS: List[SuitType]

    def __init__(self, suit: Union[SuitType, int], rank: Union[RankType, int]) -> None: ...
    def __str__(self) -> str: ...


class UnoDeck(Deck[UnoCard]):
    def __init__(self, cards: Optional[List[UnoCard]] = None) -> None: ...
