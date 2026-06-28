import curses
import random

def main(stdscr):
    curses.curs_set(0)
    h, w = stdscr.getmaxyx()

    win = curses.newwin(h, w, 0, 0)
    win.keypad(1)
    win.timeout(100)

    snk_x = w // 4
    snk_y = h // 2

    snake = [
        [snk_y, snk_x],
        [snk_y, snk_x - 1],
        [snk_y, snk_x - 2]
    ]

    food = [h // 2, w // 2]
    win.addch(food[0], food[1], '*')

    key = curses.KEY_RIGHT
    score = 0

    while True:
        next_key = win.getch()
        key = key if next_key == -1 else next_key

        new_head = snake[0].copy()

        if key == curses.KEY_DOWN:
            new_head[0] += 1
        elif key == curses.KEY_UP:
            new_head[0] -= 1
        elif key == curses.KEY_LEFT:
            new_head[1] -= 1
        elif key == curses.KEY_RIGHT:
            new_head[1] += 1

        snake.insert(0, new_head)

        if snake[0] == food:
            score += 1
            food = [random.randint(1, h - 2), random.randint(1, w - 2)]
        else:
            tail = snake.pop()
            win.addch(tail[0], tail[1], ' ')

        if (snake[0][0] in [0, h - 1] or
            snake[0][1] in [0, w - 1] or
            snake[0] in snake[1:]):
            break

        win.clear()
        win.addstr(0, 2, f"Score: {score}")
        win.addch(food[0], food[1], '*')

        for y, x in snake:
            win.addch(y, x, '#')

    curses.endwin()

curses.wrapper(main)
