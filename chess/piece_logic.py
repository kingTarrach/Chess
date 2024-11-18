from visuals import *
from game_logic import *
from piece import ChessPiece
from pawn import Pawn
from bishop import Bishop
from rook import Rook
from queen import Queen
from knight import Knight
from king import King


def select_piece(piece):
    piece.check_for_moves()       # Check the current piece to find moves that work
    piece.show_valid_moves()          # Once moves are checked, display all valid moves via gray 
    return piece

# Use this function when a move occurs so only the pieces that have new moves get ran
def calculate_piece_moves(white_pieces, black_pieces, whose_turn):
    
    if whose_turn == "white":
        calculate_one_color(white_pieces)
        calculate_one_color(black_pieces)
    elif whose_turn == "black":
        calculate_one_color(black_pieces)
        calculate_one_color(white_pieces)
    

def calculate_one_color(color_pieces):
    king = None
    for piece in color_pieces:
        if piece.piece_type == "king":
            king = piece
        else:
            piece.generate_moves()
    
    king.generate_moves()


# Checks if the passed in color is in check
def is_check(pieces, color):
    
    king = return_king(color, pieces)
    
    if king is None:
        return None
    
    for piece in pieces:
        if piece.get_color() is not color and piece.piece_type is not "king":
            for move_position in piece.valid_moves:
                if king.get_position() == move_position:
                    return color
    
    return None             

# Once there is a check, we need to check if it's a checkmate
# Checkmate happens if the following conditions are true:
# 1. The king has no where to move (king.valid_moves = None)
# 2. The king has no pieces that can capture another piece to save the king
# 3. The king has no pieces that can block the opposing pieces to save the king'
def check_protocol(pieces, color):
    
    #for piece in pieces:
        
    
    for piece in pieces:
        if piece.get_color() == color:
            if piece.piece_type == "king":
                return_king_moves(piece)
            else:
                piece.valid_moves = save_by_capture(pieces, piece)
    
    
    return pieces

def print_color_moves(pieces, color):
    
    for piece in pieces:
        if piece.color is color:
            print(piece.color + " " + piece.piece_type + "'s moves: ")
            for move in piece.valid_moves:
                print(str(move), end=", ")
            print()

def remove_all_moves(pieces):
    for piece in pieces:
        piece.valid_moves = None
    
def check_for_checkmate(color, pieces):
      
    for piece in pieces:
        if piece.color is color:
            if piece.valid_moves:
                return None
    
    return color

# Condition 1
def return_king_moves(king):
    return king.generate_moves()

# Condition 2
def save_by_capture(pieces, piece):
    
    if piece.color == "white":
        opposing_color = "black"
    elif piece.color == "black":
        opposing_color = "white"
    
    checking_pieces = return_all_checking_pieces(pieces, opposing_color)

    potential_captures = []
    potential_blocks = []
    # Check if one of the pieces on the side of the checking king
    # can capture a piece that is checking the king
    # If it can, recalculate the moves and see if one move allows the
    # king to not be in check anymore
    for move in piece.valid_moves:
        for checking_piece in checking_pieces:
            if move == checking_piece.position:
                print("Potential capture: " + str(move))
                potential_captures.append(checking_piece)
            else:
                for checking_move in checking_piece.valid_moves:
                    if move == checking_move:
                        print("Potential block: " + str(move))
                        potential_blocks.append(move)
                     
    potential_moves = []
    for checking_piece in potential_captures:
        
        delete_piece = checking_piece
        deleted_index = piece.piece_list.index(delete_piece)
        original_position = piece.position
        piece.position = checking_piece.position
        
        pieces.remove(delete_piece)
        for other_pieces in pieces:
            other_pieces.set_piece_list(pieces)
        piece.recalculate_all_opposing_moves()
        
        isCheck = is_check(pieces, piece.color)
        if isCheck is None:
            potential_moves.append(piece.position)
        
        piece.position = original_position
        pieces.insert(deleted_index, delete_piece)
        for other_piece in pieces:
            other_piece.set_piece_list(pieces)
    
    if potential_captures:
        piece.recalculate_all_opposing_moves()
    isCheck = None    
    
    for move_x, move_y in potential_blocks:
        
        move_position = (move_x, move_y)
        original_position = piece.position
        piece.position = move_position
        
        for other_piece in pieces:
            other_piece.set_piece_list(pieces)
        piece.recalculate_all_opposing_moves()
        isCheck = is_check(pieces, piece.color)
        if isCheck is None:
            potential_moves.append(piece.position)
        
        piece.position = original_position
        for other_piece in pieces:
            other_piece.set_piece_list(pieces)
    
    if potential_blocks:
        piece.recalculate_all_opposing_moves()    
    
    return potential_moves
            
# Function to return all the checking pieces for a gicen color
def return_all_checking_pieces(pieces, opposing_color):
    
    if opposing_color == "white":
        color = "black"
    elif opposing_color == "black":
        color = "white"
    
    opposing_king = return_king(color, pieces)
    
    checking_pieces = []
    for piece in pieces:
        if piece.color == opposing_color:
            for move in piece.valid_moves:
                if move == opposing_king.position:
                    checking_pieces.append(piece)
            
    return checking_pieces

# Reset piece checks
def reset_piece_checks(pieces, opposing_color):
    
    for piece in pieces:
        if piece.is_checking == True and piece.get_color() == opposing_color:
            piece.is_checking = False            

# Return the king
def return_king(color, pieces):
    
    for piece in pieces:
        if piece.get_color() == color and piece.piece_type == "king":
            return piece
        
    return None

def print_all_moves(pieces):
    for piece in pieces:
        print(piece.color + " " + piece.piece_type + "'s moves: ", end="")
        for move in piece.valid_moves:
            print(str(move), end=", ")
        print()
    print()    
        