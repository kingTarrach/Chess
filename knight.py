from piece import ChessPiece

class Knight(ChessPiece):
    
    def __init__(self, color, position, size, game_surface, board_offset_x, board_offset_y, block_size):
        super().__init__(color, position, size, game_surface, board_offset_x, board_offset_y, block_size)
        self.piece_type = "knight"
        self.image = self.load_image_by_width()
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
        
        direction_x = 1
        direction_y = 1
        
        for i in range(0, 4):
            position_x = self.position[0]
            position_y = self.position[1]
            if i is 1:
                direction_x = -1
            elif i is 2:
                direction_y = -1
            elif i is 3:
                direction_x = 1
            position_x += (2 * direction_x)
            position_y += (1 * direction_y)
            move_iterator = (position_x, position_y)
            result = self.check_piece_list(move_iterator, opposing_color)
            if self.check_boundaries(move_iterator) and result in ["valid", "capture", "king"]:
                if result == "king":
                    self.is_checking = True
                if self.whose_turn == self.color and self.save_king_by_capture(move_iterator):    
                    validMoves.append(move_iterator)
                elif self.whose_turn != self.color:
                    validMoves.append(move_iterator)
        
        direction_x = 1
        direction_y = 1
        
        for i in range(0, 4):
            position_x = self.position[0]
            position_y = self.position[1]
            if i is 1:
                direction_x = -1
            elif i is 2:
                direction_y = -1
            elif i is 3:
                direction_x = 1
            position_x += (1 * direction_x)
            position_y += (2 * direction_y)
            move_iterator = (position_x, position_y)
            result = self.check_piece_list(move_iterator, opposing_color)
            if self.check_boundaries(move_iterator) and result in ["valid", "capture", "king"]:
                if result == "king":
                    self.is_checking = True
                if self.whose_turn == self.color and self.save_king_by_capture(move_iterator):    
                    validMoves.append(move_iterator)
                elif self.whose_turn != self.color:
                    validMoves.append(move_iterator)
        
        return validMoves
    
    