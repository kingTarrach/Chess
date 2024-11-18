from piece_logic import *



def initializeBoardMatrix():
    # Create an 8x8 board_matrix initialized with an empty string or a specific label
    board_matrix = [['' for _ in range(8)] for _ in range(8)]
    
    # Columns 0 to 7
    cols = [i for i in range(8)]

    # Rows 0 to 7
    rows = [i for i in range(8)]

    # Fill the board_matrix with tuples
    board_matrix = [[(cols[j], rows[i]) for j in range(8)] for i in range(8)]
    
    return board_matrix


def standard_chess_setup(piece_size, game_surface, board_offset_x, board_offset_y, block_size):
    
    pieces = []
    
    pieces += setup_one_side("black", "top", piece_size, game_surface, board_offset_x, board_offset_y, block_size)
    pieces += setup_one_side("white", "bottom", piece_size, game_surface, board_offset_x, board_offset_y, block_size)
    
    pieces = initialize_pieces(pieces)
    
    return pieces

def setup_one_side(color, side, piece_size, game_surface, board_offset_x, board_offset_y, block_size):
    
    pieces = []
    if side == "top":
        y_position = 0
    elif side == "bottom":
        y_position = 7

    pieces.append(Rook(color, (0, y_position), piece_size, game_surface, board_offset_x, board_offset_y, block_size))
    pieces.append(Knight(color, (1, y_position), piece_size, game_surface, board_offset_x, board_offset_y, block_size))
    pieces.append(Bishop(color, (2, y_position), piece_size, game_surface, board_offset_x, board_offset_y, block_size))
    pieces.append(Queen(color, (3, y_position), piece_size, game_surface, board_offset_x, board_offset_y, block_size))
    pieces.append(King(color, (4, y_position), piece_size, game_surface, board_offset_x, board_offset_y, block_size))
    pieces.append(Rook(color, (7, y_position), piece_size, game_surface, board_offset_x, board_offset_y, block_size))
    pieces.append(Knight(color, (6, y_position), piece_size, game_surface, board_offset_x, board_offset_y, block_size))
    pieces.append(Bishop(color, (5, y_position), piece_size, game_surface, board_offset_x, board_offset_y, block_size))
    
    if side == "top":
        y_position += 1
    elif side == "bottom":
        y_position -= 1
    
    for i in range(0, 8):
        pieces.append(Pawn(color, (i, y_position), piece_size, game_surface, board_offset_x, board_offset_y, block_size))
        
    return pieces
    

def create_pieces(piece_size, game_surface, board_offset_x, board_offset_y, block_size):
  
    pieces = []
    
    pieces.append(Bishop("black", (4, 2), piece_size, game_surface, board_offset_x, board_offset_y, block_size))
    pieces.append(King("white", (4, 5), piece_size, game_surface, board_offset_x, board_offset_y, block_size))  
    pieces.append(King("black", (5, 2), piece_size, game_surface, board_offset_x, board_offset_y, block_size))
    pieces.append(Queen("black", (0, 4), piece_size, game_surface, board_offset_x, board_offset_y, block_size))
    pieces.append(Rook("white", (2, 4), piece_size, game_surface, board_offset_x, board_offset_y, block_size))  
      
    
    pieces = initialize_pieces(pieces)
    
    return pieces

def initialize_pieces(pieces):
    
    king_pieces = []
    
    for piece in pieces:
        if piece.get_piece_type() != "king":
            piece.set_piece_list(pieces)
            piece.generate_moves()
        elif piece.get_piece_type() == "king":
            king_pieces.append(piece)
     
    for king in king_pieces:
        king.set_piece_list(pieces)
    for king in king_pieces:
        king.generate_moves()    
    return pieces
    
def change_whose_turn(pieces, new_turn_color):
    
    for piece in pieces:
        piece.whose_turn = new_turn_color
        
def detect_location(piece_list, location):
    for piece in piece_list:
        if (piece.get_position() == location):
            return True
    return False

def find_piece(pieces, position):
    for piece in pieces:
        if (position == piece.get_position()):
            return piece
    return None
       
def convert_coords_to_position(coords, block_size, board_offset_x, board_offset_y):
    x, y = coords
    board_x = -1
    board_y = -1
    for i in range(0, 8):
        if (x >= (block_size * i) + board_offset_x and x <= (block_size * i) + board_offset_x + block_size):
            board_x = i
        if (y >= (block_size * i) + board_offset_y and y <= (block_size * i) + board_offset_y + block_size):
            board_y = i
    return (board_x, board_y)