from typing import Literal, get_args, List

from .. import GenericCard, GenericDeck, GenericPlayer, GenericGame

ranks = Literal["2", "3", "4", "5", "6", "7", "8", "9", "10", "Jack", "Queen",
                "King", "Ace"]
suits = Literal["Diamonds", "Hearts", "Spades", "Clubs"]


class PokerCard(GenericCard[ranks, suits]):
    """
    A card for a standard 52-card deck
    """
    RANKS: List[ranks] = ...
    SUITS: List[suits] = ...


class PokerDeck(GenericDeck[PokerCard]):
    def __init__(self) -> None: ...


class PokerPlayer(GenericPlayer[PokerCard]): ...


class PokerGame(GenericGame[PokerCard]):
    def __init__(self, starting_player_index: int = 0,
                 *players: PokerPlayer) -> None:
        self.trash_pile: List[PokerCard] = []
        self.trash_pile_limit: int = 2
        self.trash_pile_index: int = 0
