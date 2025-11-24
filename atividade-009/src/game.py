import random
import sys
from dataclasses import dataclass

import pygame as pg

import config as C
from systems import World
from utils import text


@dataclass
class Scene:
    name: str


class Game:
    def __init__(self):
        pg.init()

        # Set the random seed
        if C.RANDOM_SEED is not None:
            random.seed(C.RANDOM_SEED)

        # Screen setup
        self.screen = pg.display.set_mode((C.WIDTH, C.HEIGHT))
        pg.display.set_caption("Asteroids")

        # Clock and fonts
        self.clock = pg.time.Clock()
        self.font = pg.font.SysFont("consolas", 20)
        self.big = pg.font.SysFont("consolas", 48)

        # Scene control
        self.scene = Scene("menu")

        # Game world
        self.world = World()

    def run(self):
        while True:
            dt = self.clock.tick(C.FPS) / 1000.0

            # Process events
            for e in pg.event.get():
                if e.type == pg.QUIT:
                    pg.quit()
                    sys.exit(0)

                if e.type == pg.KEYDOWN and e.key == pg.K_ESCAPE:
                    pg.quit()
                    sys.exit(0)

                if self.scene.name == "play":
                    # Fire shot
                    if e.type == pg.KEYDOWN and e.key == pg.K_SPACE:
                        self.world.try_fire()

                        # Play shooting sound
                        sounds.sound_shot.play()  # play shot sound

                    # Hyperspace
                    if e.type == pg.KEYDOWN and e.key == pg.K_LSHIFT:
                        self.world.hyperspace()

                elif self.scene.name == "menu":
                    # Start game
                    if e.type == pg.KEYDOWN:
                        self.scene = Scene("play")

            keys = pg.key.get_pressed()
            self.screen.fill(C.BLACK)

            # Draw scenes
            if self.scene.name == "menu":
                self.draw_menu()
            elif self.scene.name == "play":
                self.world.update(dt, keys)
                self.world.draw(self.screen, self.font)

            pg.display.flip()

    def draw_menu(self):
        # Draw main menu
        text(self.screen, self.big, "ASTEROIDS",
             C.WIDTH // 2 - 150, 180)

        text(self.screen, self.font,
             "Arrows: turn/accelerate  Space: shoot  Shift: hyperspace",
             160, 300)

        text(self.screen, self.font,
             "Press any key to start...", 260, 360)
