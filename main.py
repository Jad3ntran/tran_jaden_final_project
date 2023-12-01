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
