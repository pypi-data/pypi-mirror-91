from .game import Game

KEYBINDINGS = {
    "w": 0,
    "a": 3,
    "s": 2,
    "d": 1,
}


def main(game: Game):
    game.set_apple()
    while True:
        game.draw_field()
        while (go := input("> ").lower()) not in ["w", "a", "s", "d"]:
            print(":(")

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


if __name__ == '__main__':
    size = input("Game size: ")
    try:
        size = int(size)
    except ValueError:
        size = 5
    g = Game(size)
    main(g)
