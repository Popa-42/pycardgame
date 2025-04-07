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
import random
from typing import Literal, Optional

from app.pycardgame import (
    CardMeta,
    DeckMeta,
    GenericCard,
    GenericDeck,
    GenericGame,
    GenericPlayer,
    UnoGame,
    UnoPlayer,
)

from pycardgame import UnoCard

# Example 1: Using Generic Card Game Classes
# ------------------------------------------

# Define custom rank and suit types
Rank = Literal["1", "2", "3", "4", "5", "6", "7", "8", "9", "10"]
Suit = Literal["Red", "Yellow", "Green", "Blue"]


# Create a custom card class
class CustomCard(
    GenericCard[Rank, Suit],
    metaclass=CardMeta,
    rank_type=Rank,
    suit_type=Suit
):
    def effect(self, game, player, *args):
        """Custom card effect implementation"""
        pass


# Create a custom deck class
class CustomDeck(
    GenericDeck[CustomCard],
    metaclass=DeckMeta,
    card_type=CustomCard
):
    pass


# Create a custom player class
class CustomPlayer(GenericPlayer[CustomCard]):
    pass


# Create a custom game class
class CustomGame(GenericGame[CustomCard]):
    def __init__(self, *players, draw_pile=None, discard_pile=None, trump=None,
                 hand_size=4, starting_player_index=0, do_not_shuffle=False):
        super().__init__(CustomCard, CustomDeck, draw_pile, discard_pile, trump,
                         hand_size, starting_player_index, do_not_shuffle,
                         *players)

    def check_valid_play(self, card1: CustomCard,
                         card2: Optional[CustomCard]) -> bool:
        """Define game-specific rules for valid card plays"""
        if card2 is None:
            return True
        return card1.suit == card2.suit or card1.rank == card2.rank

    def start_game(self):
        """Initialize the game state"""
        self.deal_initial_cards()

    def end_game(self):
        """Clean up game state"""
        pass


# Example usage of the custom game
def play_custom_game():
    # Create players
    player1 = CustomPlayer("Alice")
    player2 = CustomPlayer("Bob")

    # Create and initialize the game
    game = CustomGame(
        player1, player2,
        hand_size=3,
        trump="Red",
        starting_player_index=0
    )

    # Start the game
    game.start_game()
    print(f"Starting custom game with trump suit: {game.trump!r}")

    # Example of playing a card
    if game.check_valid_play(player1.hand[0], game.get_top_card()):
        played = player1.hand[0]
        game.play_card(player1.hand[0], player1)
        print(f"{player1.name} played {played}")
    game.next_player()

    # Example of drawing cards
    cards = game.draw_cards(n=2)
    print(f"{game.get_current_player().name} drew 2 cards:",
          f"{', '.join(str(card) for card in cards)}")

    # Example of changing trump suit
    game.change_trump("Green")
    print(f"Trump suit changed to {game.trump!r}")


# Example 2: Using UNO Implementation
# -----------------------------------

def play_uno_game():
    """A rudimentary UNO game"""

    random.seed(42)  # For reproducibility

    # Create UNO players
    player1 = UnoPlayer("Alice")
    player2 = UnoPlayer("Bob")
    player3 = UnoPlayer("Charlie")
    player4 = UnoPlayer("Diana")

    # Create and initialize UNO game
    game = UnoGame(player1, player2, player3, player4)

    def play_card(played_card: UnoCard):
        # Check if the card is a wild card
        if played_card.is_wild():
            # Change the color to the one that occurs most in the hand
            color_count = {c.suit: 0 for c in current_player}
            for c in current_player:
                color_count[c.suit] += 1
            new_color = max(color_count, key=color_count.get)
            # Play the card and change the color
            game.play_card(played_card, current_player, new_color)
            print(f"{current_player.name} plays {played_card} and changes "
                  f"color to {UnoCard.SUITS[new_color]}")
        else:
            # Play the card normally
            game.play_card(played_card, current_player)
            print(f"{current_player.name} plays {played_card}")

    # Start the game
    game.start_game()
    print(f"Starting UNO game with {len(game.players)} players.",
          f"\nTop card: {game.get_top_card()}\n")

    # Main game loop
    while game.determine_winner() is None:
        current_player = game.get_current_player()

        # Check if the player has a valid card to play
        for card in current_player:
            if game.check_valid_play(card):
                play_card(card)
                break
        # If no valid card is found, draw a card
        else:
            cards = game.draw_instead_of_play(current_player)
            print(f"{current_player.name} draws {len(cards)} cards:",
                  f"{', '.join(str(card) for card in cards)}")
            # If only one card is drawn and it's valid, immediately play it
            if len(cards) == 1 and game.check_valid_play(cards[0]):
                print(f"{current_player.name} throws {cards[0]} after drawing:")
                play_card(cards[0])

        game.next_player()

    print(f"\n{game.determine_winner().name} wins!")


# Example 3: Creating a Custom Card Game with Special Effects
# -----------------------------------------------------------

class SpecialCard(
    GenericCard[Rank, Suit],
    metaclass=CardMeta,
    rank_type=Rank,
    suit_type=Suit
):
    def __init__(self, rank: Rank, suit: Suit):
        super().__init__(rank, suit)  # type: ignore

    @property
    def value(self) -> int:
        return int(self.rank + 1)

    @value.setter
    def value(self, value: int):
        if 1 <= value <= 10:
            self.rank = value - 1
        else:
            raise ValueError(f"{value} is not between 1 and 10")

    def effect(self, game, player, *args):
        """Special card effect that doubles the next card's value"""
        if args and isinstance(args[0], SpecialCard):
            args[0].value *= 2
            return True
        return False


class SpecialDeck(
    GenericDeck[SpecialCard],
    metaclass=DeckMeta,
    card_type=SpecialCard
):
    pass


class SpecialPlayer(GenericPlayer[SpecialCard]):
    def __init__(self, name: str, hand=None):
        super().__init__(name, hand)
        self.score = 0

    def calculate_score(self) -> int:
        """Calculate player's score based on card values"""
        return sum(card.value for card in self.hand)


class SpecialGame(GenericGame[SpecialCard]):
    def __init__(self, *players, draw_pile=None, discard_pile=None, trump=None,
                 hand_size=4, starting_player_index=0, do_not_shuffle=False):
        super().__init__(SpecialCard, SpecialDeck, draw_pile, discard_pile,
                         trump,
                         hand_size, starting_player_index, do_not_shuffle,
                         *players)

    def check_valid_play(self, card1: SpecialCard,
                         card2: Optional[SpecialCard]) -> bool:
        """Special game rules for valid plays"""
        if card2 is None:
            return True
        return (card1.suit == card2.suit or
                card1.rank == card2.rank or
                isinstance(card1, SpecialCard))

    def start_game(self):
        """Initialize the special game"""
        self.deal_initial_cards()
        self.current_player_index = 0

    def end_game(self):
        """End the special game and calculate scores"""
        for player in self.players:
            player.score = player.get_score()


def play_special_game():
    # Create players
    player1 = SpecialPlayer("Alice")
    player2 = SpecialPlayer("Bob")

    # Create and initialize the game
    game = SpecialGame(
        player1, player2,
        hand_size=5,
        trump="Red"
    )

    # Start the game
    game.start_game()

    # Example of playing a special card
    special_card = next(
        card for card in player1.hand if isinstance(card, SpecialCard))
    if game.play_card(special_card, player1):
        print(f"{player1.name} played a special card")

    # Example of using the special effect
    next_card = player2.hand[0]
    if special_card.effect(game, player1, next_card):
        print(f"Next card's value was doubled to {next_card.value}")

    # End the game and show scores
    game.end_game()
    for player in game.players:
        print(f"{player.name}'s score: {player.score}")


if __name__ == "__main__":
    # Run the examples
    print("Playing custom game example...")
    play_custom_game()

    print("\nPlaying UNO game example...")
    play_uno_game()

    print("\nPlaying special game example...")
    play_special_game()
