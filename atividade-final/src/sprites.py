import math
from pathlib import Path
from random import uniform
from typing import Optional

import pygame as pg
from pygame.joystick import Joystick

import config as C
import sounds
from utils import Vec, wrap_pos, draw_circle, angle_to_vec


BASE_PATH = Path(__file__).resolve().parent
ASSETS_PATH = BASE_PATH.parent / "assets"


def load_sprite(filename: str, scale: float = 1.0) -> pg.Surface:
    # Loads a PNG sprite and scales it.
    path = ASSETS_PATH / filename

    try:
        image = pg.image.load(path).convert_alpha()
    except FileNotFoundError:
        print(f"[WARN] Sprite '{filename}' not found at '{path}'")
        image = pg.Surface((32, 32), pg.SRCALPHA)
        pg.draw.rect(image, (255, 0, 255), image.get_rect(), 1)

    if scale != 1.0:
        width, height = image.get_size()
        image = pg.transform.smoothscale(
            image, (int(width * scale), int(height * scale))
        )

    return image


class Bullet(pg.sprite.Sprite):
    def __init__(self, pos: Vec, vel: Vec, is_player: bool = False) -> None:
        # Represents a projectile (player or UFO).
        super().__init__()
        self.pos = Vec(pos)
        self.vel = Vec(vel)
        self.is_player = is_player
        self.ttl = C.BULLET_TTL
        self.r = C.BULLET_RADIUS

        size = self.r * 2
        self.rect = pg.Rect(0, 0, size, size)
        self.rect.center = (int(self.pos.x), int(self.pos.y))

    def update(self, dt: float) -> None:
        # Moves bullet and decreases lifetime.
        self.pos += self.vel * dt
        self.pos = wrap_pos(self.pos)
        self.ttl -= dt

        if self.ttl <= 0:
            self.kill()

        self.rect.center = (int(self.pos.x), int(self.pos.y))

    def draw(self, surface: pg.Surface) -> None:
        # Player bullet = blue, enemy bullet = red.
        color = (80, 180, 255) if self.is_player else (255, 60, 60)
        pg.draw.circle(surface, color,
                       (int(self.pos.x), int(self.pos.y)), self.r)


class Asteroid(pg.sprite.Sprite):
    def __init__(self, pos: Vec, vel: Vec, size: str) -> None:
        # Asteroid with irregular polygon shape.
        super().__init__()
        self.pos = Vec(pos)
        self.vel = Vec(vel)
        self.size = size
        self.r = C.AST_SIZES[size]["r"]

        self.points = self._make_points()
        size_px = self.r * 2
        self.rect = pg.Rect(0, 0, size_px, size_px)
        self.rect.center = (int(self.pos.x), int(self.pos.y))

    def _make_points(self) -> list[Vec]:
        # Generates asteroid polygon points.
        if self.size == "L":
            step_count = 10
        elif self.size == "M":
            step_count = 8
        else:
            step_count = 6

        points: list[Vec] = []
        for i in range(step_count):
            angle = i * 360 / step_count
            jitter = uniform(0.7, 1.3)
            radius = self.r * jitter
            rad = math.radians(angle)
            vec = Vec(math.cos(rad), math.sin(rad)) * radius
            points.append(vec)

        return points

    def update(self, dt: float) -> None:
        # Asteroid drift + wrap.
        self.pos += self.vel * dt
        self.pos = wrap_pos(self.pos)
        self.rect.center = (int(self.pos.x), int(self.pos.y))

    def draw(self, surface: pg.Surface) -> None:
        # Draw asteroid polygon.
        world_points = [self.pos + p for p in self.points]
        pg.draw.polygon(surface, C.WHITE, world_points, 1)


class UFO(pg.sprite.Sprite):
    def __init__(self, pos: Vec, vel: Vec) -> None:
        # Enemy UFO using PNG sprite.
        super().__init__()
        self.pos = Vec(pos)
        self.vel = Vec(vel)
        self.r = C.UFO_RADIUS

        self.base_image = load_sprite("enemy.png", scale=0.1)
        self.image = self.base_image
        self.rect = self.image.get_rect(center=(int(self.pos.x),
                                                int(self.pos.y)))

        self.shoot_timer = uniform(0.5, 2.0)

        # Looping UFO engine sound.
        self.channel = pg.mixer.find_channel()
        if self.channel is not None:
            self.channel.play(sounds.FLY_NAVE, loops=-1)

    def update(self, dt: float) -> None:
        # Moves UFO and cooldown.
        self.pos += self.vel * dt
        self.pos = wrap_pos(self.pos)
        self.rect.center = (int(self.pos.x), int(self.pos.y))

        if self.shoot_timer > 0:
            self.shoot_timer -= dt

    def fire(self) -> Optional["Bullet"]:
        # Fires a bullet in a random direction.
        if self.shoot_timer > 0:
            return None

        self.shoot_timer = C.UFO_FIRE_RATE
        angle = uniform(0, 360)
        direction = angle_to_vec(angle)
        pos = self.pos + direction * (self.r + 4)
        vel = direction * C.UFO_BULLET_SPEED

        return Bullet(pos, vel, is_player=False)

    def draw(self, surface: pg.Surface) -> None:
        # Draw UFO sprite.
        surface.blit(self.image, self.image.get_rect(center=self.pos))

    def kill(self) -> None:
        # Stop sound on death.
        if getattr(self, "channel", None) is not None:
            self.channel.stop()
        super().kill()


class Ship(pg.sprite.Sprite):
    def __init__(self, pos: Vec) -> None:
        # Player spaceship using PNG sprite.
        super().__init__()
        self.pos = Vec(pos)
        self.vel = Vec(0, 0)
        self.angle = -90.0
        self.cooldown = 0.0
        self.invulnerable = 0.0
        self.alive = True
        self.r = C.SHIP_RADIUS

        self.base_image = load_sprite("player.png", scale=0.07)
        self.image = self.base_image
        self.rect = self.image.get_rect(center=(int(self.pos.x),
                                                int(self.pos.y)))

    def control(
        self,
        keys: pg.key.ScancodeWrapper,
        dt: float,
        joystick: Optional[Joystick] = None,
    ) -> None:
        # Handles keyboard/joystick input.
        if keys[pg.K_LEFT]:
            self.angle -= C.SHIP_TURN_SPEED * dt
        if keys[pg.K_RIGHT]:
            self.angle += C.SHIP_TURN_SPEED * dt
        if keys[pg.K_UP]:
            self.vel += angle_to_vec(self.angle) * C.SHIP_THRUST * dt

        if joystick is not None:
            deadzone = 0.15
            axis_x = joystick.get_axis(0)

            if abs(axis_x) > deadzone:
                self.angle += axis_x * C.SHIP_TURN_SPEED * dt

            try:
                rt_value = joystick.get_axis(5)
            except IndexError:
                rt_value = -1.0

            if rt_value > -0.8:
                power = (rt_value + 1.0) / 2.0
                self.vel += (
                    angle_to_vec(self.angle)
                    * C.SHIP_THRUST
                    * dt
                    * power
                )

        self.vel *= C.SHIP_FRICTION

    def fire(self) -> Optional["Bullet"]:
        # Creates a blue bullet if cooldown is ready.
        if self.cooldown > 0:
            return None

        direction = angle_to_vec(self.angle)
        pos = self.pos + direction * (self.r + 6)
        vel = self.vel + direction * C.SHIP_BULLET_SPEED

        bullet = Bullet(pos, vel, is_player=True)
        self.cooldown = C.SHIP_FIRE_RATE

        return bullet

    def hyperspace(self) -> None:
        # Teleports the ship and activates shield.
        self.pos = Vec(
            uniform(0, C.WIDTH),
            uniform(0, C.HEIGHT),
        )
        self.vel.xy = (0, 0)
        self.invulnerable = 1.0

    def update(self, dt: float) -> None:
        # Updates cooldown, movement, wrapping.
        if self.cooldown > 0:
            self.cooldown -= dt
        if self.invulnerable > 0:
            self.invulnerable -= dt

        self.pos += self.vel * dt
        self.pos = wrap_pos(self.pos)
        self.rect.center = (int(self.pos.x), int(self.pos.y))

    def draw(self, surface: pg.Surface) -> None:
        # Draw rotated ship and shield effect.
        rotated = pg.transform.rotate(self.base_image, -self.angle - 90)
        rect = rotated.get_rect(center=self.pos)
        surface.blit(rotated, rect)

        if self.invulnerable > 0 and int(self.invulnerable * 10) % 2 == 0:
            draw_circle(surface, self.pos, self.r + 6)
