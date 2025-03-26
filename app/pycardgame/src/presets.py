from typing import Literal, get_args, List

from .. import GenericCard, GenericDeck, GenericPlayer, GenericGame

ranks = Literal["2", "3", "4", "5", "6", "7", "8", "9", "10", "Jack", "Queen",
                "King", "Ace"]
suits = Literal["Diamonds", "Hearts", "Spades", "Clubs"]


class PokerCard(GenericCard[ranks, suits]):
    RANKS = list(get_args(ranks))
    SUITS = list(get_args(suits))


class PokerDeck(GenericDeck[PokerCard]):
    def __init__(self):
        super().__init__(PokerCard)


class PokerPlayer(GenericPlayer[PokerCard]): ...


class PokerGame(GenericGame[PokerCard]):
    def __init__(self, starting_player_index=0, *players):
        super().__init__(PokerCard, PokerDeck, None, None, None, 2,
                         starting_player_index, *players)
        self.trash_pile = []
        self.trash_pile_limit = 2
        self.trash_pile_index = 0
