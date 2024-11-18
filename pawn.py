from piece import ChessPiece

class Pawn(ChessPiece):
    
    def __init__(self, color, position, size, game_surface, board_offset_x, board_offset_y, block_size):
        super().__init__(color, position, size, game_surface, board_offset_x, board_offset_y, block_size)
        self.piece_type = "pawn"
        self.image = self.load_image_by_height()
        if self.image is not None:
            self.rect = self.image.get_rect(topleft=self.place_by_board_position(self.position))  # Renamed method
    
    
    def check_for_moves(self):
        
        if self.color == "black":
            validMoves = self.move_check_helper(1, "white")
        elif self.color == "white":
            validMoves = self.move_check_helper(-1, "black")
        self.valid_moves = validMoves
        return self.valid_moves
            
    def move_check_helper(self, direction_value, opposing_color):
        
        # validMoves[(position of the move)]
        validMoves = []
        
        position_x = self.position[0]
        position_y = self.position[1]
        
        # One move forward
        position_y += (1 * direction_value)
        move_iterator = (position_x, position_y)
        
        result = self.check_piece_list(move_iterator, opposing_color)
        if result == "valid" and self.check_boundaries(move_iterator):
            if self.whose_turn == self.color:    
                validMoves.append(move_iterator)
            elif self.whose_turn != self.color:
                validMoves.append(move_iterator)
            position_y += (1 * direction_value)
            move_iterator = (position_x, position_y)
            result = self.check_piece_list(move_iterator, opposing_color)
            if result == "valid" and self.moves == 0 and self.check_boundaries(move_iterator):
                if self.whose_turn == self.color:    
                    validMoves.append(move_iterator)
                elif self.whose_turn != self.color:
                    validMoves.append(move_iterator)
        
        position_y = self.position[1] + (1 * direction_value)
        position_x += 1
        move_iterator = (position_x, position_y)       
        
        result = self.check_piece_list(move_iterator, opposing_color)
        if result == "capture" and self.check_boundaries(move_iterator):
            if self.whose_turn == self.color and self.save_king_by_capture(move_iterator):    
                validMoves.append(move_iterator)
            elif self.whose_turn != self.color:
                validMoves.append(move_iterator)
        elif result == "king" and self.check_boundaries(move_iterator):
            self.is_checking = True
            if self.whose_turn == self.color:    
                validMoves.append(move_iterator)
            elif self.whose_turn != self.color:
                validMoves.append(move_iterator)
            
        position_x = self.position[0] - 1
        move_iterator = (position_x, position_y)
        
        result = self.check_piece_list(move_iterator, opposing_color)
        if result == "capture" and self.check_boundaries(move_iterator):
            
            if self.whose_turn == self.color and self.save_king_by_capture(move_iterator):    
                validMoves.append(move_iterator)
            elif self.whose_turn != self.color:
                validMoves.append(move_iterator)
                
        elif result == "king" and self.check_boundaries(move_iterator):
            self.is_checking = True
            if self.whose_turn == self.color:    
                validMoves.append(move_iterator)
            elif self.whose_turn != self.color:
                validMoves.append(move_iterator)
        
        
        return validMoves
            