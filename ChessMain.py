import pygame as py

import ChessEngine, ChessBotAlgorithm, ChessClock


UI_MARGIN = 60
BOARD_WIDTH = BOARD_HEIGHT = 512
MOVE_LOG_PANEL_WIDTH = 250
MOVE_LOG_PANEL_HEIGHT = BOARD_HEIGHT
DIMENSION = 8
SQ_SIZE = BOARD_HEIGHT // DIMENSION
MAX_FPS = 15
IMAGES = {}
WINDOW_HEIGHT = BOARD_HEIGHT + UI_MARGIN


def load_images():
    pieces = {'bR','bN','bB','bQ','bK','bp','wR','wN','wB','wQ','wK','wp'}
    for piece in pieces:
        IMAGES [piece] = py.transform.scale(py.image.load("images/" + piece + ".png"), (SQ_SIZE, SQ_SIZE))


def main():
    py.init()
    py.mixer.init()
    move_sound = py.mixer.Sound(r"E:\working folder\vs codes\Chess Bot\sounds\move-self.mp3")
    capture_sound = py.mixer.Sound(r"E:\working folder\vs codes\Chess Bot\sounds\capture.mp3")
    check_sound = py.mixer.Sound(r"E:\working folder\vs codes\Chess Bot\sounds\move-check.mp3")
    castle_sound = py.mixer.Sound(r"E:\working folder\vs codes\Chess Bot\sounds\castle.mp3")
    game_over_sound = py.mixer.Sound(r"E:\working folder\vs codes\Chess Bot\sounds\game-end.mp3")

    
    game_clock = ChessClock.ChessClock(180)  # 3-minute timer
    screen = py.display.set_mode((BOARD_WIDTH , WINDOW_HEIGHT))  # Increased window height for clocks
    # Define timer positions (for example, top corners)
    WHITE_Y = BOARD_HEIGHT + 10
    BLACK_Y = BOARD_HEIGHT + 10
    white_timer_pos = (10, WHITE_Y)
    black_timer_pos = (BOARD_WIDTH - 160, BLACK_Y)


    FPS_clock = py.time.Clock()
    screen.fill(py.Color("white"))

    gs = ChessEngine.GameState()
    validMoves = gs.getValidMoves()
    moveMade = False
    animate = False #flag for when we want to see animation and when we dont
    load_images()
    running = True
    selected_square = ()
    playerClicks = [] #tuple two store value starting sq and destination square (eg : [(6, 4), (4, 8)])
    gameOver = False
    playerOne = True # If human is playing white then this is true if Bot is playing this is False
    playerTwo = False # same as above but for black
    winner_by_time = None  


    while running:
        game_clock.update()

        time_up = game_clock.is_time_up()
        if time_up and not gameOver:
            gameOver = True
            winner_by_time = 'black' if time_up == 'white' else 'white'

        humanTurn = (gs.whiteToMove and playerOne) or (not gs.whiteToMove and playerTwo)

        for e in py.event.get():
            if e.type == py.QUIT:
                running = False
            elif e.type == py.MOUSEBUTTONDOWN:
                if not gameOver and humanTurn:
                    location = py.mouse.get_pos() # get x,y cords of the mouse
                    col = location [0]//SQ_SIZE
                    row = location[1]//SQ_SIZE
                    if 0 <= row < 8 and 0 <= col < 8:
                        if selected_square == (row, col) or col >= 8: # user clicking on same square twice or user clicked movelog
                            selected_square = () # unselect the sdelected sq
                            playerClicks = []
                        else:
                            selected_square = (row, col)
                            playerClicks.append(selected_square)
                        if len(playerClicks) == 2:
                            move = ChessEngine.Move (playerClicks[0], playerClicks[1], gs.board)
                            
                            for i in range(len(validMoves)):
                                if move == validMoves[i]:
                                    game_clock.save_state()                                
                                    gs.makeMove(validMoves[i])
                                    game_clock.switch_player()
                                    moveMade = True
                                    animate = True
                                    
                                    if move.isCastleMove:
                                        print("castle")
                                        castle_sound.play()
                                    elif gs.isCheck():  
                                        print("check")
                                        check_sound.play()
                                    elif move.pieceCaptured != "--" or move.isEnpassantMove :
                                        print("Capture")
                                        capture_sound.play()
                                    else:
                                        print("moved")
                                        move_sound.play()

                                    selected_square = () # reset selected sq
                                    playerClicks = []
                            if not moveMade:
                                playerClicks = [selected_square]

            elif e.type == py.KEYDOWN:
                if e.key == py.K_u: #undo when pressing u
                    gs.undoMove()
                    game_clock.undo()
                    moveMade = True
                    animate = False #dont see animation in undo
                    gameOver = False
                    
                if e.key == py.K_r: #reset the board when pressing r key
                    gs = ChessEngine.GameState()
                    game_clock = ChessClock.ChessClock(180)
                    validMoves = gs.getValidMoves()
                    selected_square = ()
                    playerClicks = []
                    moveMade = False
                    animate = False
                    gameOver = False

        #Bot Move Finder
        if not gameOver and not humanTurn:
            BotMove = ChessBotAlgorithm.findBestMove(gs, validMoves)
            if BotMove is None:
                BotMove = ChessBotAlgorithm.findRandomMove(validMoves)
            game_clock.save_state()
            gs.makeMove(BotMove)
            game_clock.switch_player()
            moveMade = True
            animate = True
            if BotMove.isCastleMove:
                castle_sound.play()
            elif BotMove.pieceCaptured != "--" or BotMove.isEnpassantMove:
                capture_sound.play()
            elif gs.isCheck(): 
                check_sound.play()
            else:
                move_sound.play()            


        if moveMade:
            print (move.getChessNotation())
            if animate:
                animateMove(gs.moveLog[-1], screen, gs.board, FPS_clock)
            validMoves = gs.getValidMoves()
            moveMade = False
            animate = False


        drawGameState (screen, gs, validMoves, selected_square)
        py.draw.rect(
            screen, py.Color("white"),
            py.Rect(0, BOARD_HEIGHT, BOARD_WIDTH, UI_MARGIN)
        )
        drawText(screen, f"White: {game_clock.format_time(game_clock.white_time)}", white_timer_pos)
        drawText(screen, f"Black: {game_clock.format_time(game_clock.black_time)}", black_timer_pos)


        if (gs.checkmate or gs.stalemate) and not gameOver:
            gameOver = True
            game_over_sound.play()

        if gameOver:
            if winner_by_time:
                drawEndGameText(screen, f"{winner_by_time.capitalize()} wins on time!")
            else:
                drawEndGameText(screen, 'Stalemate' if gs.stalemate else 'Black wins by checkmate' if gs.whiteToMove else 'White wins by checkmate')


        FPS_clock.tick(MAX_FPS)
        py.display.flip()



def drawGameState (screen, gs, validMoves, selected_square):
    drawBoard(screen)
    highlightSquares(screen, gs, validMoves, selected_square)
    drawPieces (screen, gs.board)



def drawBoard(screen):
    global colors
    colors = [py.Color("bisque2"), py.Color("burlywood3")]
    for row in range(DIMENSION):
        for col in range(DIMENSION):
            color = colors[(row + col) % 2]
            py.draw.rect(screen, color, py.Rect(col * SQ_SIZE, row * SQ_SIZE, SQ_SIZE, SQ_SIZE))

'''
highlight the piece slected and also where it can move
'''
def highlightSquares (screen, gs, validMoves, selected_square):
    if selected_square != ():
        r, c, = selected_square
        if gs.board[r][c][0] == ('w' if gs.whiteToMove else 'b'): #sq selected is piece that can be moved
            #highlight sq
            s = py.Surface((SQ_SIZE, SQ_SIZE))
            s.set_alpha(100) # value of transparency of the highlighting color
            s.fill(py.Color('blue'))
            screen.blit(s, (c*SQ_SIZE, r*SQ_SIZE))

            #highlight all valid move that comes from that square
            s.fill(py.Color('yellow'))
            for move in validMoves:
                if move.startRow == r and move.startCol == c:
                    screen.blit(s, (move.endCol*SQ_SIZE, move.endRow*SQ_SIZE))


def drawPieces(screen, board):
    for row in range(DIMENSION):
        for col in range(DIMENSION):
            piece = board [row][col]
            if piece != "--":
                screen.blit(IMAGES[piece], py.Rect(col * SQ_SIZE, row * SQ_SIZE, SQ_SIZE, SQ_SIZE))

'''
function for animation
'''
def animateMove(move, screen, board, clock):
    global colors
    dR = move.endRow - move.startRow #representing th row where image will appear breifly
    dC = move.endCol - move.startCol #representing th column where image will appear breifly
    framesPerSq = 5 #frame to move one square
    frameCount = (abs(dR) + abs(dC)) * framesPerSq
    for frame in range(frameCount+1):
        r, c = (move.startRow + dR*frame/frameCount, move.startCol + dC*frame/frameCount)
        drawBoard(screen)
        drawPieces(screen, board)
        #erase piece from its end location
        color = colors [(move.endRow + move.endCol) % 2]
        endSq = py.Rect(move.endCol*SQ_SIZE, move.endRow*SQ_SIZE, SQ_SIZE, SQ_SIZE)
        py.draw.rect(screen, color, endSq)
        #draw captured piece onto the rectangle
        if move.pieceCaptured != '--':
            if move.isEnpassantMove:
                enPassantRow = move.endRow + 1 if move.pieceCaptured[0] == 'b' else move.endRow - 1
                endSq = py.Rect(move.endCol*SQ_SIZE, enPassantRow*SQ_SIZE, SQ_SIZE, SQ_SIZE)
            screen.blit(IMAGES[move.pieceCaptured], endSq)
        #draw movin piece
        screen.blit(IMAGES[move.pieceMoved], py.Rect(c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE))
        py.display.flip()
        clock.tick(60)
    
def drawEndGameText (screen, text):
    font = py.font.SysFont("Helvetica", 32, True, False)
    textObject = font.render(text, 0, py.Color('Gray'))
    textlocation = py.Rect(0,0,BOARD_WIDTH, BOARD_HEIGHT).move(BOARD_WIDTH/2 - textObject.get_width()/2, BOARD_HEIGHT/2 - textObject.get_height()/2)
    screen.blit(textObject,textlocation)
    textObject = font.render(text, 0, py.Color("Black"))
    screen.blit(textObject,textlocation.move(2, 2))


def drawText(screen, text, pos, fontSize=24, color=(0, 0, 0)):
    font = py.font.SysFont('Arial', fontSize)
    text_surface = font.render(text, True, color)
    screen.blit(text_surface, pos)

def drawClock(screen, game_clock):
    white_time, black_time = game_clock.get_time()
    font = py.font.SysFont("Arial", 32, True, False)

    white_text = font.render(f"White: {game_clock.format_time(white_time)}", True, py.Color("black"))
    black_text = font.render(f"Black: {game_clock.format_time(black_time)}", True, py.Color("black"))

    screen.blit(white_text, (10, 10))
    screen.blit(black_text, (10, 50))


if __name__ == "__main__":
    main()
