from typing import Literal, get_args, List

from .base import GenericCard, GenericDeck

ranks = Literal["2", "3", "4", "5", "6", "7", "8", "9", "10", "Jack", "Queen",
                "King", "Ace"]
suits = Literal["Diamonds", "Hearts", "Spades", "Clubs"]


class PokerCard(GenericCard[ranks, suits]):
    RANKS: List[ranks] = list(get_args(ranks))
    SUITS: List[suits] = list(get_args(suits))


class PokerDeck(GenericDeck[PokerCard]):
    def __init__(self):
        super().__init__(PokerCard)
