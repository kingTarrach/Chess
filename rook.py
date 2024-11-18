from piece import ChessPiece

class Rook(ChessPiece):
    
    def __init__(self, color, position, size, game_surface, board_offset_x, board_offset_y, block_size):
        super().__init__(color, position, size, game_surface, board_offset_x, board_offset_y, block_size)
        self.piece_type = "rook"
        self.image = self.load_image_by_height()
        if self.image is not None:
            self.rect = self.image.get_rect(topleft=self.place_by_board_position(self.position))  # Renamed method
    
    
    def check_for_moves(self):
        if self.color == "white":
            self.valid_moves = self.move_check_helper("black")
        elif self.color == "black":
            self.valid_moves = self.move_check_helper("white")
        return self.valid_moves
            
    def move_check_helper(self, opposing_color):
        
        validMoves = []
        
        x_iterator = -1
        y_iterator = 0
                
        for i in range(0, 4):
            # Move left
            position_x = self.position[0]
            position_y = self.position[1]
            
            if i == 1:
                x_iterator = 1
            elif i == 2:
                x_iterator = 0
                y_iterator = 1
            elif i == 3:
                y_iterator = -1
            
            position_x += x_iterator
            position_y += y_iterator
            
            move_iterator = (position_x, position_y)
            result = self.check_piece_list(move_iterator, opposing_color)
            
            while result is "valid" and self.check_boundaries(move_iterator):
                if self.whose_turn == self.color:    
                    validMoves.append(move_iterator)
                elif self.whose_turn != self.color:
                    validMoves.append(move_iterator)
                
                position_x += x_iterator
                position_y += y_iterator
                
                move_iterator = (position_x, position_y)
                result = self.check_piece_list(move_iterator, opposing_color)
            result = self.check_piece_list(move_iterator, opposing_color)
            if result is "capture":
                if self.whose_turn == self.color and self.save_king_by_capture(move_iterator):    
                    validMoves.append(move_iterator)
                elif self.whose_turn != self.color:
                    validMoves.append(move_iterator)
            elif result is "king":
                self.is_checking = True
                if self.whose_turn == self.color:    
                    validMoves.append(move_iterator)
                elif self.whose_turn != self.color:
                    validMoves.append(move_iterator)            
        
        # Now we have all the valid moves
        # validMoves[(position of the move)]
        return validMoves       