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


from app.pycardgame import *

# Set the rank and suit names
Card.RANKS = ["7", "8", "9", "10", "Esquire", "Knight", "King", "Ace"]
Card.SUITS = ["Cups", "Golds", "Clubs", "Swords"]

card1 = Card(2, 2)
card2 = Card("Ace", "Golds")

print(f"card1 = {repr(card1)}")
print(f"card1 = {repr(card2)}\n")

print(f"{card1 < card2 = }")
print(f"{card1 > card2 = }")
print(f"{card1 == card2 = }")
print(f"card1 != card2 = {card1 != card2}")
print(f"{card1 <= card2 = }")
print(f"{card1 >= card2 = }", end="\n\n")

deck = PokerDeck().add(Card(None, None, joker=True),
                       Card(None, None, joker=True)).shuffle()
print(deck)  # Same effect as print(str(deck))
print(repr(deck))  # Will print the object representation! (evaluable)

for card in deck:
    # Make all Golds trumps
    if card.get_suit(as_index=True) == 1:
        card.trump = True
    print("-", card)
print()

deck.sort()
for card in deck:
    print("-", card)
print()

# Create a few players
player1 = Player("Alice")
player2 = Player("Bob")
player3 = Player("Charlie")

# Create a new game with the players
game = Game(deck.shuffle(), "Cups", 4, player1, player2, player3)
print(game)
print(repr(game), end="\n\n")

print(str(game.deal().get_current_player()) + ":")
[print(c) for c in game.get_current_player().get_hand()]
print()

game.play(game.get_current_player(), game.get_current_player().get_hand()[0])
print(str(game.get_current_player()) + ":")
[print(c) for c in game.get_current_player().get_hand()]
print("Discard Pile:", game.discard_pile)
