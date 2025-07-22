import random

pieceScore = {"K": 100, "Q": 10, "R": 5, "B": 3, "N": 3, "p": 1}

knightScores = [
    [1, 1, 1, 1, 1, 1, 1, 1],
    [1, 2, 2, 2, 2, 2, 2, 1],
    [1, 2, 3, 3, 3, 3, 2, 1],
    [1, 2, 3, 4, 4, 3, 2, 1],
    [1, 2, 3, 4, 4, 3, 2, 1],
    [1, 2, 3, 3, 3, 3, 2, 1],
    [1, 2, 2, 2, 2, 2, 2, 1],
    [1, 1, 1, 1, 1, 1, 1, 1],
]

bishopScores = [
    [4, 3, 2, 1, 1, 2, 3, 4],
    [3, 4, 3, 2, 2, 3, 4, 3],
    [2, 3, 4, 3, 3, 4, 3, 2],
    [1, 2, 3, 4, 4, 3, 2, 1],
    [1, 2, 3, 4, 4, 3, 2, 1],
    [2, 3, 4, 3, 3, 4, 3, 2],
    [3, 4, 3, 2, 2, 3, 4, 3],
    [4, 3, 2, 1, 1, 2, 3, 4],
]

queenScores = [
    [1, 1, 1, 3, 1, 1, 1, 1],
    [1, 2, 3, 3, 3, 1, 1, 1],
    [1, 4, 3, 3, 3, 4, 2, 1],
    [1, 2, 3, 3, 3, 2, 2, 1],
    [1, 2, 3, 3, 3, 2, 2, 1],
    [1, 4, 3, 3, 3, 4, 2, 1],
    [1, 1, 2, 3, 3, 1, 1, 1],
    [1, 1, 1, 3, 1, 1, 1, 1],
]

rookScores = [
    [4, 3, 4, 4, 4, 4, 3, 4],
    [4, 4, 4, 4, 4, 4, 4, 4],
    [1, 1, 2, 3, 3, 2, 1, 1],
    [1, 2, 3, 4, 4, 3, 2, 1],
    [1, 2, 3, 4, 4, 3, 2, 1],
    [1, 1, 2, 3, 3, 2, 1, 1],
    [4, 4, 4, 4, 4, 4, 4, 4],
    [4, 3, 4, 4, 4, 4, 3, 4],
]

whitePawnScores = [
    [8, 8, 8, 8, 8, 8, 8, 8],
    [8, 8, 8, 8, 8, 8, 8, 8],
    [5, 6, 6, 7, 7, 6, 6, 5],
    [2, 3, 3, 5, 5, 3, 3, 2],
    [1, 2, 3, 4, 4, 3, 2, 1],
    [1, 1, 2, 3, 3, 2, 1, 1],
    [1, 1, 1, 0, 0, 1, 1, 1],
    [0, 0, 0, 0, 0, 0, 0, 0],
]

blackPawnScores = [
    [0, 0, 0, 0, 0, 0, 0, 0],
    [1, 1, 1, 0, 0, 1, 1, 1],
    [1, 1, 2, 3, 3, 2, 1, 1],
    [1, 2, 3, 4, 4, 3, 2, 1],
    [2, 3, 3, 5, 5, 3, 3, 2],
    [5, 6, 6, 7, 7, 6, 6, 5],
    [8, 8, 8, 8, 8, 8, 8, 8],
    [8, 8, 8, 8, 8, 8, 8, 8],
]

kingScores = [
    [ 3,  4,  4,  5,  5,  4,  4,  3],
    [ 3,  4,  4,  5,  5,  4,  4,  3],
    [ 3,  4,  4,  5,  5,  4,  4,  3],
    [ 3,  4,  4,  5,  5,  4,  4,  3],
    [ 2,  3,  3,  4,  4,  3,  3,  2],
    [ 1,  2,  2,  2,  2,  2,  2,  1],
    [ 2,  2,  0,  0,  0,  0,  2,  2],
    [ 2,  3,  1,  0,  0,  1,  3,  2]
]

kingScoresEndGame = [
    [0, 1, 2, 3, 3, 2, 1, 0],
    [2, 2, 1, 0, 0, 1, 2, 2],
    [2, 1, 2, 3, 3, 2, 1, 2],
    [2, 1, 3, 4, 4, 3, 1, 2],
    [2, 1, 3, 4, 4, 3, 1, 2],
    [2, 1, 2, 3, 3, 2, 1, 2],
    [2, 3, 0, 0, 0, 0, 3, 2],
    [0, 2, 2, 2, 2, 2, 2, 0]
]

# map eaching of the pieces to the appropriate 2d array
piecePositionScores = {
    "N": knightScores,
    "B": bishopScores,
    "Q": queenScores,
    "R": rookScores,
    "K": kingScores,
    "bp": blackPawnScores,
    "wp": whitePawnScores,
}

CHECKMATE = 1000
STALEMATE = 0
DEPTH = 3


def findRandomMove (validMoves):
    return validMoves[random.randint(0, len(validMoves)-1)]


'''Method to make first recurssive call'''
def findBestMove(gs, validMoves):
    global nextMove, counter
    nextMove = None
    counter = 0
    #findMoveMinMax (gs, validMoves, DEPTH, gs.whiteToMove)
    #findMoveNegaMax(gs, validMoves, DEPTH, 1 if gs.whiteToMove else -1)
    
    findMoveNegaMaxAlphaBeta(gs, validMoves, DEPTH, -CHECKMATE, CHECKMATE, 1 if gs.whiteToMove else -1)
    print (counter)
    return nextMove


def findMoveNegaMaxAlphaBeta(gs, validMoves, depth, alpha, beta, turnMultiplier):
    global nextMove, counter
    counter += 1
    if depth == 0:
        return turnMultiplier * evaluateBoard(gs)
    
    #move ordering
    def moveScore(move):
        if move.pieceCaptured != "--":
            return 10 * pieceScore[move.pieceCaptured[1]] - pieceScore[move.pieceMoved[1]]
        else:
            return 0  # non-captures are less urgent

    validMoves.sort(key=moveScore, reverse=True)

    maxScore = -CHECKMATE
    for move in validMoves:
        gs.makeMove(move)
        nextMoves = gs.getValidMoves()
        score = -findMoveNegaMaxAlphaBeta(gs, nextMoves, depth-1, -beta, -alpha, -turnMultiplier)
        if score > maxScore:
            maxScore = score
            if depth == DEPTH:
                nextMove = move
        gs.undoMove()
        if maxScore > alpha: #pruning
            alpha = maxScore
        if alpha >= beta:
            break
    return maxScore


'''
a positive score means white is winning and negative score means black is winning
'''
def evaluateBoard(gs):
    # checking for those two basic cases here instead of doing
    # that in the findMoveMinMax()
    if gs.checkmate:
        if gs.whiteToMove:
            return -CHECKMATE  # black wins
        else:
            return CHECKMATE  # white wins
    elif gs.stalemate:
        return STALEMATE
    pieceCount = sum(1 for row in gs.board for square in row if square != "--")
    is_endgame = pieceCount <= 12
    if is_endgame:
        piecePositionScores ["K"] = kingScoresEndGame

    score = 0
    for row in range(len(gs.board)):
        for col in range(len(gs.board[row])):
            square = gs.board[row][col]
            if square != "--":
                pps = 0
                fac = 0.2
                color = square[0]
                piece = square[1]
                if piece != "K":
                    pps += (
                        piecePositionScores[piece if piece != "p" else square][row][col]
                        * fac
                    )
                if color == "w":
                    score += pieceScore[piece] + pps
                elif color == "b":
                    score -= pieceScore[piece] + pps
    return score

