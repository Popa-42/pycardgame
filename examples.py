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

card1 = Card(2, 1)
card2 = Card("Ace", "Hearts")

print(f"card1 = {card1}")
print(f"card1 = {card2}\n")

print(f"{card1 < card2 = }")
print(f"{card1 > card2 = }")
print(f"{card1 == card2 = }")
print(f"card1 != card2 = {card1 != card2}")
print(f"{card1 <= card2 = }")
print(f"{card1 >= card2 = }\n\n")

deck = Deck().shuffle()
print(deck)  # Same effect as print(str(deck))
print(repr(deck))  # Will print the object representation! (evaluable)

for card in deck:
    # Make all Diamonds trumps
    if card.get_suit() == "Diamonds":
        card.trump = True
    print("-", card)
print()

deck.sort()
for card in deck:
    print("-", card)
