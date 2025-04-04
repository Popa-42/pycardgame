import random
from app.pycardgame import UnoGame, UnoPlayer


def move(game: UnoGame, *args):
    current: UnoPlayer = game.get_current_player()
    current.reset_uno()

    for card in current.hand:
        if game.check_valid_play(card, game.get_top_card()):
            if card.is_wild():
                color = args[0] if args and args[0] else None
                if color is None:
                    raise ValueError("Wild card played without color.")
                game.play_card(card, current, color)
            else:
                game.play_card(card, current)
            print(f"{current.name} plays {card} ({len(current)})")
            if args and len(args) > 1 and args[1]:
                if len(current) == 1:
                    print(f">>> {current.name} calls UNO! <<<")
                    current.call_uno()
                else:
                    raise ValueError("Cannot call UNO! with more than 1 card")
            break
    else:
        card = game.draw_cards(current)[0]
        print(f"{current.name} cannot play any card and draws {card} "
              f"({len(current)})")


    if len(current) == 1 and not current.uno:
        print(f">>> {current.name} forgot to call UNO! <<<")
        game.draw_cards(current)

    if (winner := game.determine_winner()) is not None:
        print(f"{winner.name} wins the game!")
        game.end_game()

    game.next_player()


def main():
    random.seed(42)

    player1 = UnoPlayer("Alice")
    player2 = UnoPlayer("Bob")
    player3 = UnoPlayer("Charlie")
    player4 = UnoPlayer("Diana")

    game = UnoGame(player1, player2, player3, player4)
    game.start_game()  # Start the game. Top card: Yellow 2
    print(game, "\n")

    for player in game.players:
        print(f"{player.name} has {len(player.hand)} cards:")
        for card in sorted(player):
            print(f" - {card}")

    print()

    move(game)  # Alice plays Yellow 1
    move(game)  # Bob plays Red 1
    move(game)  # Charlie plays Red 9
    move(game)  # Diana plays Blue 9

    move(game)  # Alice plays Blue 2
    move(game)  # Bob plas Red 2
    move(game, "Green")  # Charlie plays Wild and chooses Green
    move(game)  # Diana draws Green 8

    move(game)  # Alice plays Green 2
    move(game)  # Bob plays Green Skip
    move(game)  # Diana plays Green 8

    move(game)  # Alice draws Red 4
    move(game)  # Bob plays Green 7
    move(game)  # Charlie plays Green 3
    move(game)  # Diana plays Yellow 3

    move(game)  # Alice plays Yellow Reverse

    move(game)  # Diana plays Blue Reverse

    move(game)  # Alice plays Blue 4
    move(game)  # Bob plays Blue 7
    move(game)  # Charlie plays Blue 6
    move(game)  # Diana plays Blue 5

    move(game)  # Alice draws Red 3
    move(game)  # Bob draws Blue 9
    move(game)  # Charlie draws Yellow 9
    move(game)  # Diana plays Blue 1

    move(game)  # Alice draws Red Skip
    move(game)  # Bob plays Blue 9
    move(game)  # Charlie plays Yellow 9
    move(game, None, True)  # Diana plays Yellow 1 and calls UNO!

    move(game)  # Alice plays Yellow 4
    move(game)  # Bob draws Green 9
    move(game)  # Charlie plays Green 4
    move(game)  # Diana draws Yellow 3

    move(game)  # Alice plays Red 4
    move(game)  # Bob draws Green 4
    move(game)  # Charlie plays Red 3 and forgets to call UNO!
    move(game, None, True)  # Diana plays Red 5 and calls UNO!

    move(game)  # Alice plays Red 4
    move(game)  # Bob plays Green 4
    move(game)  # Charlie draws Yellow 7
    move(game)  # Diana draws Yellow 2

    move(game)  # Alice draws Red 1
    move(game)  # Bob plays Green 6
    move(game)  # Charlie plays Red 6
    move(game)  # Diana draws Wild Draws Four

    move(game)  # Alice plays Red 3
    move(game)  # Bob draws Green Reverse
    move(game)  # Charlie draws Yellow 9
    move(game)  # Diana plays Yellow 3

    move(game)  # Alice draws Green 2
    move(game)  # Bob draws Blue 2
    move(game)  # Charlie plays Yellow 0
    move(game, None, True)  # Diana plays Yellow 2 and calls UNO!

    move(game)  # Alice plays Green 2
    move(game, "Blue")  # Bob plays Wild and chooses Blue
    move(game)  # Charlie draws Wild
    move(game, "Green")  # Diana plays Wild Draw Four, chooses Green and
    # wins the game


if __name__ == "__main__":
    main()
