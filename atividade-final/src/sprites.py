import math
from random import uniform
import pygame as pg
import config as C
from utils import Vec, angle_to_vec, draw_circle, wrap_pos
import sounds

class Bullet(pg.sprite.Sprite):
    def __init__(self, pos: Vec, vel: Vec):
        super().__init__()
        self.pos = Vec(pos)
        self.vel = Vec(vel)
        self.ttl = C.BULLET_TTL
        self.r = C.BULLET_RADIUS
        self.rect = pg.Rect(0, 0, self.r * 2, self.r * 2)

    def update(self, dt: float):
        self.pos += self.vel * dt
        self.pos = wrap_pos(self.pos)
        self.ttl -= dt
        if self.ttl <= 0:
            self.kill()
        self.rect.center = self.pos

    def draw(self, surf: pg.Surface):
        draw_circle(surf, self.pos, self.r)

class Asteroid(pg.sprite.Sprite):
    def __init__(self, pos: Vec, vel: Vec, size: str):
        super().__init__()
        self.pos = Vec(pos)
        self.vel = Vec(vel)
        self.size = size
        self.r = C.AST_SIZES[size]["r"]
        self.poly = self._make_poly()
        self.rect = pg.Rect(0, 0, self.r * 2, self.r * 2)

    def _make_poly(self):
        steps = 10 if self.size == "L" else 8
        pts = []
        for i in range(steps):
            ang = i * (360 / steps)
            jitter = uniform(0.8, 1.2)
            r = self.r * jitter
            v = Vec(math.cos(math.radians(ang)), math.sin(math.radians(ang)))
            pts.append(v * r)
        return pts

    def update(self, dt: float):
        self.pos += self.vel * dt
        self.pos = wrap_pos(self.pos)
        self.rect.center = self.pos

    def draw(self, surf: pg.Surface):
        pts = [(self.pos + p) for p in self.poly]
        pg.draw.polygon(surf, C.WHITE, pts, width=1)

class UFO(pg.sprite.Sprite):
    def __init__(self, pos: Vec, vel: Vec):
        super().__init__()
        self.pos = Vec(pos)
        self.vel = Vec(vel)
        self.r = C.UFO_RADIUS
        self.rect = pg.Rect(0, 0, self.r * 2, self.r * 2)
        
        self.shoot_timer = uniform(0.5, 2.0)
        
        # Som
        self.channel = pg.mixer.find_channel()
        if self.channel is not None:
            self.channel.play(sounds.FLY_SMALL, loops=-1)

    def update(self, dt: float):
        self.pos += self.vel * dt
        self.pos = wrap_pos(self.pos)
        self.rect.center = self.pos
        if self.shoot_timer > 0:
            self.shoot_timer -= dt

    def fire(self) -> Bullet | None:
        if self.shoot_timer > 0: return None
        self.shoot_timer = C.UFO_FIRE_RATE
        # Atira em direção aleatória
        angle = uniform(0, 360)
        dirv = angle_to_vec(angle)
        spawn_pos = self.pos + dirv * (self.r + 5)
        vel = dirv * C.UFO_BULLET_SPEED
        return Bullet(spawn_pos, vel)

    def draw(self, surf: pg.Surface):
        # Desenha UFO em vermelho (Perigo)
        pg.draw.circle(surf, C.RED_DANGER, self.pos, self.r, width=2)
        pg.draw.circle(surf, C.RED_DANGER, self.pos, self.r * 0.4, width=0)

    def kill(self) -> None:
        if hasattr(self, "channel") and self.channel is not None:
            self.channel.stop()
        super().kill()

class Ship(pg.sprite.Sprite):
    def __init__(self, pos: Vec):
        super().__init__()
        self.pos = Vec(pos)
        self.vel = Vec(0, 0)
        self.angle = -90.0
        self.cool = 0.0
        self.invuln = 0.0
        self.alive = True
        self.r = C.SHIP_RADIUS
        self.rect = pg.Rect(0, 0, self.r * 2, self.r * 2)

    def control(self, keys: pg.key.ScancodeWrapper, dt: float, joystick: pg.joystick.Joystick = None):
        # --- TECLADO ---
        if keys[pg.K_LEFT]:
            self.angle -= C.SHIP_TURN_SPEED * dt
        if keys[pg.K_RIGHT]:
            self.angle += C.SHIP_TURN_SPEED * dt
        if keys[pg.K_UP]:
            self.vel += angle_to_vec(self.angle) * C.SHIP_THRUST * dt

        # --- JOYSTICK ---
        if joystick:
            DEADZONE = 0.15
            # Eixo 0: Esquerda/Direita
            axis_x = joystick.get_axis(0)
            if abs(axis_x) > DEADZONE:
                self.angle += axis_x * C.SHIP_TURN_SPEED * dt

            # Eixo 5: Gatilho Direito (RT) para acelerar
            # Normalmente RT vai de -1 (solto) a 1 (pressionado)
            try:
                rt_val = joystick.get_axis(5)
                if rt_val > -0.8: # Zona morta do gatilho
                    power = (rt_val + 1.0) / 2.0
                    self.vel += angle_to_vec(self.angle) * C.SHIP_THRUST * dt * power
            except:
                pass

        self.vel *= C.SHIP_FRICTION

    def fire(self) -> Bullet | None:
        if self.cool > 0:
            return None
        dirv = angle_to_vec(self.angle)
        pos = self.pos + dirv * (self.r + 6)
        vel = self.vel + dirv * C.SHIP_BULLET_SPEED
        self.cool = C.SHIP_FIRE_RATE
        return Bullet(pos, vel)

    def hyperspace(self):
        self.pos = Vec(uniform(0, C.WIDTH), uniform(0, C.HEIGHT))
        self.vel.xy = (0, 0)
        self.invuln = 1.0

    def update(self, dt: float):
        if self.cool > 0:
            self.cool -= dt
        if self.invuln > 0:
            self.invuln -= dt
        self.pos += self.vel * dt
        self.pos = wrap_pos(self.pos)
        self.rect.center = self.pos

    def draw(self, surf: pg.Surface):
        dirv = angle_to_vec(self.angle)
        left = angle_to_vec(self.angle + 140)
        right = angle_to_vec(self.angle - 140)
        p1 = self.pos + dirv * self.r
        p2 = self.pos + left * self.r * 0.9
        p3 = self.pos + right * self.r * 0.9
        pg.draw.polygon(surf, C.MUSTARD_YELLOW, [p1, p2, p3], width=0)
        if self.invuln > 0 and int(self.invuln * 10) % 2 == 0:
            draw_circle(surf, self.pos, self.r + 6)