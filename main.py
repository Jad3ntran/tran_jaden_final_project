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

# Code for projectile
a=float(input("Enter the angle in degrees\n"))
# converting angle in radians
a=radians(a)

# Initial velocity of projectile
u=float(input("Enter initial velocity in m/s \n"))

# Evaluating Range
R=u**2*sin(2*a)/g

# Evaluating max height
h=u**2*(sin(a))**2/(2*g)

# Creating array of x with 50 points
x=linspace(0, R, 20)

# Solving for y
y=x*tan(a)-(1/2)*(g*x**2)/(u**2*(cos(a))**2 )
# Data plotting

figure(1,dpi=300)
plot(x,y,'r-',linewidth=3)
xlabel('x')
ylabel('y')
ylim(0, h+0.05)
savefig('proj.jpg')
show()

print(f"{'S. No.':^10}{'x':^10}{'y':^10}")
for i in range(len(x)):
   print(f"{i+1:^10}{round(x[i],3):^10}{round(y[i],3):^10}")

class Game:
    def __init__(self):
        # Initialize pygame and create a window
        pg.init()
        pg.mixer.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption("My Game...")
        self.running = True
        self.paused = False

    def new(self):
        # Create a group for all sprites
        self.bgimage = pg.image.load(os.path.join(img_folder, "court.png")).convert()
        self.score = 0
        self.all_sprites = pg.sprite.Group()

    def draw(self):
        # Draw the background screen
        if not self.game_over:
            self.screen.fill(BLACK)
            self.screen.blit(self.bgimage, (0, 0))
            # Draw all sprites
            self.all_sprites.draw(self.screen)
            # if self.player.health <= 0:
            #     self.draw_text("Game Over", 48, WHITE, WIDTH / 2, HEIGHT / 4)
            self.draw_text("Score: " + str(self.cd.delta), 22, WHITE, WIDTH/2, HEIGHT/10)