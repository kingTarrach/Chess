from piece import ChessPiece
import copy

def find_piece(pieces, position):
    for piece in pieces:
        if (position == piece.get_position()):
            return piece
    return None

class King(ChessPiece):
    
    def __init__(self, color, position, size, game_surface, board_offset_x, board_offset_y, block_size):
        super().__init__(color, position, size, game_surface, board_offset_x, board_offset_y, block_size)
        self.piece_type = "king"
        self.image = self.load_image_by_width()
        if self.image is not None:
            self.rect = self.image.get_rect(topleft=self.place_by_board_position(self.position))  # Renamed method
    
    def check_for_moves(self):
        pass
            
    def move_check_helper(self, direction_value, opposing_color, move_number):
        pass      
        
    def check_for_king_moves(self):
        if self.color == "white":
            self.valid_moves = self.king_move_check_helper("black")
        elif self.color == "black":
            self.valid_moves = self.king_move_check_helper("white")
        return self.valid_moves
    
    def king_move_check_helper(self, opposing_color):
        
        print(self.color + " king being calculated.")
        
        validMoves = []
        
        direction_x = 1
        direction_y = 1
        
        for i in range(0, 8):
            position_x = self.position[0]
            position_y = self.position[1]
            if i is 1:
                direction_x = 0
            elif i is 2:
                direction_x = -1
            elif i is 3:
                direction_y = 0
            elif i is 4:
                direction_y = -1
            elif i is 5:
                direction_x = 0
            elif i is 6:
                direction_x = 1
            elif i is 7:
                direction_y = 0
            position_x += (1 * direction_x)
            position_y += (1 * direction_y)
            move_iterator = (position_x, position_y)
            if self.check_boundaries(move_iterator) and self.check_piece_moves(move_iterator, opposing_color) and self.check_piece_list(move_iterator, opposing_color) is not "invalid":
                validMoves.append(move_iterator)
        
        print()
        for piece in self.piece_list:
            print(piece.color + " " + piece.piece_type + "'s moves before recalc: ", end="")
            if piece.valid_moves:
                for move in piece.valid_moves:
                    print(move, end=", ")
            print()
                
        return validMoves
    
    # Checks all of the opposing pieces moves to ensure it doesn't overlap with the king's future position
    def check_piece_moves(self, position, opposing_color):
        
        delete_piece = None     # 
        original_position = self.position   # Save current position
        self.position = position        # Update self position to check against 
        result = self.check_piece_list(self.position, opposing_color)   # 
        
        if result is "capture":
            delete_piece = find_piece(self.piece_list, self.position)
            deleted_index = self.piece_list.index(delete_piece)
            self.piece_list.remove(delete_piece)
            for piece in self.piece_list:
                piece.set_piece_list(self.piece_list)
            self.recalculate_all_opposing_moves()
        else:
            self.recalculate_opposing_pawn()
        
        function_bool = True
        
        for piece in self.piece_list:
            if piece.get_color() is not self.color:
                if piece.valid_moves:
                    for move_position in piece.valid_moves:
                        if move_position == position:
                            function_bool = False
                            break
                    if function_bool is False:
                        break     
        
        self.position = original_position
        if delete_piece:
            self.piece_list.insert(deleted_index, delete_piece)
        
        for piece in self.piece_list:
            piece.set_piece_list(self.piece_list)
        
        return function_bool             
    
    
                            