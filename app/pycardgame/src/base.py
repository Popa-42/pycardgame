# PyCardGame - A base library for creating card games in Python
# Copyright (C) 2025  Popa-42
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

from __future__ import annotations

import random
from abc import ABC, ABCMeta, abstractmethod
from typing import Generic, get_args, MutableSequence, Type, TypeVar

_RankT = TypeVar("_RankT")
_SuitT = TypeVar("_SuitT")


class CardMeta(ABCMeta):
    def __new__(cls, name, bases, class_dict, rank_type, suit_type):
        class_dict["RANKS"] = list(get_args(rank_type))
        class_dict["SUITS"] = list(get_args(suit_type))
        return super().__new__(cls, name, bases, class_dict)


class GenericCard(ABC, Generic[_RankT, _SuitT]):
    __slots__ = ("rank", "suit", "trump")

    RANKS: MutableSequence[_RankT] = []
    SUITS: MutableSequence[_SuitT] = []

    def __init__(self, rank, suit, trump=False):
        self.rank = None
        self.suit = None

        if rank is not None:
            self.change_rank(rank)
        if suit is not None:
            self.change_suit(suit)

        self.trump = trump

    @staticmethod
    def _set_value(value, values_list, value_name):
        if not isinstance(value, int):
            if value is None:
                return None
            elif value not in values_list:
                raise ValueError(f"Invalid {value_name} name: {value}")
            value = values_list.index(value)
        else:
            if value < 0 or value >= len(values_list):
                raise ValueError(f"Invalid {value_name} index: {value}")
        return value

    @abstractmethod
    def effect(self, game, player, *args):  # pragma: no cover
        pass

    def get_rank(self, as_index=False):
        if self.rank is None:
            return None
        return self.rank if as_index else self.__class__.RANKS[self.rank]

    def change_rank(self, rank):
        self.rank = self._set_value(rank, self.__class__.RANKS, "rank")
        return self

    def get_suit(self, as_index=False):
        if self.suit is None:
            return None
        return self.suit if as_index else self.__class__.SUITS[self.suit]

    def change_suit(self, suit):
        self.suit = self._set_value(suit, self.__class__.SUITS, "suit")
        return self

    def is_trump(self):
        return self.trump

    def set_trump(self, trump):
        if not isinstance(trump, bool):
            raise TypeError("Trump must be a boolean value")
        self.trump = trump
        return self

    def __copy__(self):
        return self.__class__(rank=self.rank, suit=self.suit, trump=self.trump)

    def __str__(self):
        rank_str = str(self.get_rank(as_index=False))
        suit_str = str(self.get_suit(as_index=False))
        return f"{suit_str} {rank_str}{' (trump)' if self.trump else ''}"

    def __repr__(self):
        return (f"{self.__class__.__name__}(rank={self.rank!r}, "
                f"suit={self.suit!r}{', trump=True' if self.trump else ''})")

    def __lt__(self, other):
        if self.trump and not other.trump:
            return False
        if not self.trump and other.trump:
            return True
        # Defined cards are always greater than None
        suit1 = self.suit if self.suit is not None else float("-inf")
        suit2 = other.suit if other.suit is not None else float("-inf")
        rank1 = self.rank if self.rank is not None else float("-inf")
        rank2 = other.rank if other.rank is not None else float("-inf")
        return (suit1, rank1) < (suit2, rank2)

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return (self.suit == other.suit and self.rank == other.rank and
                self.trump == other.trump)

    def __ne__(self, other):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return not self.__eq__(other)

    def __gt__(self, other):
        return not self.__lt__(other) and not self.__eq__(other)

    def __le__(self, other):
        return not self.__gt__(other)

    def __ge__(self, other):
        return not self.__lt__(other)


_CardT = TypeVar("_CardT", bound=GenericCard)


class DeckMeta(ABCMeta):
    def __new__(cls, name, bases, class_dict, card_type):
        class_dict["_card_type"] = card_type
        return super().__new__(cls, name, bases, class_dict)


class GenericDeck(ABC, Generic[_CardT]):
    _card_type: Type[_CardT]
    __hash__ = None  # type: ignore  # Mutable type, so hash is not defined

    def __init__(self, cards=None):
        if cards is None:
            self.cards = self.reset().get_cards()
        else:
            self.cards = list(cards)

    def reset(self):
        self.cards = [self._card_type(rank, suit)
                      for suit in range(len(self._card_type.SUITS))
                      for rank in range(len(self._card_type.RANKS))]
        return self.sort()

    def count(self, card):
        if isinstance(card, self._card_type):
            return self.cards.count(card)
        elif isinstance(card, str):
            if card in self._card_type.RANKS:
                return sum(1 for c in self.cards if c.get_rank() == card)
            elif card in self._card_type.SUITS:
                return sum(1 for c in self.cards if c.get_suit() == card)
            else:
                raise ValueError(
                    "Invalid card name: must be a rank or suit name")
        else:
            raise TypeError(
                "Invalid card type: must be a Card object, a suit, or a rank")

    def sort(self, by="suit"):
        if by == "rank":
            self.cards.sort(key=lambda c: (
                not c.trump, c.rank if c.rank is not None else -1,
                c.suit if c.suit is not None else -1))
        elif by == "suit":
            self.cards.sort()
        else:
            raise ValueError("Invalid sort key: must be 'rank' or 'suit'")
        return self

    def shuffle(self, seed=None):
        if seed is not None:
            random.seed(seed)
        random.shuffle(self.cards)
        return self

    def draw(self, n=1):
        if n < 1 or n > len(self.cards):
            raise ValueError(f"Cannot draw {n} cards: number of cards to draw must be between 1 and {len(self.cards)}")
        return self.cards.pop(0) if n == 1 else [self.cards.pop(0) for _ in (
            range(n))]

    def add(self, *cards, to_top=False):
        if not all(isinstance(card, self._card_type) for card in cards):
            raise TypeError("Invalid card type: must be a Card object")
        if to_top:
            self.cards = list(cards) + self.cards
        else:
            self.cards.extend(cards)
        return self

    def remove(self, *cards):
        if not all(isinstance(card, self._card_type) for card in cards):
            raise TypeError("Invalid card type: must be a Card object")
        for card in cards:
            self.cards.remove(card)
        return self

    def clear(self):
        self.cards.clear()
        return self

    def get_index(self, card):
        if not isinstance(card, self._card_type):
            raise TypeError("Invalid card type: must be a Card object")
        return [i for i, c in enumerate(self.cards) if c == card]

    def get_cards(self):
        return self.cards

    def get_top_card(self):
        return self.cards[0] if self.cards else None

    def __str__(self):
        deck_string = f"Deck of {len(self)} cards."
        top_card = f" Top card: {self[0]}" if self.cards else ""
        return deck_string + top_card

    def __repr__(self):
        return (f"{self.__class__.__name__}("
                f"card_type={self._card_type!r}, "
                f"cards={self.cards!r})")

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self.cards == other.cards

    def __ne__(self, other):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return not self.__eq__(other)

    def __copy__(self):
        return self.__class__(cards=self.cards.copy())

    def __getitem__(self, key):
        return self.cards[key]

    def __len__(self):
        return len(self.cards)

    def __iter__(self):
        return iter(self.cards)

    def __contains__(self, item):
        if not isinstance(item, self._card_type):
            return False
        return item in self.cards

    def __bool__(self):
        return bool(self.cards)


class GenericPlayer(ABC, Generic[_CardT]):
    __slots__ = ("name", "hand", "score")

    def __init__(self, name, hand=None, score=0):
        self.name = name
        self.hand = hand or []
        self.score = score

    def add_cards(self, *cards):
        self.hand.extend(cards)

    def remove_cards(self, *cards):
        for card in cards:
            self.hand.remove(card)
        return self

    def play_cards(self, *cards):
        if not cards:
            cards = self.hand
        for card in cards:
            self.hand.remove(card)
        return list(cards)

    def get_hand(self):
        return self.hand

    def get_score(self):
        return self.score

    def set_score(self, score):
        self.score = score
        return self

    def get_name(self):
        return self.name

    def set_name(self, name):
        self.name = name
        return self

    def __getitem__(self, key):
        return self.hand[key]

    def __str__(self):
        return f"Player {self.name} ({len(self.hand)} card(s)):\n" + "\n".join(
            f" - {card}" for card in self.hand)

    def __repr__(self):
        return (f"{self.__class__.__name__}({self.name!r}, hand={self.hand!r},"
                f" score={self.score!r})")

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return (self.score == other.score and self.hand == other.hand and
                self.name == other.name)

    def __ne__(self, other):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return not self.__eq__(other)

    def __lt__(self, other):
        return self.score < other.score

    def __le__(self, other):
        return self.score <= other.score

    def __gt__(self, other):
        return self.score > other.score

    def __ge__(self, other):
        return self.score >= other.score

    def __bool__(self):
        return bool(self.hand) and self.score >= 0

    def __iter__(self):
        return iter(self.hand)

    def __len__(self):
        return len(self.hand)


class GenericGame(ABC, Generic[_CardT]):
    def __init__(self, card_type, deck_type, draw_pile=None, discard_pile=None,
                 trump=None, hand_size=4, starting_player_index=0,
                 do_not_shuffle=False, *players):
        self._card_type = card_type
        self._deck_type = deck_type

        if trump is not None and trump not in self._card_type.SUITS:
            raise ValueError(f"Invalid suit for trump: {trump}")

        self.draw_pile = draw_pile if draw_pile is not None \
            else self._deck_type()
        if not do_not_shuffle:
            self.draw_pile.shuffle()

        self.discard_pile = discard_pile or self._deck_type(cards=[])

        self.trump = None
        if trump is not None:
            self.set_trump(trump)
        self.apply_trump()

        self.hand_size = hand_size

        self.players = list(players)

        start_idx = starting_player_index
        if start_idx != 0:  # 0 is a valid index
            if start_idx < 0 or start_idx >= len(self.players):
                raise ValueError(f"Invalid starting player index: {start_idx} "
                                 f"> {len(self.players)} {self.players}")
        self.current_player_index = start_idx

        self.direction = 1  # 1 for clockwise, -1 for counter-clockwise

    @abstractmethod
    def check_valid_play(self, card1, card2):  # pragma: no cover
        pass

    @abstractmethod
    def start_game(self):  # pragma: no cover
        pass

    @abstractmethod
    def end_game(self):  # pragma: no cover
        pass

    def discard_cards(self, *cards):
        self.discard_pile.add(*cards, to_top=True)
        return self

    def get_discard_pile(self):
        return self.discard_pile

    def get_top_card(self):
        return self.discard_pile.get_top_card()

    def reshuffle_discard_pile(self):
        if len(self.draw_pile) == 0:
            self.draw_pile.add(*self.discard_pile.get_cards())
            self.discard_pile.clear()
            self.draw_pile.shuffle()
        return self

    def draw_cards(self, player=None, n=1):
        if len(self.draw_pile) >= n:
            drawn = self.draw_pile.draw(n)
            if not isinstance(drawn, list):
                drawn = [drawn]
            player.add_cards(*drawn)
            return drawn
        if len(self.draw_pile) == 0:
            return self.reshuffle_discard_pile().draw_cards(player, n)
        raise ValueError("Not enough cards in the draw pile.")

    def deal_initial_cards(self, *players):
        players_to_deal = players or self.players
        for player in players_to_deal:
            cards_needed = max(0, self.hand_size - len(player.hand))
            if cards_needed > 0:
                player.add_cards(*self.draw_pile.draw(cards_needed))
        return self

    def add_players(self, *players):
        self.players.extend(players)
        return self

    def remove_players(self, *players):
        for player in players:
            self.players.remove(player)
        return self

    def deal(self, num_cards=1, *players):
        players = players or self.players
        for player in players:
            player.add_cards(*self.draw_pile.draw(num_cards))
        return self

    def play_card(self, card, player=None, *args):
        top_card = self.discard_pile.get_top_card()

        if top_card is None:
            return False

        if self.check_valid_play(card, top_card):
            if not player:
                player = self.get_current_player()

            self.discard_cards(card)
            player.play_cards(card)

            card.effect(self, player, *args)

            return True
        return False

    def shuffle(self):
        self.draw_pile.shuffle()
        return self

    def get_trump(self):
        return self.trump

    def set_trump(self, suit):
        if suit not in self._card_type.SUITS:
            raise ValueError(f"Invalid suit for trump: {suit}")
        self.trump = suit
        return self

    def apply_trump(self):
        for card in self.draw_pile:
            if card.get_suit() == self.trump:
                card.set_trump(True)
            else:
                card.set_trump(False)
        return self

    def change_trump(self, suit):
        if suit not in self._card_type.SUITS:
            raise ValueError(f"Invalid suit for trump: {suit}")
        self.set_trump(suit)
        self.apply_trump()
        return self

    def get_current_player(self):
        return self.players[self.current_player_index]

    def set_current_player(self, player):
        if isinstance(player, int):
            if player < 0 or player >= len(self.players):
                raise ValueError("Invalid player index")
            self.current_player_index = player
        elif isinstance(player, GenericPlayer):
            self.current_player_index = self.players.index(player)
        else:
            raise TypeError(
                "Invalid player type: must be an integer or a Player object")
        return self

    def get_players(self):
        return self.players

    def next_player(self):
        self.reshuffle_discard_pile()

        new_index = (self.current_player_index + self.direction) % len(
            self.players)
        self.set_current_player(new_index)
        return self

    def reverse_direction(self):
        self.direction *= -1
        return self

    def get_draw_pile(self):
        return self.draw_pile

    def set_draw_pile(self, deck):
        self.draw_pile = deck
        return self

    def __str__(self):
        return f"Game of {len(self.players)} players"

    def __repr__(self):
        return (f"{self.__class__.__name__}("
                f"card_type={self._card_type!r}, "
                f"deck_type={self._deck_type!r}, "
                f"draw_pile={self.draw_pile!r}, "
                f"discard_pile={self.discard_pile!r}, "
                f"trump={self.trump!r}, "
                f"hand_size={self.hand_size!r}, "
                f"starting_player_index={self.current_player_index!r}, "
                f"*{self.players!r}")
