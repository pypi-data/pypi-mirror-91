import argparse
from curses import wrapper
import curses

from .game import Game
from .tui import TUI

KEYBINDINGS = {
    "w": 0,
    "a": 3,
    "s": 2,
    "d": 1,
}


def play(game: Game):
    game.set_apple()
    first = True
    while True:
        if not first:
            print("\033[F" * (game.field_size + 4) + "\b")
        else:
            first = False
        game.draw_field()
        lines = 1
        while (go := input("> ").lower()) not in ["w", "a", "s", "d", "exit"]:
            print("\033[F" * (lines + 1) + "\b")
            print("Please type 'w', 'a', 's' or 'd'! To exit the game, type 'exit'")
            lines = 2

        print(("\033[F\b" + " " * 30) * lines)

        if go == "exit":
            print("Game aborted.")
            break

        game.orientation = KEYBINDINGS[go]

        if not game.move():
            print("You lost!")
            break

        if game.score == game.max_score:
            print("You won!")
            break

        game.max_apples = max((1, game.score // 5))
    game.end_game()
    print(f"Score: {game.score} | Highscore: {game.highscore}")


def main(stdscr):
    size = input("Game size: ")
    try:
        size = int(size)
    except ValueError:
        size = 5

    print("\033[F\033[F\b" + " " * 30 + "\b")
    g = Game(size)
    play(g)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Command line snake game')
    parser.add_argument('field_size', type=int, default=5, help='Size of your field')
    parser.add_argument('-c', '--continuous', action='store_true', help='Play this game continuously?')

    args = parser.parse_args()
    print(f"Generating field with size {args.field_size}")

    tui = wrapper(TUI, args.field_size, args.continuous)
    for msg in tui.msgs:
        print(msg)
