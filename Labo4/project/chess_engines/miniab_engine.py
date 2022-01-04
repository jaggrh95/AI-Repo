import chess

from chess_agents.MiniMaxAB import *

class MiniMaxABEngine():

    def engine_operation(self):
        # Create a clean chess board
        board = chess.Board()
        n = 0
        print(board)
        while n < 100:
            if n % 2 == 0:
                move = input("Enter move: ")
                move = chess.Move.from_uci(str(move))
                board.push(move)
            else:
                print("Computers Turn:")
                move = minimaxRoot(3, board, True)
                move = chess.Move.from_uci(str(move))
                board.push(move)
            print(board)
            n += 1


    def __uci(self):
        print("""id name {}
id author {}
option name Debug Log File type string default
option name Contempt type spin default 0 min -100 max 100
option name Threads type spin default 1 min 1 max 128
option name Hash type spin default 16 min 1 max 1048576
option name Clear Hash type button
option name Ponder type check default false
option name MultiPV type spin default 1 min 1 max 500
option name Skill Level type spin default 20 min 0 max 20
option name Move Overhead type spin default 30 min 0 max 5000
option name Minimum Thinking Time type spin default 20 min 0 max 5000
option name Slow Mover type spin default 89 min 10 max 1000
option name nodestime type spin default 0 min 0 max 10000
option name UCI_Chess960 type check default false
option name SyzygyPath type string default <empty>
option name SyzygyProbeDepth type spin default 1 min 1 max 100
option name Syzygy50MoveRule type check default true
option name SyzygyProbeLimit type spin default 6 min 0 max 6
uciok""".format(self.name, self.author))