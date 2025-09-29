import pygame
import random
import os

# Game Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 800
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
BALL_RADIUS = 10
BALL_SPEED_X = 5
BALL_SPEED_Y = 5
PADDLE_WIDTH = 100
PADDLE_HEIGHT = 20
PADDLE_SPEED = 7
FPS = 60


# Ball Class
class Ball(pygame.sprite.Sprite):
    # Represents the game ball.

    def __init__(self, x, y, radius, color, speed_x, speed_y):
        super().__init__()
        self.radius = radius
        self.image = pygame.Surface([radius * 2, radius * 2], pygame.SRCALPHA)
        pygame.draw.circle(self.image, color, (radius, radius), radius)
        self.rect = self.image.get_rect(center=(x, y))
        self.speed_x = speed_x
        self.speed_y = speed_y
        self.color = color
        self.hit_cooldown = 0  # collision delay

    def update(self):
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y

        if self.rect.left <= 0:
            self.rect.left = 0
            self.speed_x *= -1
        if self.rect.right >= SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
            self.speed_x *= -1
        if self.rect.top <= 0:
            self.rect.top = 0
            self.speed_y *= -1

        # reduce cooldown each frame
        if self.hit_cooldown > 0:
            self.hit_cooldown -= 1

    def reset_position(self, x, y,
                       speed_x=BALL_SPEED_X, speed_y=BALL_SPEED_Y):
        self.rect.center = (x, y)
        self.speed_x = speed_x if random.choice([True, False]) else -speed_x
        self.speed_y = -abs(speed_y)
        self.hit_cooldown = 0
