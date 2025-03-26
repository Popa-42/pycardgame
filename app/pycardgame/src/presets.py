from typing import Literal, get_args

from .. import GenericCard, GenericDeck, GenericPlayer, GenericGame

ranks = Literal["2", "3", "4", "5", "6", "7", "8", "9", "10", "Jack", "Queen",
                "King", "Ace"]
suits = Literal["Diamonds", "Hearts", "Spades", "Clubs"]


class PokerCard(GenericCard[ranks, suits]):
    RANKS = list(get_args(ranks))
    SUITS = list(get_args(suits))


class PokerDeck(GenericDeck[PokerCard]):
    def __init__(self, cards=None, card_type=PokerCard):
        super().__init__(card_type, cards=cards)


class PokerPlayer(GenericPlayer[PokerCard]):
    ...


class PokerGame(GenericGame[PokerCard]):
    def __init__(self, starting_player_index=0, *players):
        super().__init__(PokerCard, PokerDeck, deck=None, discard_pile=None,
                         trump=None, hand_size=2,
                         starting_player_index=starting_player_index, *players)
        self.trash_pile = []
        self.trash_pile_limit = 2
        self.trash_pile_index = 0
