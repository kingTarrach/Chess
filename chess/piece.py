from abc import ABC, abstractmethod
from visuals import *

class ChessPiece(ABC):
    
    def __init__(self, color, position, size, game_surface, board_offset_x, board_offset_y, block_size):
        
        self.color = color
        self.moves = 0
        self.position = position
        self.valid_moves = None
        self.rectangles = []
        self.game_surface = game_surface
        self.board_offset_x = board_offset_x
        self.board_offset_y = board_offset_y
        self.block_size = block_size
        self.size = size
        self.is_checking = False
        self.whose_turn = "white"
        
        
    # Delete the current image on the board and place on new position
    def move(self, new_position):
        self.erase_piece()
        self.place_by_board_position(new_position)
        self.delete_valid_moves()
        self.position = new_position
        self.moves += 1
        if self.piece_type == "pawn" and (self.position[1] == 0 or self.position[1] == 7):
            # Promotion for pawn
            pass          
    
    # Given a position on the board, move the piece to that position
    def place_by_board_position(self, position):
        width, height = self.image.get_size()
        block_offset_x = (self.block_size - width) / 2
        block_offset_y = (self.block_size - height) / 2
        x = self.board_offset_x + block_offset_x + (position[0] * self.block_size)
        y = self.board_offset_y + block_offset_y + (position[1] * self.block_size)

        self.game_surface.blit(self.image, (x, y))
        self.position = position
        return (x, y)
    
    def place_rectangle_by_board_position(self, position, border, color):
        border_offset = border / 2
        x = self.board_offset_x + border_offset + (position[0] * self.block_size)
        y = self.board_offset_y + border_offset + (position[1] * self.block_size)
        rect = pygame.draw.rect(self.game_surface, color, (x, y, self.block_size - border_offset, self.block_size - border_offset), border)
        return rect
    
    def delete_rectangle_by_border_position(self, position, border):
        border_offset = border / 2
        # Set color
        
        if (position[0] + position[1]) % 2 == 0:
            color = (125, 135, 150)
        else:
            color = (232, 235, 239)
        
        x = self.board_offset_x + border_offset + (position[0] * self.block_size)
        y = self.board_offset_y + border_offset + (position[1] * self.block_size)
        pygame.draw.rect(self.game_surface, color, (x, y, self.block_size - border_offset, self.block_size - border_offset), border)
    
    # Not really used yet
    def delete_piece_by_position(self, position):
        
        if (position[0] + position[1]) % 2 == 0:
            color = (125, 135, 150)
        else:
            color = (232, 235, 239)
            
        x = self.board_offset_x + (position[0] * self.block_size)
        y = self.board_offset_y + (position[1] * self.block_size)
        pygame.draw.rect(self.game_surface, color, (x, y, self.block_size, self.block_size), 0)

    def load_image_by_height(self):
        
        # Construct the file path using os.path.join for better compatibility
        image_path = os.path.join("pieces", f"{self.color}_{self.piece_type}.png")
        try:
            # Load the image
            image = pygame.image.load(image_path).convert_alpha()  # Using convert_alpha to keep transparency
        except pygame.error as e:
            print(f"Failed to load image at {image_path}: {e}")
            return None  # Return None or raise an error

        # Scale the image while maintaining aspect ratio
        width, height = image.get_size()
        aspect_ratio = width / height
        new_width = int(self.size * aspect_ratio)
        image = pygame.transform.scale(image, (new_width, self.size))

        return image
    
    # Everything but the pawn uses this method
    def load_image_by_width(self):
        
        # Construct the file path using os.path.join for better compatibility
        image_path = os.path.join("pieces", f"{self.color}_{self.piece_type}.png")
        try:
            # Load the image
            image = pygame.image.load(image_path).convert_alpha()  # Using convert_alpha to keep transparency
        except pygame.error as e:
            print(f"Failed to load image at {image_path}: {e}")
            return None  # Return None or raise an error

        # Scale the image while maintaining aspect ratio
        width, height = image.get_size()
        aspect_ratio = height / width
        new_height = int(self.size * aspect_ratio)
        image = pygame.transform.scale(image, (self.size, new_height))

        return image
    
    @abstractmethod
    def check_for_moves(self):
        # Abstract Function
        pass
    
    def generate_moves(self):
        
        if self.get_piece_type() is not "king":
            self.valid_moves = self.check_for_moves()
        elif self.get_piece_type() is "king":
            self.valid_moves = self.check_for_king_moves()
            
    
    def recalculate_all_opposing_moves(self):
        
        king = None

        for piece in self.piece_list:
            
            if piece.color is not self.color:
                if piece.piece_type == "king":
                    king = piece
                else:
                    piece.generate_moves()
        
        if king:
            king.generate_moves()
        
        return self.piece_list
    
    def recalculate_all_moves_but_king(self):

        for piece in self.piece_list:
            
            if piece.color is not self.color:
                if piece.piece_type == "bishop":
                    print(piece.piece_type + "'s position before recalc: " + str(piece.position))
                if piece.piece_type != "king":
                    piece.generate_moves()
                if piece.piece_type == "bishop":
                    print(piece.piece_type + "'s position after recalc: " + str(piece.position))
        
        return self.piece_list
    
    def recalculate_opposing_pawn(self):
        
        for piece in self.piece_list:
            
            if piece.color is not self.color and piece.piece_type is "pawn":
                piece.generate_moves()
        
        
    
    def change_position_for_piece(self, new_position, piece_index):
        
        self.piece_list[piece_index].position = new_position
        
        for piece in self.piece_list:
            piece.set_piece_list(self.piece_list)
    
    def save_king_by_capture(self, position):
        
        original_position = self.position
        self.position = position
        captured_piece = None
        captured_index = 0
        
        for piece in self.piece_list:
            if (position == piece.get_position()):
                captured_piece = piece
                break
            captured_index += 1
        
        self.piece_list.remove(captured_piece)
        
        for piece in self.piece_list:
            piece.piece_list = self.piece_list
        
        self.recalculate_all_moves_but_king()
        
        is_not_check = self.look_for_check()
        
        self.position = original_position
        self.piece_list.insert(captured_index, captured_piece)
        for piece in self.piece_list:
            piece.set_piece_list(self.piece_list)
            
        return is_not_check
    
    def look_for_check(self):
        
        king = None
        for piece in self.piece_list:
            if piece.piece_type == "king" and piece.color == self.color:
                king = piece
                break
            
        if king is None:
            return True
        
        for piece in self.piece_list:
            if piece.get_color() is not self.color and piece.piece_type is not "king":
                for move_position in piece.valid_moves:
                    if king.get_position() == move_position:
                        return False
        
        return True             
        
    
    @abstractmethod
    def move_check_helper(self, direction_value, opposing_color, move_number):
        # Abstract function
        pass
    
    def check_piece_list(self, position, opposing_color):
        for piece in self.piece_list:
            if position == piece.get_position() and piece.get_color() is not opposing_color:
                return "invalid"
            elif position == piece.get_position() and piece.get_color() is opposing_color:
                if piece.piece_type is not "king":
                    return "capture"
                elif piece.piece_type is "king":
                    return "king"
        return "valid"    
    
    def print_all_positions(self):
        for piece in self.piece_list:
            print(piece.color + " " + piece.piece_type + "'s position: " + str(piece.position))
    
    def check_boundaries(self, position):
        if position[1] < 0 or position[1] > 7 or position[0] < 0 or position[0] > 7:
            return False
        return True
    
    # Returns a list of all the pieces it could capture
    def return_all_captures(self):
        
        captured_pieces = []
        
        for opposing_piece in self.piece_list:
            if opposing_piece.color is not self.color:
                for move in self.valid_moves:
                    if move == opposing_piece.get_position():
                        captured_pieces.append(opposing_piece)
        
        return captured_pieces
                        
    
    def set_piece_list(self, piece_list):
        self.piece_list = piece_list
    
    def show_valid_moves(self):
        for move_position in self.valid_moves:
            border = 5
            rect_color = (1, 150, 32)
            self.place_rectangle_by_board_position(move_position, border, rect_color)     
    
    def delete_valid_moves(self):
        for move_position in self.valid_moves:
            border = 5
            self.delete_rectangle_by_border_position(move_position, border)
            
    def erase_piece(self):
        if (self.position[0] + self.position[1]) % 2 == 0:
            color = (125, 135, 150)
        else:
            color = (232, 235, 239)
            
        x = self.board_offset_x + (self.position[0] * self.block_size)
        y = self.board_offset_y + (self.position[1] * self.block_size)
        pygame.draw.rect(self.game_surface, color, (x, y, self.block_size, self.block_size), 0)
    
    
    
    def get_position(self):      
        return self.position
    
    def get_color(self):
        return self.color
    
    def get_piece_type(self):
        return self.piece_type
    
    def __del__(self):
        pass
    