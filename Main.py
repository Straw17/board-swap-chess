import chess
import chess.pgn
import chess.engine
import random

def fillPositions():
    for i in range(-99999, 100000):
        positions[i] = []
    file = open('positions.txt', 'r')
    positionsRaw = file.read()
    file.close()
    positionsRaw = positionsRaw.split("\n")
    for position in positionsRaw:
        splitPos = position.split(",")
        positions[int(splitPos[0])].append(splitPos[1])

def getBoardForEval(evaluation):
    keys = list(positions.keys())
    keys = list(filter(lambda x: len(positions[x]) != 0, keys))
    minValue = abs(min(keys, key=lambda x:abs(x-evaluation)) - evaluation)
    results = [x for x in keys if abs(x-evaluation) == minValue]
    result = random.choice(results)
    result = random.choice(positions[result])
    newBoard = chess.Board(result)
    return newBoard

def evalPiece(uci):
    first = uci[0]
    if first.islower():
        return "P"
    else:
        return first

def getPlayerMove(board, isWhite):
    moves = [board.san(move) for move in list(board.legal_moves)]
    print("Moves: ", end="")
    lastPiece = ""
    for move in list(board.legal_moves):
        move = board.san(move)
        if lastPiece != evalPiece(move):
            lastPiece = evalPiece(move)
            print()
        print(move, end=" ")
    print()
    
    while True:
        try:
            move = input("Enter move: ")
            if move == "quit":
                sys.exit(1)
            board.push_san(move)
            break
        except Exception:
            continue
    return board

def isOver(board):
    outcome = board.outcome()
    if outcome == None:
        return False
    else:
        print()
        print(board)
        print("Game over!")
        print(str(outcome.termination).split(".")[1])
        return True

def runGame():
    board = chess.Board()
    while True:
        lastPieceCount = len(board.piece_map())
        if board.turn is chess.WHITE:
            print()
            print(board)
            board = getPlayerMove(board, (board.turn is chess.WHITE))
        else:
            nextMove = playerEngine.play(board, chess.engine.Limit(time=0.1)).move
            board.push(nextMove)
        if isOver(board):
            break
        score = analysisEngine.analyse(board, chess.engine.Limit(time=1.0))["score"].white().score(mate_score=100000)
        pieceCount = len(board.piece_map())
        if abs(lastPieceCount - pieceCount) > 0:
            lastScore = score
            board = getBoardForEval(score)
            print()
            print("New board!")
            print(board)

positions = {}
fillPositions()
analysisEngine = chess.engine.SimpleEngine.popen_uci(r"C:\Users\Evan Conway\Desktop\Programming\Python\Stockfish Chess Game\stockfish_14.1_win_x64_avx2\stockfish_14.1_win_x64_avx2.exe")
playerEngine = chess.engine.SimpleEngine.popen_uci(r"C:\Users\Evan Conway\Desktop\Programming\Python\Stockfish Chess Game\stockfish_14.1_win_x64_avx2\stockfish_14.1_win_x64_avx2.exe")
playerEngine.configure({"Skill Level": 1})
runGame()
analysisEngine.quit()
playerEngine.quit()
