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

card1 = Card(2, 1)
card2 = Card("Ace", "Hearts")

print(card1)  # Output: 3 of Diamonds
print(card2)  # Output: Ace of Hearts
```

#### Class methods

- `get_suit(as_index=False)`: Returns the suit of the card. If `as_index` is `True`, returns the index of the suit.
- `get_rank(as_index=False)`: Returns the rank of the card. If `as_index` is `True`, returns the index of the rank.
- Comparison operators: `<`, `<=`, `==`, `!=`, `>=`, `>`. Cards are compared first based on their suit and then on their rank.

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
from pycardgame import Card, Deck

# Create cards
card1 = Card(2, 1)
card2 = Card("Ace", "Hearts")

# Compare cards
print(card1 < card2)  # Output: True or False

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
