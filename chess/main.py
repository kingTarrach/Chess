
#!/usr/bin/env python3

from visuals import *
from game_logic import *
from piece_logic import *
from piece import ChessPiece
import time
     
        
def main():
    
    # Initialize the pygame library to allow for visuals
    pygame.init()
    
    # Initialize crucial variables
    block_size = 100
    piece_overall_size = block_size * .7
    
    board_offset_x = block_size * 3
    board_offset_y = block_size / 2
    
    screen_width = board_offset_x + (block_size * 8) + board_offset_x
    screen_height = board_offset_y + (block_size * 8) + board_offset_y
    game_surface = pygame.display.set_mode((screen_width, screen_height))
    
    board_matrix = initializeBoardMatrix()   
    
    # Initialize game world

    draw_game(game_surface, block_size, board_offset_x, board_offset_y)
    
    #pieces = standard_chess_setup(piece_overall_size, game_surface, board_offset, block_size)
    pieces = standard_chess_setup(piece_overall_size, game_surface, board_offset_x, board_offset_y, block_size)
    
    whose_turn = "white"
    white_pieces = []
    black_pieces = []
    
    for piece in pieces:
        if piece.color == "white":
            white_pieces.append(piece)
        elif piece.color == "black":
            black_pieces.append(piece)
    
    calculate_piece_moves(white_pieces, black_pieces, whose_turn)
            
    running = True
    selected_piece = None
    whose_turn = "white"
    change_turn = False
    delete_piece = False
    check_color = None
    checkmate_color = None
    
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:

                # Handles mouse clicks
                # Get mouse position
                
                mouse_x, mouse_y = event.pos    
                mouse_position = convert_coords_to_position((mouse_x, mouse_y), block_size, board_offset_x, board_offset_y)  
                                 
                change_turn = False
                delete_piece = None
                
                # If the location is the location of a piece
                if (detect_location(pieces, mouse_position)):
                    
                    piece = find_piece(pieces, mouse_position)         # Set piece to the piece on location of the mouse click
                    # If selected_piece is none, select the piece and don't change the turn
                    if selected_piece is None and piece.get_color() == whose_turn:
                        
                        if check_color != piece.get_color():
                            selected_piece = select_piece(piece)
                        else:
                            selected_piece = piece
                            piece.show_valid_moves()
                            
                    # If the color of the piece is the same and the piece is not selected, change selected piece to the piece
                    elif piece.get_color() == whose_turn and piece is not selected_piece and selected_piece:
                        
                        selected_piece.delete_valid_moves()
                        if check_color != piece.get_color():
                            selected_piece = select_piece(piece)
                        else:
                            selected_piece = piece
                            piece.show_valid_moves()
                            
                    # If the color is the opposite of whose turn it is
                    elif piece.get_color() != whose_turn and selected_piece:      # If there is a piece selected right now  
                            
                        for move_position in selected_piece.valid_moves:
                            
                            # If the piece has a valid capture
                            if move_position == piece.get_position():
                                
                                piece.erase_piece()            # Delete the physical piece off the screen 
                                selected_piece.move(move_position)
                                print(selected_piece.color + " " + selected_piece.piece_type + " to position: " + str(selected_piece.position))
                                delete_piece = piece
                                change_turn = True
                                
                                break
                            
                # If the position of the mouse is on an open square
                elif (not detect_location(pieces, mouse_position)):
                    
                    if selected_piece:
                        
                        for move_position in selected_piece.valid_moves:
                            
                            if move_position == mouse_position:
                                
                                # Remove piece's current position
                                selected_piece.move(move_position)
                                print(selected_piece.color + " " + selected_piece.piece_type + " to position: " + str(selected_piece.position))
                                # Add piece's new position to the end of the list
                                change_turn = True
                                
                                break
                            
                        
                # If a piece gets captured, delete its instance from the pieces list and call its destructor
                if delete_piece:
                    print(selected_piece.color + " captures the " + delete_piece.color + " " + delete_piece.piece_type + ".")
                    pieces.remove(delete_piece)
                    del delete_piece
                    for piece in pieces:
                        piece.set_piece_list(pieces)
                    
                if change_turn:     # Can only change turn if a move occurs
                    print()
                    
                    # Change whose turn it is first
                    if whose_turn == "white":
                        whose_turn = "black"
                        
                    elif whose_turn == "black":
                        whose_turn = "white"
                    change_whose_turn(pieces, whose_turn)
                    
                    remove_all_moves(pieces)
                    for piece in pieces:
                        if piece.color == "white":
                            white_pieces.append(piece)
                        elif piece.color == "black":
                            black_pieces.append(piece)
                    # First calculate all the new moves now that a piece has moved
                    calculate_piece_moves(white_pieces, black_pieces, whose_turn)
                                        
                    check_color = is_check(pieces, whose_turn)
                    if check_color:
                        print("Check for " + check_color)
                        #pieces = check_protocol(pieces, check_color) 
                        checkmate_color = check_for_checkmate(check_color, pieces)     
                    
                    if checkmate_color:
                        print("Checkmate for " + checkmate_color)
                    
                    selected_piece = None
                    print_all_moves(pieces)
                        
                    
        pygame.display.update()
    
    pygame.quit()
    sys.exit()
    
    
    
if __name__ == "__main__":
    main()