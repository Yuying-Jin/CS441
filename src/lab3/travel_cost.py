'''
Lab 3: Travel Cost

Your player will need to move from one city to another in order to complete the game.
The player will have to spend money to travel between cities. The cost of travel depends 
on the difficulty of the terrain.
In this lab, you will write a function that calculates the cost of a route between two cities,
A terrain is generated for you 
'''
import numpy as np
import matplotlib.pyplot as plt
import math

def update_position(start, end):
  if start > end:
    start -= 1
  elif start < end:
    start += 1
  return start


def get_route_cost(route_coordinate, game_map):
    """
    This function takes in a route_coordinate as a tuple of coordinates of cities to connect, 
    example:  and a game_map as a numpy array of floats,
    remember from previous lab the routes looked like this: [(A, B), (A, C)]
    route_coordinates is just inserts the coordinates of the cities into a route like (A, C).
    route_coordinate might look like this: ((0, 0), (5, 4))

    For each route this finds the cells that lie on the line between the
    two cities at the end points of a route, and then sums the cost of those cells
      -------------
    1 | A |   |   |
      |-----------|
    2 |   |   |   |
      |-----------|
    3 |   | C |   |
      -------------
        I   J   K 

    Cost between cities A and C is the sum of the costs of the cells 
        I1, I2, J2 and J3.
    Alternatively you could use a direct path from A to C that uses diagonal movement, like
        I1, J2, J3

    :param route_coordinates: a list of tuples of coordinates of cities to connect
    :param game_map: a numpy array of floats representing the cost of each cell

    :return: a floating point number representing the cost of the route
    """
    # Build a path from start to end that looks like [(0, 0), (1, 1), (2, 2), (3, 3), (4, 4), (5, 4)]

    print(route_coordinate)
    path = []

    # Get start and end cells
    city_start, city_end = route_coordinate
    city_start_x, city_start_y = city_start
    city_end_x, city_end_y = city_end

    # Append the first cell
    path.append((city_start_x, city_start_y))

    # Initialize the var is_H_or_V_line as False
    is_H_or_V_line = False

    # Process the case that path is a horizontal or vertical line first
    if city_start_x == city_end_x:
      is_H_or_V_line = True
      vertical_distance = abs(city_start_y - city_end_y)

      for i in range(vertical_distance):
        city_start_y = update_position(city_start_y, city_end_y)
        path.append((city_start_x, city_start_y))

    if city_start_y == city_end_y:
      is_H_or_V_line = True
      horizontal_distance = abs(city_start_x - city_end_x)

      for i in range(horizontal_distance):
        city_start_x = update_position(city_start_x, city_end_x)
        path.append((city_start_x, city_start_y))

    if is_H_or_V_line:
      return game_map[tuple(zip(*path))].sum() # Return

    horizontal_distance = abs(city_start_x - city_end_x)
    vertical_distance = abs(city_start_y - city_end_y)

    # Process the case that path is a diagonal line (horizontal dist equals to vertial dist)
    if horizontal_distance == vertical_distance:
      while city_start_x != city_start_y:
        city_start_x = update_position(city_start_x, city_end_x)
        city_start_y = update_position(city_start_y, city_end_y)
        path.append((city_start_x, city_start_y))
      return game_map[tuple(zip(*path))].sum() # Return

    # Process other cases
    # if horizontal dist is longer
    if horizontal_distance > vertical_distance:
      multi = horizontal_distance / vertical_distance # float
      # print(f"multi: {multi}")

      for pt in range(horizontal_distance):

        # Update y
        if math.floor(pt % multi) == 0 and pt != 0:
          city_start_y = update_position(city_start_y, city_end_y)
          
        # Update x
        city_start_x = update_position(city_start_x, city_end_x)
        path.append((city_start_x, city_start_y))

    # if vertical dist is longer
    if horizontal_distance < vertical_distance:
      multi = vertical_distance / horizontal_distance # float
      # print(f"multi: {multi}")

      for pt in range(vertical_distance):

        # Update x
        if math.floor(pt % multi) == 0 and pt != 0:
          city_start_x = update_position(city_start_x, city_end_x)
        
        # Update y
        city_start_y = update_position(city_start_y, city_end_y)
        path.append((city_start_x, city_start_y))

    # issue: the floor() method of math.floor(pt % multi) leads to miss the last one
    # if using round(), the path is not smooth enough
    # Append the last one
    if path[-1] != (city_end_x, city_end_y):
      path.append((city_end_x, city_end_y))

    # Visualize and save the path as a scatter diagram and a text file
    x, y = zip(*path)
    plt.scatter(x,y, marker="s")
    plt.savefig(f"{route_coordinate[0]}-{route_coordinate[1]}.jpg")
    plt.clf() # clear figure

    with open(f"{route_coordinate[0]}-{route_coordinate[1]}.txt", 'w') as file:
      for p in path:
          file.write("%s\n" % str(p))
    return game_map[tuple(zip(*path))].sum()


def route_to_coordinates(city_locations, city_names, routes):
    """ get coordinates of each of the routes from cities and city_names"""
    route_coordinates = []
    for route in routes:
        start = city_names.index(route[0])
        end = city_names.index(route[1])
        route_coordinates.append((city_locations[start], city_locations[end]))
    return route_coordinates


def generate_terrain(map_size):
    """ generate a terrain map of size map_size """
    return np.random.rand(*map_size)


def main():
    # Ignore the following 4 lines. This is bad practice, but it's just to make the code work in the lab.
    import sys
    from pathlib import Path
    sys.path.append(str((Path(__file__)/'..'/'..').resolve().absolute()))
    from lab2.cities_n_routes import get_randomly_spread_cities, get_routes

    city_names = ['Morkomasto', 'Morathrad', 'Eregailin', 'Corathrad', 'Eregarta', 'Numensari', 'Rhunkadi', 'Londathrad', 'Baernlad', 'Forthyr']
    map_size = 300, 200

    n_cities = len(city_names)
    game_map = generate_terrain(map_size)
    print(f'Map size: {game_map.shape}')

    city_locations = get_randomly_spread_cities(map_size, n_cities)
    routes = get_routes(city_names)
    np.random.shuffle(routes)
    routes = routes[:10]
    route_coordinates = route_to_coordinates(city_locations, city_names, routes)

    for route, route_coordinate in zip(routes, route_coordinates):
        print(f'Cost between {route[0]} and {route[1]}: {get_route_cost(route_coordinate, game_map)}')


if __name__ == '__main__':
    main()