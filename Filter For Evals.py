import chess
import chess.pgn

pgn = open(r"C:\Users\Evan Conway\Desktop\Programming\Python\Stockfish Chess Game\games1.pgn")

while True:
    game = chess.pgn.read_game(pgn)
    if(game == None):
        break
    if(game.next().eval() != None):
        print(game, file=open("games1_evals.PGN", "a"), end="\n\n")
