from typing import Literal, List, Type

from .. import GenericCard, GenericDeck, GenericPlayer, GenericGame

_T_Ranks = Literal["2", "3", "4", "5", "6", "7", "8", "9", "10", "Jack",
                   "Queen", "King", "Ace"]
_T_Suits = Literal["Diamonds", "Hearts", "Spades", "Clubs"]


class PokerCard(GenericCard[_T_Ranks, _T_Suits]):
    """
    A card for a standard 52-card deck.
    :param rank: The rank of the card.
    :param suit: The suit of the card
    """
    RANKS: List[_T_Ranks] = ...
    SUITS: List[_T_Suits] = ...

    def __init__(self, rank: _T_Ranks, suit: _T_Suits) -> None:
        """
        Initialize the card.
        :param rank: The rank of the card.
        :param suit: The suit of the card.
        """
        pass


class PokerDeck(GenericDeck[PokerCard]):
    """
    A deck of cards for a standard 52-card deck.

    :param cards: The cards in the deck.
    :param card_type: The type of card to use.
    """
    def __init__(self, cards: List[PokerCard] = None,  # type: ignore
                 card_type: Type[PokerCard] = PokerCard) -> None:
        """
        Initialize the deck.
        :param cards: The cards in the deck.
        :param card_type: The type of card to use.
        """
        pass


class PokerPlayer(GenericPlayer[PokerCard]):
    """
    A player for a standard game of poker.
    :param name: The player's name.
    :param hand: The player's hand.
    :param score: The player's score.
    """

    def __init__(self, name: str, hand: List[PokerCard] = None,  # type: ignore
                 score: int = 0) -> None:
        """
        Initialize the player.
        :param name: The player's name.
        :param hand: The player's hand.
        :param score: The player's score.
        """
        pass


class PokerGame(GenericGame[PokerCard]):
    """
    The base class for a game of poker.
    :param starting_player_index: The index of the starting player.
    :param players: The players in the game.
    """
    def __init__(self, starting_player_index: int = 0,
                 *players: PokerPlayer) -> None:
        """
        Initialize the game.
        :param starting_player_index: The index of the starting player.
        :param players: The players in the game.
        """
        self.trash_pile: List[PokerCard] = []
        self.trash_pile_limit: int = 2
        self.trash_pile_index: int = 0
