import curses
import random
from curses import wrapper

def main(stdscr):
    # Setup
    curses.curs_set(0)
    curses.start_color()
    curses.use_default_colors()

    # Color pairs
    curses.init_pair(1, curses.COLOR_GREEN, -1)   # snake
    curses.init_pair(2, curses.COLOR_RED, -1)     # food
    curses.init_pair(3, curses.COLOR_YELLOW, -1)  # score / UI
    curses.init_pair(4, curses.COLOR_CYAN, -1)    # borders
    curses.init_pair(5, curses.COLOR_WHITE, -1)   # text

    stdscr.nodelay(True)
    stdscr.timeout(120)  # starting speed (ms)

    h, w = stdscr.getmaxyx()

    def new_game():
        # Starting position
        snk_x = w // 4
        snk_y = h // 2
        snake = [
            [snk_y, snk_x],
            [snk_y, snk_x - 1],
            [snk_y, snk_x - 2]
        ]
        direction = curses.KEY_RIGHT
        score = 0
        food = place_food(snake, h, w)
        return snake, direction, score, food

    def place_food(snake, h, w):
        while True:
            food = [random.randint(1, h - 2), random.randint(1, w - 2)]
            if food not in snake:
                return food

    def draw_border():
        # Top & bottom
        for x in range(w):
            try:
                stdscr.addch(0, x, '─', curses.color_pair(4))
                stdscr.addch(h - 1, x, '─', curses.color_pair(4))
            except curses.error:
                pass
        # Sides
        for y in range(h):
            try:
                stdscr.addch(y, 0, '│', curses.color_pair(4))
                stdscr.addch(y, w - 1, '│', curses.color_pair(4))
            except curses.error:
                pass
        # Corners
        try:
            stdscr.addch(0, 0, '┌', curses.color_pair(4))
            stdscr.addch(0, w - 1, '┐', curses.color_pair(4))
            stdscr.addch(h - 1, 0, '└', curses.color_pair(4))
            stdscr.addch(h - 1, w - 1, '┘', curses.color_pair(4))
        except curses.error:
            pass

    def show_start_screen():
        stdscr.clear()
        title = "S N A K E"
        stdscr.addstr(h // 2 - 3, w // 2 - len(title) // 2, title, curses.color_pair(3) | curses.A_BOLD)
        stdscr.addstr(h // 2 - 1, w // 2 - 12, "Arrow keys to move", curses.color_pair(5))
        stdscr.addstr(h // 2,     w // 2 - 12, "P = Pause   Q = Quit", curses.color_pair(5))
        stdscr.addstr(h // 2 + 2, w // 2 - 10, "Press any key to start", curses.color_pair(3))
        stdscr.refresh()
        stdscr.nodelay(False)
        stdscr.getch()
        stdscr.nodelay(True)

    def game_over(score):
        stdscr.nodelay(False)
        msg = f" GAME OVER  •  Score: {score} "
        stdscr.addstr(h // 2 - 1, w // 2 - len(msg) // 2, msg, curses.color_pair(2) | curses.A_BOLD)
        stdscr.addstr(h // 2 + 1, w // 2 - 14, "Press R to restart  or  Q to quit", curses.color_pair(5))
        stdscr.refresh()

        while True:
            key = stdscr.getch()
            if key in (ord('q'), ord('Q')):
                return False
            if key in (ord('r'), ord('R')):
                return True

    # ===== Main loop =====
    show_start_screen()
    snake, direction, score, food = new_game()
    paused = False

    while True:
        # Adjust speed based on score (gets faster)
        speed = max(40, 120 - (score * 4))
        stdscr.timeout(speed)

        next_key = stdscr.getch()

        # Handle special keys
        if next_key in (ord('q'), ord('Q')):
            break
        if next_key in (ord('p'), ord('P')):
            paused = not paused
            if paused:
                stdscr.addstr(0, w // 2 - 4, " PAUSED ", curses.color_pair(3) | curses.A_BOLD)
                stdscr.refresh()
            continue

        if paused:
            continue

        # Prevent 180° turns
        if next_key == curses.KEY_UP and direction != curses.KEY_DOWN:
            direction = next_key
        elif next_key == curses.KEY_DOWN and direction != curses.KEY_UP:
            direction = next_key
        elif next_key == curses.KEY_LEFT and direction != curses.KEY_RIGHT:
            direction = next_key
        elif next_key == curses.KEY_RIGHT and direction != curses.KEY_LEFT:
            direction = next_key

        # Calculate new head
        new_head = snake[0][:]
        if direction == curses.KEY_DOWN:
            new_head[0] += 1
        elif direction == curses.KEY_UP:
            new_head[0] -= 1
        elif direction == curses.KEY_LEFT:
            new_head[1] -= 1
        elif direction == curses.KEY_RIGHT:
            new_head[1] += 1

        # Collision detection
        if (new_head[0] in (0, h - 1) or
            new_head[1] in (0, w - 1) or
            new_head in snake):
            if not game_over(score):
                break
            # Restart
            snake, direction, score, food = new_game()
            paused = False
            continue

        snake.insert(0, new_head)

        # Ate food?
        if new_head == food:
            score += 1
            food = place_food(snake, h, w)
        else:
            snake.pop()

        # Drawing
        stdscr.erase()
        draw_border()

        # Score
        score_text = f" Score: {score} "
        stdscr.addstr(0, 2, score_text, curses.color_pair(3) | curses.A_BOLD)

        # Food
        try:
            stdscr.addch(food[0], food[1], '●', curses.color_pair(2) | curses.A_BOLD)
        except curses.error:
            pass

        # Snake
        for i, (y, x) in enumerate(snake):
            try:
                if i == 0:  # head
                    stdscr.addch(y, x, '█', curses.color_pair(1) | curses.A_BOLD)
                else:
                    stdscr.addch(y, x, '▓', curses.color_pair(1))
            except curses.error:
                pass

        stdscr.refresh()

if __name__ == "__main__":
    wrapper(main)