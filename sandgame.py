import pygame
import sys
import random

pygame.init()
width, height = 800, 800
screen = pygame.display.set_mode((width, height))
grid_size = 0
cell_size = 13
grid_width = 1  # Specify the width of the grid lines
fall_speed = 5  # Specify the speed of the descent
running = True     
clock = pygame.time.Clock()

pygame.display.set_caption("Pygame Example")

blocks = []
falling_enabled = False

def draw_grid(blocks):
    for block in blocks:
        pygame.draw.rect(screen, block[1], block[0])

    # Draw vertical grid lines
    for x in range(0, width, cell_size):
        pygame.draw.line(screen, (255, 255, 255), (x, 0), (x, height), grid_width)

    # Draw horizontal grid lines
    for y in range(0, height, cell_size):
        pygame.draw.line(screen, (255, 255, 255), (0, y), (width, y), grid_width)

# def add_block(x, y, color):
#     rect = pygame.Rect(x, y, cell_size, cell_size)
#     blocks.append((rect, color))
max_blocks = 1000 # Set your desired limit

def add_block(x, y, color):
    rect = pygame.Rect(x, y, cell_size, cell_size)
    blocks.append((rect, color))

    # Limit the number of blocks
    if len(blocks) > max_blocks:
        blocks.pop(0)


def move_blocks_down():
    for i in range(len(blocks)):
        block = blocks[i]
        new_position = block[0].move(0, cell_size)

        # Check if the new position is within the height of the screen
        if new_position.y + cell_size <= height:
            # Check for collisions with other blocks
            if not any(new_position.colliderect(other_block[0]) for other_block in blocks[:i]):
                # Check if the new position is within the width of the screen
                if 0 <= new_position.x < width:
                    blocks[i] = (new_position, block[1])
            else:

                # Find adjacent positions
                left_position = pygame.Rect(new_position.x - cell_size, new_position.y, cell_size, cell_size)
                right_position = pygame.Rect(new_position.x + cell_size, new_position.y, cell_size, cell_size)

                # Check if left position is empty and within the width of the screen
                if not any(left_position.colliderect(other_block[0]) for other_block in blocks) and 0 <= left_position.x < width:
                    blocks[i] = (left_position, block[1])
                # Check if right position is empty and within the width of the screen
                elif not any(right_position.colliderect(other_block[0]) for other_block in blocks) and 0 <= right_position.x < width:
                    blocks[i] = (right_position, block[1])
                # If both left and right positions are occupied, stack up above the existing block
                else:
                    blocks[i] = (new_position.move(0, -cell_size), block[1])



# Main game loop
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    x, y = pygame.mouse.get_pos()

    # Check if the left mouse button is pressed
    if pygame.mouse.get_pressed()[0]:
        # Increment the hue value over time
        hue = (pygame.time.get_ticks() // 10) % 360  # 10 is a speed factor, adjust as needed
        color = pygame.Color(0)
        color.hsla = (hue, 100, 50, 100)  # Hue, Saturation, Lightness, Alpha
        clicked_block = (pygame.Rect((x // cell_size) * cell_size, (y // cell_size) * cell_size, cell_size, cell_size), color)
        add_block(clicked_block[0].x, clicked_block[0].y, clicked_block[1])

    screen.fill((0, 0, 0))
    move_blocks_down()
    draw_grid(blocks)

    pygame.display.flip()
    clock.tick(60)
