import pygame as pg
from pygame.sprite import Sprite
import random
from random import randint
from pygame.math import Vector2 as vec
import os
from settings import *
from settings import *
from math import floor

# setup asset folders here - images sounds etc.
game_folder = os.path.dirname(__file__)
img_folder = os.path.join(game_folder, 'images')


class Player(pg.sprite.Sprite):
    def __init__(self, game):
        pg.sprite.Sprite.__init__(self)
        self.game = game
        self.image = pg.image.load(os.path.join(img_folder, 'basketball.png')).convert()
        self.image.set_colorkey(WHITE)
        self.rect = self.image.get_rect()
        self.rect.center = (0, 0)
        self.pos = pg.Vector2(WIDTH / 2, HEIGHT / 2)
        self.vel = pg.Vector2(0, 0)
        self.acc = pg.Vector2(0, 0)

    def update(self):
        self.acc = pg.Vector2(0, 0.5)
        keys = pg.key.get_pressed()
        if keys[pg.K_LEFT]:
            self.acc.x = -PLAYER_ACC
        if keys[pg.K_RIGHT]:
            self.acc.x = PLAYER_ACC

        # Apply friction
        self.acc.x += self.vel.x * PLAYER_FRIC

        # Equations of motion
        self.vel += self.acc * self.game.dt
        self.pos += self.vel * self.game.dt + 0.5 * self.acc * self.game.dt ** 2

        # Wrap around the screen
        if self.pos.x > WIDTH:
            self.pos.x = 0

        self.rect.center = self.pos

        # Check if the basketball reaches the top
        if self.rect.bottom < 0:
            self.handle_shot_result()

    def handle_shot_result(self):
        if self.game.shot_effect == "time":
            self.game.shot_time += 5  # Add 5 seconds to the shot time
        elif self.game.shot_effect == "points":
            self.game.score += 2  # Add 2 points to the score

        self.kill()  # Remove the basketball from the screen

class Basketball(pg.sprite.Sprite):
    def __init__(self, game, pos, velocity):
        pg.sprite.Sprite.__init__(self)
        self.game = game
        self.image = pg.image.load(os.path.join(img_folder, 'basketball.png')).convert()
        self.image.set_colorkey(WHITE)
        self.rect = self.image.get_rect()
        self.rect.center = pos
        self.pos = pg.Vector2(pos)
        self.velocity = velocity

    def update(self):
        self.pos += self.velocity * self.game.dt
        self.rect.center = self.pos

class Hoop(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        pg.sprite.Sprite.__init__(self)
        self.game = game
        self.image = pg.Surface((50, 50))
        self.image.fill(RED)  # You can replace RED with the color you want for the hoop
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

