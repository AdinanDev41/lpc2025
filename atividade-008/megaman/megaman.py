import pygame
import os
import sys

# Initialize Pygame
pygame.init()

# Screen setup
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Megaman 1")

# Clock setup
clock = pygame.time.Clock()


# Function to load all images from a folder
def load_images_from_folder(folder_path):
    images = []
    for filename in sorted(os.listdir(folder_path)):
        if filename.endswith(".png"):
            path = os.path.join(folder_path, filename)
            image = pygame.image.load(path).convert_alpha()
            images.append(image)
    return images


# Get absolute path for assets folder
ASSETS_PATH = os.path.join(os.path.dirname(__file__), "assets")

# Load background image
background_path = os.path.join(ASSETS_PATH, "screen", "fundo_megaman.png")
background = pygame.image.load(background_path).convert()
background = pygame.transform.scale(background, (WIDTH, HEIGHT))

# Load animations
animations = {
    "stop": load_images_from_folder(os.path.join(ASSETS_PATH, "stop")),
    "run": load_images_from_folder(os.path.join(ASSETS_PATH, "run")),
    "shoot": load_images_from_folder(os.path.join(ASSETS_PATH, "shoot")),
    "jump": load_images_from_folder(os.path.join(ASSETS_PATH, "jump")),
}

# Player variables
action = "stop"
frame_index = 0
player_x = 200
player_y = 310
speed = 7
facing_right = True

# Jump variables
is_jumping = False
jump_speed = -15
gravity = 1
vertical_velocity = 0
ground_y = 310


# Main loop
running = True
while running:
    # Draw background
    screen.blit(background, (0, 0))

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Key handling
    keys = pygame.key.get_pressed()

    moving = False

    # Movement logic
    if keys[pygame.K_RIGHT]:
        player_x += speed
        facing_right = True
        moving = True
    if keys[pygame.K_LEFT]:
        player_x -= speed
        facing_right = False
        moving = True

    # Jumping logic
    if not is_jumping:
        if keys[pygame.K_SPACE]:
            is_jumping = True
            vertical_velocity = jump_speed
    else:
        vertical_velocity += gravity
        player_y += vertical_velocity

        # Stop falling when reaching the ground
        if player_y >= ground_y:
            player_y = ground_y
            is_jumping = False

    # Action selection
    if is_jumping:
        action = "jump"
    elif keys[pygame.K_z]:
        action = "shoot"
    elif moving:
        action = "run"
    else:
        action = "stop"

    # Update animation frame
    frames = animations[action]
    frame_index += 0.3
    if frame_index >= len(frames):
        frame_index = 0

    current_image = frames[int(frame_index)]

    # Flip image when facing left
    if not facing_right:
        current_image = pygame.transform.flip(current_image, True, False)

    # Draw player
    screen.blit(current_image, (player_x, player_y))

    # Update screen
    pygame.display.flip()
    clock.tick(30)

pygame.quit()
sys.exit()
