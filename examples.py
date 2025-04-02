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
    UnoCard,
    UnoDeck,
    UnoGame,
    UnoPlayer,
)

# Example 1: Using Generic Card Game Classes
# ------------------------------------------

# Define custom rank and suit types
Rank = Literal["1", "2", "3"]
Suit = Literal["Red", "Green", "Blue"]


# Create a custom card class
class CustomCard(
    GenericCard[Rank, Suit],
    metaclass=CardMeta,
    rank_type=Rank,
    suit_type=Suit,
):
    # Customise the string representation of the card
    def __str__(self):
        return (f"{self.get_suit()} {self.get_rank()}"
                f"{' (trump)' if self.get_trump() else ''}")


# Create a custom deck class
class CustomDeck(GenericDeck[CustomCard], metaclass=DeckMeta,
                 card_type=CustomCard):
    ...


# Create a custom player class
class CustomPlayer(GenericPlayer[CustomCard]):
    ...


# Create a custom game class
class CustomGame(GenericGame[CustomCard]):
    def __init__(self, *players, deck=None, discard_pile=None, trump=None, hand_size=4,
                 starting_player_index=0):
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
deck.add(card1, card2, card3)
print(f"\nCreated {deck}. Contents:")
[print(f"- {card}") for card in deck]

# Create players
player1 = CustomPlayer("Alice")
player2 = CustomPlayer("Bob")

# Create a game
game = CustomGame(player1, player2, deck=deck.shuffle(), trump="Red",
                  hand_size=3)
print(f"\nGame created: {game}")

# Deal cards and demonstrate gameplay
game.deal_initial_cards()
print("\nAfter dealing first round:")
for player in game.get_players():
    print(f"{player.name}'s hand: {[str(card) for card in player.get_hand()]}")

# Example 2: Using UNO Game Classes
# ---------------------------------

print("\n\nExample 2: UNO")
print("-" * 14)

# Create UNO game with players
player1 = UnoPlayer("Alice")
player2 = UnoPlayer("Bob")
player3 = UnoPlayer("Charlie")

# Create a game instance
game = UnoGame(player1, player2, player3)
game.start_game()
print("\nGame started with players:")
for player in game.get_players():
    print(f"- {player.name} with {len(player.get_hand())} cards")
print(f"Top card on discard pile: {game.discard_pile.get_top_card()}")
print(f"Current player: {game.get_current_player().name}")

# Example gameplay
print("\nGameplay:")
print(f"{game.get_current_player().name} has the following cards:")
for card in sorted(game.get_current_player().get_hand()):
    print(f"- {card}")

# Check if the player can play a card
for card in game.get_current_player():
    if game.check_valid_play(card, game.discard_pile.get_top_card()):
        print(f"{game.get_current_player().name} can play {card}")
        break
else:
    print(f"{game.get_current_player().name} cannot play any cards")
    # Draw a card from the deck
    drawn_card = game.draw_card(game.get_current_player())
    if drawn_card:
        print(f"{game.get_current_player().name} drew a card: {drawn_card}")
    else:
        print("No cards left in the deck to draw.")

game.next_player()
