import pygame

pygame.init()
#hum
# Define some colors
WHITE = (255, 255, 255)
DARKBLUE = (36, 90, 190)
LIGHTBLUE = (0, 176, 240)
RED = (255, 0, 0)
ORANGE = (255, 100, 0)
YELLOW = (255, 255, 0)
COLOR_BLACK = (0, 0, 0)

# Screen
size = (1280, 720)
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Breakout - PyGame Edition")


# Main Loop
game_loop = True
clock = pygame.time.Clock()

while game_loop:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_loop = False

    # background color of her
    screen.fill(COLOR_BLACK)

    # update the screen
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
