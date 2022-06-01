import chess
import chess.pgn

pgn = open(r"C:\Users\Evan Conway\Desktop\Programming\Python\Stockfish Chess Game\games1_evals.pgn")

while True:
    game = chess.pgn.read_game(pgn)
    if(game == None):
        break
    move = game.next()
    while True:
        if(move == None or move.eval() == None):
            break
        board = move.board().fen()
        score = move.eval().white().score(mate_score=100000)
        string = str(score) + "," + str(board)
        print(string, file=open("positions.txt", "a"), end="\n")
        move = move.next()
