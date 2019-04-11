from flask import Flask
from flask_restful import Api, Resource, reqparse
from play import *

PLAYER = 0
COMPUTER = 1

class Board(Resource):

    board = [-1]*9

    def get(self):
        """Get the board state
        
        Returns:
            dict -- Contains the representation of the board
        """

        return {
            "board": self.board
        }, 200

    def put(self):
        """Play a move
        
        Returns:
            dict -- The state of the board, moves of the 2 players and a boolean to know wether or not there's a winner
        """

        parser = reqparse.RequestParser()
        parser.add_argument("move")
        args = parser.parse_args()

        free_cells = get_free_cells(self.board)
        player_move = None
        computer_move = None
        depth = len(free_cells)
	# Player plays
        if int(args.move) in free_cells:  # TODO Send an error code
            player_move = int(args.move)
            self.board[player_move] = PLAYER

            # Computer plays
            computer_move = get_random_move(self.board, depth, COMPUTER)
            if computer_move is not None:
                self.board[computer_move] = COMPUTER

        # Check for a winner
        winner = find_winner(self.board)

        return {
            "player_move": player_move,
            "computer_move": computer_move,
            "winner": winner,   
            "board": self.board
        }, 200

    def delete(self):
        """Reset board state
        
        Returns:
            dict -- Contains the representation of the board
        """

        for i in range(len(self.board)):
            self.board[i] = -1
        return {
            "board": self.board
        }, 200


if __name__ == "__main__":
    app = Flask(__name__)

    api = Api(app)
    api.add_resource(Board, "/board")

    app.run(
        host='0.0.0.0',
        port=5001,
        debug=True
    )
