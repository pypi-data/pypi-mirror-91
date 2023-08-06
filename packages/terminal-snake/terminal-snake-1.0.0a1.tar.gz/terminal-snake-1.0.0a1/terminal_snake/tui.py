import curses
import locale
import time
from typing import List

from .game import Game


class TUI:
    KEYBINDINGS = {
        ord("w"): 0,
        ord("a"): 3,
        ord("s"): 2,
        ord("d"): 1,
        curses.KEY_UP: 0,
        curses.KEY_RIGHT: 1,
        curses.KEY_DOWN: 2,
        curses.KEY_LEFT: 3,
    }

    def __init__(self, stdscr, field_size, continous_mode=False):
        self.mode = continous_mode

        locale.setlocale(locale.LC_ALL, '')
        self.stdscr = stdscr
        self.stdscr.border()

        self.stdscr.refresh()

        self.width = curses.COLS
        self.height = curses.LINES

        self.middle = self.middle_y, self.middle_x = (self.height // 2, self.width // 2)

        self.game = self.prepare_game(field_size)

        self.game_pos = self.game_y, self.game_x = (middle_coord - field_coord for middle_coord, field_coord in
                                                    zip(self.middle, (self.game.field_size,) * 2))

        self.game_win = self.stdscr.subwin(self.game_y, self.game_x)
        self.game_win.keypad(1)

        self.msgs = []

        instruction = "Use 'wasd' or your arrow keys to move. Quit using 'q'."
        try:
            self.stdscr.addstr(3, (self.width - len(instruction)) // 2, instruction)
        except curses.error:
            pass
        finally:
            self.stdscr.refresh()

        self.play()

    @staticmethod
    def encode(text: str):
        return text.encode("utf-8", "replace")

    def prepare_game(self, field_size):
        game = Game(field_size, score_key=f"c{field_size}" if self.mode else None)
        game.set_apple()
        return game

    def play(self):
        self.game_win.nodelay(self.mode)

        while True:
            score_text = f"Score: {self.game.score}"
            self.stdscr.addstr(2, (self.width - len(score_text)) - 2, score_text)
            self.stdscr.refresh()

            game_field = self.game.draw_field(print_=False)
            self.game_win.clear()
            for line_count, line in enumerate(game_field):
                self.game_win.addstr(line_count, 0, self.game.theme.character_separator.join(line))
            self.game_win.refresh()

            while (go := self.game_win.getch()) not in list(self.KEYBINDINGS.keys()) + [ord("q")]:
                # wrong chr -> continue if mode == True
                if self.mode:
                    go = [ord(c) for c in "wdsa"][self.game.orientation]
                    break

            if go == ord("q"):
                self.msgs.append("Game aborted.")
                break

            self.game.orientation = self.KEYBINDINGS[go]

            if not self.game.move():
                self.msgs.append("You lost!")
                break

            if self.game.score == self.game.max_score:
                self.msgs.append("You won!")
                break

            self.game.max_apples = max((1, self.game.score // 5))
            if self.mode:
                time.sleep(0.2)
        self.game.end_game()
        self.msgs.append(f"Score: {self.game.score} | Highscore: {self.game.highscore}")
