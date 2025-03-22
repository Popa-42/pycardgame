# PyCardGame

A base library for creating card games in Python

<!--
Copyright (C) 2025  Popa-42
This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.
This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.
You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
--->

## Installation

```bash
pip install -i https://test.pypi.org/simple/ pycardgame
```

## Usage

### `Card` class

The `Card` class represents a single playing card. It includes attributes for rank, suit, and whether the card is a
trump card.

**Example:**

```python
from pycardgame import Card

print(Card.suit_names)  # Output: ["Clubs", "Diamonds", "Hearts", "Spades"]
print(Card.rank_names)  # Output: ["2", "3", "4", "5", "6", "7", "8", "9", "10", "Jack", "Queen", "King", "Ace"]

card1 = Card(12, 1)
card2 = Card("4", "Hearts")
card3 = Card(9, "Hearts")
card4 = Card("Jack", 2)

print(card1)  # Output: Ace of Diamonds
print(card2)  # Output: 4 of Hearts
print(card3)  # Output: Jack of Hearts
print(card4)  # Output: Jack of Hearts

# Compare cards
print(card1 < card2)  # Output: True => Diamonds < Hearts
print(card2 >= card3)  # Output: False => 4 < Jack
print(card3 == card4)  # Output: True => Jack of Hearts == Jack of Hearts
```

**Example:**

```python
from pycardgame import Deck

deck = Deck().shuffle()
print(deck)  # Output: Deck of 52 cards

card = deck.draw()
print(card)  # Output: (random card from the deck)
```

### `Deck` class

The `Deck` class represents a collection of Card objects. It includes methods for shuffling, drawing, adding, and
sorting cards.

**Example:**

```python
from pycardgame import Deck

deck = Deck().shuffle()
print(deck)  # Output: Deck of 52 cards

card = deck.draw()
print(card)  # Output: (random card from the deck)
```

#### Class methods

- `reset()`: Resets the deck to its original state.
- `count()`: Counts the occurrences of a specific card, rank, or suit in the deck.
- `sort(by="suit")`: Sorts the deck by suit or rank.
- `shuffle()`: Shuffles the deck.
- `draw(n=1)`: Draws `n` cards from the deck.
- `add(card)`: Adds a card to the deck.
- `get_index(card)`: Returns the indices of all occurrences of a card in the deck.
- `get_cards()`: Returns a list of all cards in the deck.

**Example:**

```python
from pycardgame import Deck

# Create and shuffle deck
deck = Deck().shuffle()
print(deck)

# Draw a card
drawn_card = deck.draw()
print(drawn_card)

# Sort the deck
deck.sort()
for card in deck:
    print(card)
```

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## License

This project is licensed under the GNU General Public License v3.0 - see the [LICENSE](LICENSE) file for details.
