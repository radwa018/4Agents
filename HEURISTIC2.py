import numpy as np # type: ignore
import pygame # type: ignore
import sys
import math
import random

BLUE=(0,0,153)
BLACK=(0,0,0)
RED=(204,0,0)
YELLOW=(255,255,0)
ROW_COUNT=6
COLUMN_COUNT=7
WHITE=(255,255,255)
PLAYER =0
AI=1

EMPTY=0
PLAYER_PIECE=1
AI_PIECE=2

WINDOW_LENGTH=4

#creating board
def create_board():
    board = np.zeros((ROW_COUNT,COLUMN_COUNT)) #row*col matrix
    return board

def drop_piece(board,row,col,piece):
    board[row][col]=piece

def is_valid_location(board,col):
    return board[ROW_COUNT-1][col]==0

def get_next_open_row(board,col):
    for r in range(ROW_COUNT):
     if board[r][col]==0:
         return r
     
def print_board(board):
    print(np.flip(board,0)) #flip the board to show it correctly

def winning_move(board,piece):
    #check horizontal
    for c in range(COLUMN_COUNT-3):
        for r in range(ROW_COUNT):
            if (
               board[r][c] ==piece 
               and board[r][c+1] ==piece 
               and board[r][c+2]==piece 
               and board[r][c+3]==piece
            ):
              return True
    #check vertical
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT-3):
            if(
                board[r][c]==piece
                and board[r+1][c]==piece
                and board[r+2][c]==piece
                and board[r+3][c]==piece
            ):
                return True
    #check +diagonal
    for c in range(COLUMN_COUNT-3):
        for r in range(ROW_COUNT-3):
            if(
                board[r][c]==piece
                and board[r+1][c+1]==piece
                and board[r+2][c+2]==piece
                and board[r+3][c+3]==piece
            ):
                return True
    #check -diagonal
    for c in range(COLUMN_COUNT-3):
        for r in range(3,ROW_COUNT):
            if(
                board[r][c]==piece
                and board[r-1][c+1]==piece
                and board[r-2][c+2]==piece
                and board[r-3][c+3]==piece
            ):
                return True
def evaluate_window(window,piece):
        score =0
        opp_piece=PLAYER_PIECE
        if piece ==PLAYER_PIECE:
           opp_piece=AI_PIECE
    
        if window.count(piece) == 4: 
            score +=100
        elif window.count(piece)==3 and window.count(EMPTY)==1: 
            score +=10
        elif window.count(piece)==2 and window.count(EMPTY)==2: 
            score +=2
            
        if window.count(opp_piece)== 3 and window.count(EMPTY)==1:
            score -=8
        
        return score   


    #calculating the heuristic score :
def score_position(board,piece):
    score =0
    #score center coulmn:
    center_array  = [int (i) for i in list(board[:,COLUMN_COUNT//2])]
    center_count=center_array.count(piece)
    score += center_count*3
    ##score horizontal
    for r in range(ROW_COUNT):
        row_array=[int (i) for i in list(board[r,:])]
        for c in range(COLUMN_COUNT-3):
            window = row_array[c:c+WINDOW_LENGTH]
            score += evaluate_window(window,piece)
            
    #score vertical
    for c in range(COLUMN_COUNT):
        col_array=[int(i) for i in list(board[:,c])]
        for r in range(ROW_COUNT-3):
            window = col_array[r:r+WINDOW_LENGTH]
            score += evaluate_window(window,piece)
    # +diagonals
    for r in range(ROW_COUNT-3):
        for c in range(COLUMN_COUNT-3):
            window = [board[r + i][c + i]for i in range(WINDOW_LENGTH)]
            score += evaluate_window(window,piece)
    #-diagonal
    for r in range(ROW_COUNT-3):
        for c in range(COLUMN_COUNT-3):
            window =[board[r+3-i][c+i]for i in range(WINDOW_LENGTH)]
            score += evaluate_window(window,piece)
            
    return score   

def is_terminal_node(board):
    return winning_move(board,PLAYER_PIECE) or winning_move(board,AI_PIECE) or len(get_valid_locations(board))==0

def valid_moves(board):
    valid_locations = get_valid_locations(board)
    best_score = -math.inf
    best_col = random.choice(valid_locations)

    for col in valid_locations:
        row = get_next_open_row(board, col)
        b_copy = board.copy()
        drop_piece(b_copy, row, col, AI_PIECE)
        score = score_position(b_copy, AI_PIECE)

        if score > best_score:
            best_score = score
            best_col = col

    return best_col
def minimax(board, depth, maximizingPlayer):
    valid_locations = get_valid_locations(board)
    is_terminal = is_terminal_node(board)
    if depth == 0 or is_terminal:
        if is_terminal:
            if winning_move(board, AI_PIECE):
                return (None, 1e6)
            elif winning_move(board, PLAYER_PIECE):
                return (None, -1e6)
            else:
                return (None, 0)
        else:
            return (None, score_position(board, AI_PIECE))
        #prioritize moves
    column=valid_moves(board)    #integration with minimax(heuristic) 
    if maximizingPlayer:
        value = -math.inf
        column = random.choice(valid_locations)
        for col in valid_locations:
            row = get_next_open_row(board, col)
            b_copy = board.copy()
            drop_piece(b_copy, row, col, AI_PIECE)
            new_score = minimax(b_copy, depth - 1, False)[1]
            if new_score > value:
                value = new_score
                column = col #update col to the best move
        return column, value
    else:
        value = math.inf
        column = random.choice(valid_locations)
        for col in valid_locations:
            row = get_next_open_row(board, col)
            b_copy = board.copy()
            drop_piece(b_copy, row, col, PLAYER_PIECE)
            new_score = minimax(b_copy, depth - 1, True)[1]
            if new_score < value:
                value = new_score
                column = col
        return column, value

def get_valid_locations(board):
    valid_location=[]
    for col in range(COLUMN_COUNT):
        if is_valid_location(board,col):
            valid_location.append(col)
    return valid_location

def draw_board(board):
    # screen.fill(BLACK)
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT):
            pygame.draw.rect(screen,BLUE,(c*SQUARESIZE,r*SQUARESIZE+SQUARESIZE,SQUARESIZE,SQUARESIZE))
            pygame.draw.circle(screen,BLACK,(int(c*SQUARESIZE+SQUARESIZE/2),int(r*SQUARESIZE+SQUARESIZE+SQUARESIZE/2)),RADIUS)
               
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT):    
            if board[r][c]==PLAYER_PIECE:
                pygame.draw.circle(screen,RED,(int(c*SQUARESIZE+SQUARESIZE/2),height-int(r*SQUARESIZE+SQUARESIZE/2)),RADIUS)
            elif board[r][c]==AI_PIECE:
                pygame.draw.circle(screen,YELLOW,(int(c*SQUARESIZE+SQUARESIZE/2),height-int(r*SQUARESIZE+SQUARESIZE/2)),RADIUS)
        
    pygame.display.update() 
board = create_board()
# print(board)
print_board(board)
game_over=False


pygame.init()

SQUARESIZE=100
width = COLUMN_COUNT * SQUARESIZE
height = (ROW_COUNT+1) * SQUARESIZE

size = (width,height)

RADIUS = int(SQUARESIZE/ 2 - 5)

screen = pygame.display.set_mode(size)
draw_board(board) 
pygame.display.update()

myfont=pygame.font.SysFont("timesnewroman",75,bold=True)
turn =random.randint(PLAYER,AI)

while not game_over:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
           sys.exit()
        
        if event.type==pygame.MOUSEMOTION:
            pygame.draw.rect(screen,BLACK,(0,0,width,SQUARESIZE))
            posx=event.pos[0]
            if turn ==PLAYER:
                pygame.draw.circle(screen,RED,(posx,int(SQUARESIZE/2)),RADIUS)
           
        pygame.display.update()
        
        
        if event.type == pygame.MOUSEBUTTONDOWN:
            pygame.draw.rect(screen,BLACK,(0,0,width,SQUARESIZE))
            #player1 turn
            if turn ==PLAYER:  
                posx=event.pos[0]
                col=int(math.floor(posx/SQUARESIZE))
            
                if is_valid_location(board,col):
                    row = get_next_open_row(board,col)
                    drop_piece(board,row,col,PLAYER_PIECE)
                
                    if winning_move(board,PLAYER_PIECE):
                        # print("player1 wins !")
                        label=myfont.render(" you won!",1,RED)
                        screen.blit(label,(40,10))
                        game_over=True
                         
                
                    #switch to ai turn 
                    turn +=1
                    turn = turn %2 
                    
                    print_board(board) 
                    draw_board(board)
            if turn ==AI and not game_over:
                
                col,minmax_score=minimax(board,4,True)

            #    col=valid_moves(board)
           
                if is_valid_location(board, col):
			       #pygame.time.wait(500)
                    row = get_next_open_row(board, col)
                    drop_piece(board, row, col, AI_PIECE)

                    if winning_move(board, AI_PIECE):
                            label = myfont.render("  AI wins!", 1, YELLOW)
                            screen.blit(label, (40,10))
                            game_over = True

                    print_board(board)
                    draw_board(board)

                    turn += 1
                    turn = turn % 2

    if game_over:
	    	pygame.time.wait(3000)