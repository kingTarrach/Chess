import pygame, sys, os

def draw_game(game_surface, block_size, board_offset_x, board_offset_y):
    
    pygame.init()
    
    # Set values for light squares and dark squares
    color_light = (232, 235, 239)
    color_dark = (125, 135, 150)

    # Draw the board
    for i in range(8):  # Row
        for j in range(8):  # Column
            # Alternate colors
            rect_color = color_dark if (i + j) % 2 == 0 else color_light
            pygame.draw.rect(game_surface, rect_color, pygame.Rect(j * block_size + board_offset_x, i * block_size + board_offset_y, block_size, block_size))
    



    
