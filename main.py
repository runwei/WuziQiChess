import pygame._view
from pygame import *
from random import *
from sets import Set
import os
import sys
import platform
sys.path.append('modules')  # Access my module folder for importing
from menu import *
init()

screen = display.set_mode((600,600))

def reset_game():
    """Puts all of the pieces back"""

    global game_board, turn,selected_pos
    close_menu(win_menu)
    turn = 2
    for i in range(64):
        game_board[i] = None
    selected_pos = []
    whiteset,blackset = set(),set()

def mark_piece(c):
    global game_board, turn,selected_pos
    if turn ==1:
        game_board[c] = 'P1'
        whiteset.add(c)
    else:
        game_board[c] = 'P2'
        blackset.add(c)
    selected_pos.append(c)

def check_validstone(x,y):
    if x<8 and x>=0 and y<8 and y>=0:
        return True
    else:
        return False

def check_winner(c):
    #Returns 1 if the player with the current turn to move is the winner
    if len(selected_pos) ==64:
        return 1
    else:
        curset = blackset if turn==2 else whiteset
        x,y = c//8, c%8
        exl =[0,0,0,0,0,0,0,0] #r,l,d,u,dr,ul,dl,ur
        dirs = [[0,1],[0,-1],[1,0],[-1,0],[1,1],[-1,-1],[1,-1],[-1,1]]
        for i in xrange(len(dirs)):
            dir = dirs[i]
            tmpx,tmpy = x,y
            while check_validstone(tmpx+dir[0],tmpy+dir[1]) and (tmpx+dir[0])*8+tmpy+dir[1] in curset:
                tmpx,tmpy=tmpx+dir[0],tmpy+dir[1]
                exl[i]+=1
        d,u,r,l,rd,lu,ru,ld = exl[0],exl[1],exl[2],exl[3],exl[4],exl[5],exl[6],exl[7]
        print turn,x,y
        print curset
        print exl
        if l+r>=4 or d+u>=4 or rd+lu>=4 or ru+ld>=4:
            return 1
        else:
            return 0



""" Game variables """
turn = 2
moves = [i for i in range(64)]
selected_pos = []
game_board = [None for i in range(64)]
en_passent = None
blackset,whiteset = set(),set()
""" Image Loading """
pawn1 = image.load("images/wpawn.png").convert_alpha()
pawn2 = image.load("images/bpawn.png").convert_alpha()


""" Creation of game board """
# Notes:
# Event 5 represents a selected piece
# Event 6 represents a possible move for a piece
# Event 7 represents a possible capture of an enemy piece

font1 = font.Font('fonts/Alido.otf',18)
font2 = font.Font('fonts/LCALLIG.ttf',36)

win_bg = Surface((250,90))
win_bg.fill((0,0,0))
draw.rect(win_bg,(255,255,255),(5,5,240,80))

layer_black = Surface((50,50))
layer_black.fill((128,128,128))
layer_hovered = Surface((50,50))
layer_hovered.fill((0,0,255))
layer_is_move = Surface((50,50),SRCALPHA)
layer_is_move.fill((0,0,255,85))

new_bg = Surface((100,20))
new_bg.fill((255,0,0))
new_bg2 = Surface((100,20))
new_bg2.fill((0,0,255))


# In-game GUI
game_menu = make_menu((0,0,800,800),'game',0)
open_menu(game_menu)

board_buttons = [Button((100+(i%8)*50,450-(i//8)*50,50,50),i,(0,)) for i in range(64)]

for i in range(64):
    if (i+i//8)%2 == 0:
        board_buttons[i].add_layer(layer_black,(0,0),(0,))

new_game = Button((2,2,50,20),'new',(0,))
new_game.add_layer(new_bg,(0,0),(2,))
new_game.add_text("Reset",font1,(0,0,0),(25,10),1,0,(0,))

quit_button = Button((548,2,50,20),'quit',(0,))
quit_button.add_layer(new_bg,(0,0),(2,))
quit_button.add_text("Quit",font1,(0,0,0),(25,10),1,0,(0,))

add_layer_multi(layer_hovered,(0,0),(2,-5,-6,-7),board_buttons)
add_layer_multi(layer_is_move,(0,0),(-5,6,-7),board_buttons)

add_objects(game_menu,board_buttons)
add_objects(game_menu,(new_game,quit_button))

# Win menu
win_menu = make_menu((175,270,250,90),'win',1)
win_menu.add_layer(win_bg,(0,0),(5,6))
win_menu.add_text("White wins!",font2,(0,0,0),(125,30),1,0,(5,))
win_menu.add_text("Black wins!",font2,(0,0,0),(125,30),1,0,(6,))
quit2 = Button((180,60,50,20),'quit',(0,))
quit2.add_layer(new_bg,(0,0),(2,))
quit2.add_layer(new_bg2,(0,0),(0,-2))
quit2.add_text("Quit",font1,(255,255,255),(25,10),1,0,(0,))
win_menu.add_object(quit2)

reset_game()
""" Main Loop """
# Notes:
# My loops run in three main steps:
#   1. Get inputs for each menu along with general inputs
#   2. Handle inputs for each menu and update all running systems
#   3. Draw all of the objects to the screen for each menu
#
# Using my menuing system I'm able to easily organize every GUI including the
# main game itself into these three steps.

running = 1
while running:
    """ STEP 1: Get inputs """
    chars = ''
    for evnt in event.get():
        if evnt.type == QUIT:
            running = 0
        elif evnt.type == KEYDOWN:
            if evnt.key == K_ESCAPE:
                running = 0
            else:
                chars += evnt.unicode

    lc,rc = mouse.get_pressed()[0:2]
    mx,my = mouse.get_pos()
    """ STEP 2: Handle inputs / update menus """

    update_menus(mx,my,lc,chars)

    if is_menu_open(game_menu):
        # Handle the game board and game menu
        for c in game_menu.get_pressed():
            if c == 'new':      # Reset game button
                reset_game()
            elif c == 'quit':   # Exit game button
                running = 0
            else:
                if c not in selected_pos: # If the chosen square is an option
                    flag = check_winner(c)
                    mark_piece(c)
                    turn = 1+turn%2
                    if flag:
                        open_menu(win_menu)
                        win_menu.event_on(5+turn%2)

    if is_menu_open(win_menu):
        for i in win_menu.get_pressed():
            if i == 'quit':
                running = 0
            elif i == 'new':
                reset_game()

    """ STEP 3: Draw menus """
    update_menu_images()

    if is_menu_open(game_menu):
        # Draw the pieces on the game board
        for i in range(64):
            if game_board[i] == 'P1':
                game_menu.blit(pawn1,(100+(i%8)*50,450-(i//8)*50))
            if game_board[i] == 'P2':
                game_menu.blit(pawn2,(100+(i%8)*50,450-(i//8)*50))

    screen.fill((255,255,255))
    draw.rect(screen,(0,0,0),(50,50,500,500))
    draw.rect(screen,(255,255,255),(100,100,400,400))
    draw_menus(screen)

    display.flip()
    time.wait(10)

quit()