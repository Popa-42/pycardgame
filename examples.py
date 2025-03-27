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

from typing import Literal
from app.pycardgame import (
    CardMeta,
    DeckMeta,
    GenericCard,
    GenericDeck,
    GenericGame,
    GenericPlayer,
    PokerCard,
    PokerDeck,
    PokerGame,
    PokerPlayer,
)


# Example 1: Using Generic Card Game Classes
# ------------------------------------------

# Define custom rank and suit types
Rank = Literal["1", "2", "3", "4", "5"]
Suit = Literal["Red", "Blue", "Green"]

# Create a custom card class
class CustomCard(
    GenericCard[Rank, Suit],
    metaclass=CardMeta,
    rank_type=Rank,
    suit_type=Suit,
): ...

# Create a custom deck class
class CustomDeck(GenericDeck[CustomCard], metaclass=DeckMeta, card_type=CustomCard): ...

# Create a custom player class
class CustomPlayer(GenericPlayer[CustomCard]): ...

# Create a custom game class
class CustomGame(GenericGame[CustomCard]):
    def __init__(self, deck=None, discard_pile=None, trump=None, hand_size=4,
                 starting_player_index=0, *players):
        super().__init__(CustomCard, CustomDeck, deck, discard_pile, trump,
                         hand_size, starting_player_index, *players)

# Demonstrate generic card game functionality
print("Example 1: Generic Card Game")
print("-" * 28)

# Create and configure cards
card1 = CustomCard("1", "Red")
card2 = CustomCard("2", "Blue")
card3 = CustomCard("3", "Green")

print(f"Created cards: {card1}, {card2}, {card3}")

# Create a deck and add cards
deck = CustomDeck()
deck.add(card1, card2, card3).shuffle()
print(f"\nDeck contents: {deck}")

# Create players
player1 = CustomPlayer("Alice")
player2 = CustomPlayer("Bob")

# Create a game
game = CustomGame(deck, None, "Red", 2, 0, player1, player2)
print(f"\nGame created: {game}")

# Deal cards and demonstrate gameplay
game.deal()
print("\nAfter dealing:")
for player in game.get_players():
    print(f"{player.name}'s hand: {[str(card) for card in player.get_hand()]}")

# Example 2: Using Poker Card Game Classes
# ----------------------------------------

print("\n\nExample 2: Poker Card Game")
print("-" * 24)

# Create a poker deck
poker_deck = PokerDeck()
print(f"Created poker deck: {poker_deck}")

# Create poker players
poker_player1 = PokerPlayer("Charlie")
poker_player2 = PokerPlayer("David")

# Create a poker game
poker_game = PokerGame(0, poker_player1, poker_player2)
print(f"\nCreated poker game: {poker_game}")

# Deal cards and demonstrate gameplay
poker_game.deal()
print("\nAfter dealing:")
for player in poker_game.get_players():
    print(f"{player.name}'s hand: {[str(card) for card in player.get_hand()]}")

# Demonstrate card comparison
ace_hearts = PokerCard("Ace", "Hearts")
king_spades = PokerCard("King", "Spades")

print("\nCard comparison:")
print(f"{ace_hearts} > {king_spades}: {ace_hearts > king_spades}")
print(f"{ace_hearts} == {king_spades}: {ace_hearts == king_spades}")

# Demonstrate deck operations
print("\nDeck operations:")
poker_deck.shuffle()
print(f"After shuffling: {poker_deck}")

drawn_cards = poker_deck.draw(3)
print(f"Drawn cards: {[str(card) for card in drawn_cards]}")
print(f"Remaining cards: {len(poker_deck)}")

# Demonstrate game operations
print("\nGame operations:")
current_player = poker_game.get_current_player()
print(f"Current player: {current_player}")

# Play a card
if current_player.get_hand():
    played_card = current_player.get_hand()[0]
    poker_game.play(current_player, played_card)
    print(f"Played card: {played_card}")
    print(f"Discard pile: {poker_game.discard_pile}")
