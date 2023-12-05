# This is the sprites file

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

