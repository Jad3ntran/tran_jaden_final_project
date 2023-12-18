# sprites.py

import pygame as pg
import os
import random
from settings import *

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
        self.preview_color = None  # Variable to store the color of the preview ball

    def update(self):
        self.acc = pg.Vector2(0, 0)
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

        # Update the color of the player's image to reflect the color of the ball
        if self.preview_color:
            self.image = pg.image.load(os.path.join(img_folder, f'basketball_{self.preview_color}.png')).convert()
            self.image.set_colorkey(WHITE)

    def handle_shot_result(self):
        if self.game.shot_effect == "time":
            self.game.shot_time += 5  # Add 5 seconds to the shot time

        # Set the color of the preview ball
        self.preview_color = self.get_random_color()

        # Create a new basketball with the color
        ball = Basketball(self.game, self.rect.center, pg.Vector2(0, -10), color=self.preview_color)
        self.game.all_sprites.add(ball)

        # Kill the player to remove it from the screen
        self.kill()

class Hoop(pg.sprite.Sprite):
    def __init__(self, game):
        pg.sprite.Sprite.__init__(self)
        self.game = game
        self.image = pg.image.load(os.path.join(img_folder, 'hoop.png')).convert()
        self.image.set_colorkey(WHITE)
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH - 50, HEIGHT / 4)  # Adjust the coordinates as needed
        self.speed = 8  # Speed of the hoop's vertical movement

    def update(self):
        self.rect.y += self.speed

        # Reverse the direction when the hoop reaches the top or bottom
        if self.rect.bottom > HEIGHT or self.rect.top < 0:
            self.speed = -self.speed

class Basketball(pg.sprite.Sprite):
    def __init__(self, game, pos, velocity, color=None):
        pg.sprite.Sprite.__init__(self)
        self.game = game
        self.pos = pg.Vector2(pos)
        self.velocity = velocity
        self.color = color if color else self.get_random_color()

        # Load the image and set a color key
        self.image = self.get_ball_image()
        self.image.set_colorkey(WHITE)  # Set the color key to the specified color
        self.rect = self.image.get_rect()
        self.rect.center = pos

    def update(self):
        self.pos += self.velocity * self.game.dt
        self.rect.center = self.pos

        # Check if the basketball collides with any hoop
        for hoop in self.game.hoops:
            if self.rect.colliderect(hoop.rect):
                self.handle_collision_with_hoop(hoop)
                break  # Break to handle collision with only one hoop

        # Check if the basketball is below the screen
        if self.rect.top > HEIGHT or self.rect.right < 0 or self.rect.left > WIDTH:
            self.handle_missed_shot()

    def handle_collision_with_hoop(self, hoop):
        # Handle scoring logic and effects based on ball color
        if self.color == "blue":
            self.game.shot_time += 5  # Add 5 seconds to the shot time
            self.game.score += 2  # Add 2 points to the score
        elif self.color == "red":
            self.game.score += 5  # Add 5 points to the score (extra points)
        elif self.color == "regular":
            self.game.score += 2  # Add 2 points to the score for a regular basketball
            print("Regular basketball collided with hoop")  # Add this line for debugging

        self.change_color()
        self.image = self.get_ball_image()
        self.image.set_colorkey(WHITE)  # Set the color key to the specified color
        self.rect = self.image.get_rect()  # Update the rect to the new image
        self.kill()  # Remove the basketball from the screen

    def handle_missed_shot(self):
        # Handle losing points for a missed shot
        if self.color == "regular":
            self.game.score -= 2  # Lose 5 points for missing the hoop with a regular ball
            print("Missed shot with regular ball")  # Add this line for debugging
        elif self.color in ["blue", "red"]:
            self.game.score -= 5  # Lose 2 points for missing the hoop with a colored ball
            print("Missed shot with colored ball")  # Add this line for debugging

        self.kill()  # Remove the basketball from the screen

    def change_color(self):
        # Randomly choose a color for the ball
        self.color = self.get_random_color()

    def get_random_color(self):
        # Get a random color for the ball
        colors = ["blue", "red", "regular", "regular", "regular"]
        return random.choice(colors)

    def get_ball_image(self):
        # Get the basketball image based on its color
        return pg.image.load(os.path.join(img_folder, f'basketball_{self.color}.png')).convert()
