import random

from app.pycardgame import UnoGame, UnoPlayer


def move(game: UnoGame, *, color=None, uno=False):
    current = game.get_current_player()

    for card in current:
        if game.check_valid_play(card):
            if card.is_wild():
                game.play_card(card, current, color)
                print(f"{current.name} plays {card}",
                      f"and changes color to {color} ({len(current)})")
            else:
                game.play_card(card)
                print(f"{current.name} plays {card} ({len(current)})")
            break
    else:
        cards = game.draw_instead_of_play(current)
        print(f"{current.name} has to draw {len(cards)} card"
              f"{'s' if len(cards) > 1 else ''}: {', '.join(map(str, cards))}",
              f"({len(current)})")
        if len(cards) == 1 and game.check_valid_play(cards[0]):
            print(f"{current.name} throws {cards[0]}")
            game.play_card(cards[0], current, color)

    if len(current) == 1 and not uno:
        print(f">>> {current.name} forgot to call UNO!")
        drawn = game.draw_cards(current)
        print(f"{current.name} draws {len(drawn)} card"
              f"{'s' if len(drawn) > 1 else ''}:",
              f"{', '.join(map(str, drawn))}",
              f"({len(current)})")
    elif len(current) == 1 and uno:
        print(f">>> {current.name} called UNO!")

    if (winner := game.determine_winner()) is not None:
        print(f"========= {winner.name} wins the game! =========")
        game.end_game()
        return

    game.next_player()


def main():
    random.seed(42)  # for reproducibility

    player1 = UnoPlayer("Alice")
    player2 = UnoPlayer("Bob")
    player3 = UnoPlayer("Charlie")
    player4 = UnoPlayer("Diana")

    game = UnoGame(player1, player2, player3, player4)
    game.start_game()  # Start the game. Top card: Green 2
    print(game, "\n")

    for player in game.players:
        print(f"{player.name} has {len(player.hand)} cards:")
        for card in sorted(player):
            print(f" - {card}")

    print("\n")

    move(game)  # Alice plays Yellow 2
    move(game)  # Bob plays Yellow 1
    move(game)  # Charlie plays Yellow 2
    move(game)  # Diana plays Yellow 6

    move(game)  # Alice plays Yellow 8
    move(game, color="Green")  # Bob plays Wild Draw Four and calls Green
    # Charlie has to draw 4 cards
    move(game)  # Diana plays Green Draw Two

    move(game)  # Alice has to draw 2 cards: Blue 9, Blue 8
    move(game)  # Bob plays Green 7
    move(game)  # Charlie plays Green 9
    move(game, color="Yellow")  # Diana draws 1 card: Wild and immediately plays
    # it and calls Yellow

    move(game, color="Red")  # Alice plays Wild and calls Red
    move(game)  # Bob plays Red Skip
    # Charlie has to skip
    move(game)  # Diana plays Red 8

    move(game)  # Alice plays Red 9
    move(game)  # Bob plays Red Skip
    # Charlie has to skip
    move(game)  # Diana draws 1 card: Blue 5

    move(game)  # Alice plays Red 1
    move(game)  # Bob draws 1 card: Red 6 and immediately plays it
    move(game)  # Charlie plays Blue 6
    move(game)  # Diana plays Blue 4

    move(game)  # Alice plays Blue 9
    move(game)  # Bob draws 1 card: Blue 3 and immediately plays it
    move(game)  # Charlie plays Yellow 3
    move(game)  # Diana plays Yellow 4

    move(game)  # Alice plays Yellow 5
    move(game)  # Bob draws 1 card: Yellow 1 and immediately plays it
    move(game)  # Charlie plays Yellow Draw Two
    move(game)  # Diana has to draw 2 cards: Blue 2, Wild Draw Four

    move(game)  # Alice draws 1 card: Green Draw Two and immediately plays it
    move(game)  # Bob has to draw 2 cards: Yellow Skip, Blue Reverse
    move(game)  # Charlie plays Blue Draw Two
    move(game)  # Diana has to draw 2 cards: Green 8, Green 4

    move(game, uno=True)  # Alice plays Blue 8 and calls UNO
    move(game)  # Bob plays Blue Reverse
    move(game, uno=True)  # Alice draws 1 card: Blue 1 and immediately plays it
    # and calls UNO

    move(game)  # Diana plays Blue 5
    move(game)  # Charlie plays Blue 3
    move(game)  # Bob draws 1 card: Blue 2 and immediately plays it
    move(game)  # Alice draws 1 card: Red 9

    move(game)  # Diana plays Blue 2
    move(game)  # Charlie plays Blue 9
    move(game)  # Bob draws 1 card: Yellow Draw Two
    move(game, uno=True)  # Alice plays Red 9 and calls UNO

    move(game, color="Green")  # Diana plays Wild Draw Four and calls Green
    # Charlie has to draw 4 cards
    move(game)  # Bob plays Green 2
    move(game, uno=True)  # Alice draws 1 card: Green Skip and immediately plays
    # it and calls UNO

    # Diana has to skip
    move(game)  # Charlie plays Green 5
    move(game)  # Bob plays Green 4
    move(game)  # Alice draws 1 card: Blue 8

    move(game)  # Diana plays Yellow 4
    move(game)  # Charlie plays Yellow 9
    move(game, uno=True)  # Bob plays Yellow Skip and calls UNO
    # Alice has to skip

    move(game)  # Diana plays Yellow 8
    move(game)  # Charlie draws 1 card: Red 2
    move(game)  # Bob plays Yellow Draw Two and wins the game!

if __name__ == "__main__":
    main()
