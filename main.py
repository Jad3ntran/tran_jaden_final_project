# main.py
# This file was created by Jaden Tran

'''
Rules:
Goal: Score as many points as you can in the limited amount of time you have
Rules: In order to score points, you need to hit the basketball hoop that is moving up and down. The different colored balls you are able to shoot give you different benefits
Feedback: score displayed on top of the screen, as well as the amount of time you have left
Freedom: Aim wherever you want in order to score as many baskets as you can at the moving hoop
'''

# Importing necessary libraries and modules
import pygame as pg
import os
from settings import *
from sprites import *

class Game:
    def __init__(self):
        # Initialize pygame and create a window
        pg.init()
        pg.mixer.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption("My Game...")
        self.clock = pg.time.Clock()
        self.running = True
        self.paused = False
        self.player = Player(self)

        # Create a group for all sprites, including the hoop
        self.all_sprites = pg.sprite.Group()
        self.hoops = pg.sprite.Group()  # Group for hoops

        # Create instances of the Player and Hoop classes
        self.player = Player(self)
        self.hoop = Hoop(self)
        self.all_sprites.add(self.player)
        self.all_sprites.add(self.hoop)
        self.hoops.add(self.hoop)

        self.game_over = False
        self.shot_time = 20  # Initial shot time in seconds
        self.shot_effect = None  # Variable to store the effect of the shot

    def new(self):
        # Create a group for all sprites, including the hoop
        self.bgimage = pg.image.load(os.path.join(img_folder, "court2.png")).convert()
        self.score = 0
        self.all_sprites = pg.sprite.Group()
        self.hoops = pg.sprite.Group()  # Group for hoops

        # Create instances of the Player and Hoop classes
        self.player = Player(self)
        self.hoop = Hoop(self)  # Adjust the coordinates as needed
        self.all_sprites.add(self.player)
        self.all_sprites.add(self.hoop)
        self.hoops.add(self.hoop)

        self.game_over = False
        self.shot_time = 20  # Initial shot time in seconds
        self.shot_effect = None  # Variable to store the effect of the shot

    def run(self):
        # Game loop
        while self.running:
            self.dt = self.clock.tick(FPS) / 1000  # Convert milliseconds to seconds
            self.events()
            self.update()
            self.draw()

    def events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.running = False
            elif event.type == pg.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left mouse button
                    self.shoot_ball(event.pos)

    def update(self):
        if not self.game_over:
            self.all_sprites.update()
            self.handle_shots()

    def draw(self):
        if not self.game_over:
            self.screen.fill(BLACK)
            self.screen.blit(self.bgimage, (0, 0))
            self.all_sprites.draw(self.screen)

            # Draw score and time manually
            font = pg.font.Font(None, 36)
            score_text = font.render(f"Score: {self.score}", True, WHITE)
            time_text = font.render(f"Time: {int(self.shot_time)}", True, WHITE)
            self.screen.blit(score_text, (10, 10))
            self.screen.blit(time_text, (10, 50))

            pg.display.flip()

    def handle_shots(self):
        if self.shot_time > 0:
            # Update shot time
            self.shot_time -= self.dt
        else:
            # End the game when time runs out
            self.game_over = True

    def shoot_ball(self, mouse_pos):
        # Calculate initial velocity based on mouse position
        direction = pg.Vector2(mouse_pos[0] - self.player.rect.centerx,
                               mouse_pos[1] - self.player.rect.centery)
        initial_velocity = direction.normalize() * 500.0  # Use the default initial velocity

        # Create a new basketball instance with the calculated velocity
        ball = Basketball(self, self.player.rect.center, initial_velocity)
        self.all_sprites.add(ball)


# Execute the game
if __name__ == "__main__":
    g = Game()
    g.new()
    g.run()
    pg.quit()