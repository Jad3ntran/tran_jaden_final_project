# main.py

# This file was created by Jaden Tran

'''
Game revolved around basketball

Goals: Score as many points(baskets) as you can
Rules: the further you are from the basket, the more points 
(not limited to 2 or 3 points like the NBA- points can go up to 10 per basket), the further you are, the harder it is
Feedback: score displayed on top of the screen in the form of a scoreboard, similar to a real basketball game,
timer displayed, as well as a top score list.
Freedom: can move as far as the end of the screen in order to score more points, or as close to score easy, but not
as many points
'''

# Importing necessary libraries and modules
import pygame as pg
from pygame.sprite import Sprite
import os
from settings import *
from sprites import *
from numpy import *
from pylab import *

# Importing necessary libraries and modules
import pygame as pg
from pygame.sprite import Sprite
import os
from settings import *
from sprites import *

# Set default values for angle and initial velocity
a = radians(45)  # Default angle in degrees
u = 100.0  # Default initial velocity in m/s

# Evaluating Range
R = u ** 2 * sin(2 * a) / g

# Evaluating max height
h = u ** 2 * (sin(a)) ** 2 / (2 * g)

# Creating an array of x with 50 points
x = linspace(0, R, 20)

# Solving for y
y = x * tan(a) - (1 / 2) * (g * x ** 2) / (u ** 2 * (cos(a)) ** 2)
# Data plotting

figure(1, dpi=300)
plot(x, y, 'r-', linewidth=3)
xlabel('x')
ylabel('y')
ylim(0, h + 0.05)
savefig('proj.jpg')
show()

print(f"{'S. No.':^10}{'x':^10}{'y':^10}")
for i in range(len(x)):
    print(f"{i + 1:^10}{round(x[i], 3):^10}{round(y[i], 3):^10}")


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

    def new(self):
        # Create a group for all sprites, including the hoop
        self.bgimage = pg.image.load(os.path.join(img_folder, "court2.png")).convert()
        self.score = 0
        self.all_sprites = pg.sprite.Group()
        self.hoops = pg.sprite.Group()  # Group for hoops

        # Create instances of the Player and Hoop classes
        self.player = Player(self)
        self.hoop = Hoop(self, WIDTH - 50, HEIGHT/2)  # Adjust the coordinates as needed

        # Add the player and hoop to the sprite groups
        self.all_sprites.add(self.player)
        self.all_sprites.add(self.hoop)
        self.hoops.add(self.hoop)

        self.game_over = False
        self.shot_time = 10  # Initial shot time in seconds
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
        initial_velocity = direction.normalize() * u  # Use the default initial velocity

        # Create a new basketball instance with the calculated velocity
        ball = Basketball(self, self.player.rect.center, initial_velocity)
        self.all_sprites.add(ball)


# Execute the game
if __name__ == "__main__":
    g = Game()
    g.new()
    g.run()
    pg.quit()

