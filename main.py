from Ai import *
from Chess import *

# pygame UI from https://techvidvan.com/tutorials/python-game-project-tic-tac-toe/

# set configs parameters for new Gomoku game
board_size = 15
olive = (128, 128, 0)
new_game = Chess(board_size, olive)
new_game.game_opening()
#
my_ai = Ai(board_size, False)
#

# run the game loop forever
while True:
    for event in new_game.getEvent():
        new_game.draw_status()
        if event.type == QUIT:
            new_game.exit()
        elif event.type == MOUSEBUTTONDOWN:
            # the user clicked; place an X or O
            clicked = new_game.userClick()
            last = new_game.get_ticks()
            if clicked[0] == -1:
                continue
            if clicked[0] is not None and clicked[1] is not None:
                current_color = new_game.get_color()
                my_ai.place(clicked, current_color)
                if my_ai.if_win(current_color, clicked):
                    new_game.winner = 'x'
                    new_game.draw_status()
                    time.sleep(3)
                    new_game.reset_game()
                    my_ai.reset()
                    continue

                opposite_color = 1 - current_color
                suggested = my_ai.inquire(opposite_color)
                row = suggested[0]
                col = suggested[1]
                my_ai.place(suggested, opposite_color)
                now = new_game.get_ticks()
                while now < last + 600:
                    now = new_game.get_ticks()
                new_game.drawXO(row, col)
                if my_ai.if_win(opposite_color, suggested):
                    new_game.winner = 'o'
                    new_game.draw_status()
                    time.sleep(3)
                    new_game.reset_game()
                    my_ai.reset()

    new_game.CLOCK.tick(new_game.fps)
