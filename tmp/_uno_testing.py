import random

from app.pycardgame import UnoDeck, UnoGame, UnoPlayer


def move(game: UnoGame, *args):
    current: UnoPlayer = game.get_current_player()
    current.reset_uno()

    for card in current.hand:
        top_card = game.get_top_card()
        if top_card is None:
            raise ValueError("No top card found.")
        if game.check_valid_play(card, top_card):
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
        card = game.draw_cards(current)[0]  # type: ignore
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
    game.start_game()  # Start the game. Top card: Green 2
    print(game, "\n")

    for player in game.players:
        print(f"{player.name} has {len(player.hand)} cards:")
        for card in sorted(player):
            print(f" - {card}")

    move(game)  # Alice plays Yellow 2
    move(game)  # Bob plays Yellow 1
    move(game)  # Charlie plays Yellow 2
    move(game)  # Diana plays Yellow 6

    move(game)  # Alice plays Yellow 8
    move(game, "Green")  # Bob plays Wild Draw Four and calls Green
    # Charlie has to draw 4 cards
    move(game)  # Diana draws Blue 9

    move(game, "Red")  # Alice plays Wild and calls Red
    move(game)  # Bob plays Red Skip
    # Charlie has to skip his turn
    move(game)  # Diana plays Red 8

    move(game)  # Alice plays Red 9
    move(game)  # Bob draws Blue 8
    move(game)  # Charlie plays Red Draw Two
    move(game)  # Diana plays Yellow Draw Two


if __name__ == "__main__":
    main()
