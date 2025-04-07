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

## Quick Start

A detailed guide on how to use the library can be found in our
[Wiki](https://github.com/Popa-42/pycardgame/wiki) section.

## Usage

PyCardGame provides both generic base classes for creating custom card games and
preset implementations for common card games.

### Generic Base Classes

The library provides generic base classes that can be used to create custom card
games:

- [`GenericCard`](https://github.com/Popa-42/pycardgame/wiki/GenericCard): Base
  class for playing cards
- [`GenericDeck`](https://github.com/Popa-42/pycardgame/wiki/GenericDeck): Base
  class for card decks
- [`GenericPlayer`](https://github.com/Popa-42/pycardgame/wiki/GenericPlayer):
  Base class for game players
- [`GenericGame`](https://github.com/Popa-42/pycardgame/wiki/GenericGame): Base
  class for card games

These classes are generic and can be used to create any type of card game. They
provide methods for managing cards, decks, players, and game logic. The generic
classes are designed to be flexible and extensible, allowing you to create
custom card games with different rules and mechanics.

For a detailed explanation of each class, please refer to our
[Wiki](https://github.com/Popa-42/pycardgame/wiki).

### Preset Implementations

The library includes preset implementations for common card games:

#### Poker

- `PokerCard`: Standard playing card implementation
- `PokerDeck`: Standard 52-card deck implementation
- `PokerPlayer`: Player implementation for poker-style games
- `PokerGame`: Game implementation for poker-style games

> [!NOTE]
> More implementation will follow.

### Examples

#### Using Preset Classes

```python
from pycardgame import PokerCard, PokerDeck, PokerPlayer, PokerGame

# Create cards
ace_hearts = PokerCard("Ace", "Hearts")
king_spades = PokerCard("King", "Spades")

# Create a deck
deck = PokerDeck().shuffle()
print(deck)  # Output: Deck of 52 cards

# Create players
player1 = PokerPlayer("Alice")
player2 = PokerPlayer("Bob")

# Create a game
game = PokerGame(0, player1, player2)
game.deal_initial_cards()

# Compare cards
print(ace_hearts > king_spades)  # Output: True (Spades > Hearts)
```

#### Creating Custom Card Games

```python
from pycardgame import GenericCard, GenericDeck, GenericPlayer, GenericGame

# Define a new type of card
class CustomCard(GenericCard):
    RANKS = ["1", "2", "3"]
    SUITS = ["Red", "Blue", "Green"]

# Use custom cards
card1 = CustomCard("1", "Red")
card2 = CustomCard("2", "Blue")


# Create a custom deck class
class CustomDeck(GenericDeck[CustomCard]):
    pass

# Create a deck and add the predefined cards from above
deck = CustomDeck()
deck.add(card1, card2)


# Create a custom player class
class CustomPlayer(GenericPlayer[CustomCard]):
    pass

# Create some new players
player1 = CustomPlayer("Alice")
player2 = CustomPlayer("Bob")


# Create a custom game class
class CustomGame(GenericGame[CustomCard]):
    def __init__(self, deck=None, discard_pile=None, trump=None, hand_size=4,
                 starting_player_index=0, *players):
        super().__init__(CustomCard, CustomDeck, deck, discard_pile, trump,
                         hand_size, starting_player_index, *players)

    def play_round(self):
        # Some custom game logic
        current = self.get_current_player()
        self.play(current, current.play_card(current.hand[0])[0])

# ...and use the newly created classes
game = CustomGame(deck.shuffle(), None, "Red", 3, 0, player1, player2)
game.deal_initial_cards()
game.play_round()
```

## Documentation

For more detailed documentation, including examples and explanations of each of
the classes, please read our [Wiki](https://github.com/Popa-42/pycardgame/wiki).

## Contributing

Pull requests are welcome. For major changes, please open an issue first to
discuss what you would like to change. Please also note that we have a
[code of conduct](CODE_OF_CONDUCT.md), please follow it in all your interactions
with the project.

## License

This project is licensed under the GNU General Public License v3.0 — see the
[LICENSE](LICENSE) file for details.
