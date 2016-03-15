__author__ = 'runwei_zhang'

def reset_game():
    """Puts all of the pieces back"""

    global game_board, turn,selected_pos
    close_menu(win_menu)
    # win_menu.event_off(5)
    # win_menu.event_off(6)
    turn = 0
    for i in range(64):
        game_board[i] = None
    selected_pos = []

def mark_piece(c):
    global game_board, turn,selected_pos
    if turn ==1:
        game_board[c] = 'P1'
    else:
        game_board[c] = 'P2'
    selected_pos.append(c)


def check_winner():
    #Returns 1 if the player with the current turn to move is the winner
    if len(selected_pos) != 5:
        return 0
    return 1


def reset_game():
    """Puts all of the pieces back"""

    global game_board, turn,selected_pos
    close_menu(win_menu)
    # win_menu.event_off(5)
    # win_menu.event_off(6)
    turn = 0
    for i in range(64):
        game_board[i] = None
    selected_pos = []

def mark_piece(c):
    global game_board, turn,selected_pos
    if turn ==1:
        game_board[c] = 'P1'
    else:
        game_board[c] = 'P2'
    selected_pos.append(c)


def check_winner():
    #Returns 1 if the player with the current turn to move is the winner
    if len(selected_pos) != 5:
        return 0
    return 1