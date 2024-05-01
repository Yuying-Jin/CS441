'''
Lab 5: PCG and Project Lab

This a combined procedural content generation and project lab. 
You will be creating the static components of the game that will be used in the project.
Use the landscape.py file to generate a landscape for the game using perlin noise.
Use the lab 2 cities_n_routes.py file to generate cities and routes for the game.
Draw the landscape, cities and routes on the screen using pygame.draw functions.
Look for triple quotes for instructions on what to do where.
The intention of this lab is to get you familiar with the pygame.draw functions, 
use perlin noise to generate a landscape and more importantly,
build a mindset of writing modular code.
This is the first time you will be creating code that you may use later in the project.
So, please try to write good modular code that you can reuse later.
You can always write non-modular code for the first time and then refactor it later.
'''

import sys
import pygame
import random
import numpy as np
from landscape import get_landscape

from pathlib import Path
sys.path.append(str((Path(__file__)/'..'/'..').resolve().absolute()))
from lab2.cities_n_routes import get_randomly_spread_cities, get_routes


# TODO: Demo blittable surface helper function

''' Create helper functions here '''
def draw_cities(screen, size, city_locations_dict):
    pygame.display.set_caption('Show Text')
    font = pygame.font.Font('freesansbold.ttf', 16)

    for name, location in city_locations_dict.items():
        pygame.draw.circle(screen, (255,0,0), (location[0], location[1]), 4)
        label = font.render(name, True, (1,1,1))
        if location[0] < size[0]/3*2:
            x = location[0] + 4
        else:
            x = location[0] - int(len(name)*9.5)

        if location[1] < size[1]/3*2:
            y = location[1] + 4
        else:
            y = location[1] - 10

        screen.blit(label, (x, y))

def draw_first_10_routes(screen, routes, city_locations_dict):
    for start, end in routes:
        pygame.draw.line(screen, (0,0,255), city_locations_dict[start],  city_locations_dict[end])

if __name__ == "__main__":
    pygame.init()
    size = width, height = 640, 480
    black = 1, 1, 1

    screen = pygame.display.set_mode(size)
    print("screen", screen)
    landscape = get_landscape(size)
    print("Created a landscape of size", landscape.shape)
    pygame_surface = pygame.surfarray.make_surface(landscape[:, :, :3]) 
    print("pygame_surface", pygame_surface, "landscape.shape", landscape.shape)
    city_names = ['Morkomasto', 'Morathrad', 'Eregailin', 'Corathrad', 'Eregarta',
                  'Numensari', 'Rhunkadi', 'Londathrad', 'Baernlad', 'Forthyr']
    city_locations = [] 
    routes = []

    ''' Setup cities and routes in here'''
    city_locations = get_randomly_spread_cities(size=size, n_cities=len(city_names))
    routes = get_routes(cities=city_names)

    city_locations_dict = {name: location for name, location in zip(city_names, city_locations)}
    random.shuffle(routes)
    routes = routes[:10] 

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

        screen.fill(black)
        screen.blit(pygame_surface, (0, 0))

        ''' draw cities '''
        draw_cities(screen, size, city_locations_dict)

        ''' draw first 10 routes '''
        draw_first_10_routes(screen, routes, city_locations_dict)

        pygame.display.flip()
