from functions import *
from visual import *
from pygame.locals import *

height = 16
width = 16
num_mines = 40
print("Mine density:", num_mines / (height * width))
num_flags = 0
gameBoard = genBoard(height, width, num_mines)   # The board which determines if there is a mine or not in each square
knownBoard = genKnownBoard(height,width)         # The board that has what is shown to the player
probsBoard = None                                # The board which contains the probability of each square having a bomb
seen = []                                        # A list of the squares which have number 0 that have already been cleared
firstClick = True                               # First click initiation model
Gameprocess = True                               #Game in process
none_count= 0                                    #Calculation of hide cells

SQ_SIZE = 26                                     # Side length of each square in the board (probably in pixels)
clock = p.time.Clock()
p.init()
screen = p.display.set_mode((width*SQ_SIZE, height*SQ_SIZE))

lost, win = False, False    # Whether the game has been lost or not
display = False   # Whether the probabilities are shown or not
while Gameprocess:
    drawBoard(screen, knownBoard,gameBoard,probsBoard,SQ_SIZE,lost,display)
    clock.tick(MAX_FPS)
    p.display.flip()
    for e in p.event.get():
        if e.type == QUIT:
           Gameprocess = False
        if e.type == p.KEYDOWN:
            if e.key == p.K_q:
                Gameprocess = False 
            if e.key == p.K_p:
                display = True
                probsBoard = calcprobs(knownBoard, num_mines - num_flags)
                print(20*"=")
            elif e.key == p.K_l:
                display = False
            elif e.key == p.K_c:
                # Flags and clear the squares that are certainly mines or not
                for y,row in enumerate(probsBoard):
                    for x,cell in enumerate(row):
                        if cell == 0.0:
                            knownBoard[y][x] = squareNum((y, x), gameBoard)
                        elif cell == 1.0:
                            knownBoard[y][x] = '🚩'
                # Recounts the number of flags. This is to prevent some issues in which the number of flags was incorrect
                num_flags = sum(row.count('🚩') for row in knownBoard)
                cleanboard(knownBoard,gameBoard,seen)
            #GHY:New game action via N key pressed
            if e.key == p.K_n:  
                gameBoard, knownBoard, probsBoard = None,None, None
                num_flags = 0
                gameBoard = genBoard(height, width, num_mines)   # The board which determines if there is a mine or not in each square
                knownBoard = genKnownBoard(height,width)         # The board that has what is shown to the player
                seen = [] 
                display = False
                firstClick = True                               # First click initiation model
                Gameprocess = True                               # Game procces status to proper quit function
                lost, win = False, False    
        if e.type == p.MOUSEBUTTONDOWN:
            location = p.mouse.get_pos()
            col = location[0] // SQ_SIZE
            row = location[1] // SQ_SIZE
            if lost or win: break                           #Block click on win or lost game
            if e.button == 1:
                ##One-click chording 
                if knownBoard[row][col] == 1 or 2 or 3 or 4 or 5 or 6 or 7 or 8:
                    if knownBoard[row][col] == flagsNum((row, col),knownBoard):
                        for chrd in surrounds((row, col),knownBoard):
                            if knownBoard[chrd[0]][chrd[1]] == None: 
                                knownBoard[chrd[0]][chrd[1]] = squareNum((chrd[0],chrd[1]),gameBoard)
                if gameBoard[row][col] == 1:
                    if firstClick:                                  #GHY: Firstclick gameboard regeneration - 1st(simple) attempt
                        print ("Gameboard regenaration")
                        gameBoard = None
                        gameBoard = genBoard(height, width, num_mines)
                        knownBoard[row][col] = squareNum((row,col),gameBoard)   #Click action overhalt
                        cleanboard(knownBoard,gameBoard,seen)                   #Click action overhalt
                        break
                    if knownBoard[row][col] != '🚩':
                        knownBoard[row][col]= "b"
                        print("It was a mine!")
                        lost = True
                else:
                    knownBoard[row][col] = squareNum((row,col),gameBoard)
                    cleanboard(knownBoard,gameBoard,seen)
            elif e.button == 3:
                if knownBoard[row][col] == None:
                    knownBoard[row][col] = '🚩'
                    num_flags += 1
                    print("Number of flags:", num_flags, num_mines - num_flags, "left")
                elif knownBoard[row][col] == '🚩':
                    knownBoard[row][col] = None
                    num_flags -= 1
                    print("Number of flags:", num_flags)
            firstClick = False
    if not win and not lost: none_count = sum(row.count(None) for row in knownBoard) # count number of empty cells
    if (num_flags + none_count) == num_mines and not lost and not win: # Win detection
        win = True
        print("You win!!!!")   
               

p.quit()

