from typing import Literal

from .. import (
    CardMeta,
    DeckMeta,
    GenericCard,
    GenericDeck,
    GenericGame,
    GenericPlayer,
)

T_Ranks = Literal["2", "3", "4", "5", "6", "7", "8", "9", "10", "Jack",
                  "Queen", "King", "Ace"]
T_Suits = Literal["Diamonds", "Hearts", "Spades", "Clubs"]


class PokerCard(
    GenericCard[T_Ranks, T_Suits],
    metaclass=CardMeta,
    rank_type=T_Ranks,
    suit_type=T_Suits
):
    ...


class PokerDeck(
    GenericDeck[PokerCard],
    metaclass=DeckMeta,
    card_type=PokerCard
):
    ...


class PokerPlayer(GenericPlayer[PokerCard]):
    ...


class PokerGame(GenericGame[PokerCard]):
    def __init__(self, starting_player_index=0, *players):
        super().__init__(PokerCard, PokerDeck, None, None, None, 2,
                         starting_player_index, *players)
        self.trash_pile = []
        self.trash_pile_limit = 2
        self.trash_pile_index = 0
