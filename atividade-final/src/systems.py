import math
from random import uniform
import pygame as pg

import config as C
import sounds
from sprites import Asteroid, Ship, UFO
from utils import Vec, rand_edge_pos, text

class World:
    def __init__(self) -> None:
        self.ship = Ship(Vec(C.WIDTH / 2, C.HEIGHT / 2))
        self.bullets = pg.sprite.Group()
        self.enemy_bullets = pg.sprite.Group()
        self.asteroids = pg.sprite.Group()
        self.ufos = pg.sprite.Group()
        self.all_sprites = pg.sprite.Group()
        self.all_sprites.add(self.ship)

        self.lives = C.START_LIVES
        self.wave = 0
        self.wave_cool = C.WAVE_DELAY
        self.safe = C.SAFE_SPAWN_TIME

        self.start_wave()

    def start_wave(self) -> None:
        """Inicia uma nova rodada."""
        self.wave += 1
        
        # Dificuldade
        num_enemies = C.BASE_ENEMIES + (self.wave - 1) * C.ENEMIES_INC
        current_speed = C.BASE_SPEED + (self.wave - 1) * C.SPEED_INC
        
        print(f"--- WAVE {self.wave} --- Inimigos: {num_enemies} | Velocidade: {current_speed}")

        for _ in range(num_enemies):
            pos = rand_edge_pos()
            # Evita nascer em cima do player
            while self.ship.alive and (pos - self.ship.pos).length() < 200:
                pos = rand_edge_pos()

            # Calcula direção Kamikaze
            target = self.ship.pos if self.ship.alive else Vec(C.WIDTH/2, C.HEIGHT/2)
            direction = (target - pos)
            if direction.length() > 0:
                direction = direction.normalize()
            else:
                direction = Vec(1, 0)

            # 30% UFO, 70% Asteroide
            if uniform(0, 1) < 0.3:
                vel = direction * (current_speed + 20)
                ufo = UFO(pos, vel)
                self.ufos.add(ufo)
                self.all_sprites.add(ufo)
            else:
                direction = direction.rotate(uniform(-10, 10))
                vel = direction * current_speed
                # Todos nascem tamanho "L" mas não se dividem mais
                self.spawn_asteroid(pos, vel, "L")

    def spawn_asteroid(self, pos: Vec, vel: Vec, size: str) -> None:
        asteroid = Asteroid(pos, vel, size)
        self.asteroids.add(asteroid)
        self.all_sprites.add(asteroid)

    def try_fire(self) -> None:
        if len(self.bullets) >= C.MAX_BULLETS:
            return
        bullet = self.ship.fire()
        if bullet is None:
            return
        self.bullets.add(bullet)
        self.all_sprites.add(bullet)
        sounds.SHOT.play()

    def hyperspace(self) -> None:
        if not self.ship.alive:
            return
        self.ship.pos.xy = (uniform(0, C.WIDTH), uniform(0, C.HEIGHT))
        self.ship.vel.xy = (0, 0)

    def update(self, dt: float, keys: pg.key.ScancodeWrapper, joystick: pg.joystick.Joystick = None) -> None:
        self.ship.control(keys, dt, joystick)
        
        if joystick and self.ship.alive:
            if joystick.get_button(0): 
                self.try_fire()

        self.all_sprites.update(dt)
        
        for ufo in self.ufos:
            bullet = ufo.fire()
            if bullet:
                self.enemy_bullets.add(bullet)
                self.all_sprites.add(bullet)

        if self.safe > 0:
            self.safe -= dt
            self.ship.invuln = 0.5
        else:
            self.ship.invuln = max(self.ship.invuln - dt, 0.0)

        self.handle_collisions()

        # Checa se acabou a rodada
        enemies_alive = len(self.asteroids) + len(self.ufos)
        if enemies_alive == 0:
            if self.wave_cool > 0:
                self.wave_cool -= dt
            else:
                self.start_wave()
                self.wave_cool = C.WAVE_DELAY

    def handle_collisions(self) -> None:
        # Tiros vs Asteroides
        hits = pg.sprite.groupcollide(
            self.asteroids, self.bullets, False, True,
            collided=lambda a, b: (a.pos - b.pos).length() < a.r
        )
        for asteroid, _ in hits.items():
            self.split_asteroid(asteroid)

        # Tiros vs UFOs
        ufo_hits = pg.sprite.groupcollide(
            self.ufos, self.bullets, True, True,
            collided=lambda u, b: (u.pos - b.pos).length() < u.r
        )
        for ufo, _ in ufo_hits.items():
            if hasattr(ufo, "channel") and ufo.channel:
                ufo.channel.stop()
            sounds.BREAK_MEDIUM.play()

        # Player colide
        if self.ship.alive and self.ship.invuln <= 0 and self.safe <= 0:
            for asteroid in self.asteroids:
                if (asteroid.pos - self.ship.pos).length() < (asteroid.r + self.ship.r):
                    self.ship_die()
                    break
            if self.ship.alive:
                for ufo in self.ufos:
                    if (ufo.pos - self.ship.pos).length() < (ufo.r + self.ship.r):
                        self.ship_die()
                        break
            if self.ship.alive:
                hits = pg.sprite.spritecollide(
                    self.ship, self.enemy_bullets, True,
                    collided=pg.sprite.collide_circle
                )
                if hits:
                    self.ship_die()

    def split_asteroid(self, asteroid: Asteroid) -> None:
        """Destroi o asteroide (SEM MULTIPLICAR)."""
        # Toca o som
        sounds.BREAK_LARGE.play()
        
        # Apenas remove o asteroide atual
        asteroid.kill()
        
        # A lógica de criar novos pedaços foi removida daqui.

    def ship_die(self) -> None:
        if not self.ship.alive:
            return
        sounds.BREAK_LARGE.play()
        self.lives -= 1
        self.ship.alive = False

        if self.lives >= 0:
            self.ship.pos.xy = (C.WIDTH / 2, C.HEIGHT / 2)
            self.ship.vel.xy = (0, 0)
            self.ship.angle = -90.0
            self.ship.invuln = C.SAFE_SPAWN_TIME
            self.safe = C.SAFE_SPAWN_TIME
            self.ship.alive = True
        else:
            self.__init__()

    def draw(self, surf: pg.Surface, font: pg.font.Font) -> None:
        for spr in self.all_sprites:
            spr.draw(surf)

        pg.draw.line(surf, (60, 60, 60), (0, 40), (C.WIDTH, 40), width=1)
        
        text(surf, font, f"ROUND {self.wave}", 10, 10, C.WHITE)
        text(surf, font, f"LIVES {self.lives}", 150, 10, C.WHITE)
        
        enemies = len(self.asteroids) + len(self.ufos)
        color = C.RED_DANGER if enemies > 0 else C.SEA_GREEN
        text(surf, font, f"ENEMIES: {enemies}", C.WIDTH - 180, 10, color)