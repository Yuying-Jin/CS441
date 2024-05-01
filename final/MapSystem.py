import random
import itertools
import matplotlib.pyplot as plt
from perlin_noise import PerlinNoise
import numpy as np
from pygad import pygad
from PIL import Image, ImageDraw, ImageFont
import pygame

class MapSystem:
    def __int__(self):
        self.cities_t = None

    def get_landscape_surface(self, size, city_names, city_locations, route):
        width, height = size

        cities = route.generate_randomly_spread_cities(size, len(city_locations))

        # generate landscape image
        landscape = Landscape(size)
        landscape_pic = landscape.generate_elevation_to_rgba()

        # setup fitness function and GA
        ga = GeneticAlgorithm(size, len(cities), landscape)
        # fitness_function, ga_instance = ga.setup_GA()
        ga.setup_GA()

        # Run the GA to optimize the parameters of the function.
        ga.ga_instance.run()
        ga.ga_instance.plot_fitness()

        # Show the best solution after the GA finishes running.
        cities = ga.ga_instance.best_solution()[0]
        self.cities_t = ga.solution_to_cities(cities)

        # Use PIL to draw the image
        # Convert the NumPy array to a PIL image
        landscape_img = Image.fromarray(landscape_pic)

        # Create a drawing object
        draw = ImageDraw.Draw(landscape_img)

        # Draw cities and routes on the image
        if self.cities_t is not None:
            # Get routes
            routes = route.get_routes(cities=self.cities_t)

            # Draw routes
            for line in routes:
                draw.line((*line[0], *line[1]), fill='blue', width=2)

            # Get city locations
            cities_x, cities_y = self.cities_t[:, 0], self.cities_t[:, 1]
            # Draw cities
            for x, y, name in zip(cities_x, cities_y, city_names):
                circle_radius = 5  # Adjust the radius of the circle as needed
                circle_bbox = [x - circle_radius, y - circle_radius, x + circle_radius, y + circle_radius]
                draw.ellipse(circle_bbox, fill="red")  # Draw a circle representing the city

                # Draw city name
                font = ImageFont.load_default().font_variant(size=20)
                draw.text((x + circle_radius + 5, y - circle_radius), text=name, fill="black",
                          font=font)

        # Show or save the image as needed
        # landscape_img.show()

        # Convert PIL image to Pygame surface
        pil_image = landscape_img.convert("RGBA")
        image_data = pil_image.tobytes("raw", "RGBA")
        pygame_surface = pygame.image.fromstring(image_data, pil_image.size, "RGBA")

        return pygame_surface


class State:
    def __init__(
            self,
            current_city,
            destination_city,
            travelling,
            encounter_event,
            cities,
            routes,
            coins
    ):
        self.current_city = current_city
        self.destination_city = destination_city
        self.travelling = travelling
        self.encounter_event = encounter_event
        self.cities = cities
        self.routes = routes
        self.coins=coins

class Route:
    def __init__(self):
        self.cities = None
        self.routes = []

    def generate_randomly_spread_cities(self, size: tuple, n_cities: int) -> list:
        """
        :param size: the size of the map as a tuple of 2 integers
        :param n_cities: The number of cities to generate
        :return: A list of City objects with random x and y coordinates.
        """
        if self.cities is None:
            self.cities = [(random.randrange(size[0]), random.randrange(size[1])) for _ in range(n_cities)]
        return self.cities

    def get_routes(self, cities: list) -> list:
        """
        Generate routes between cities ensuring each city is connected to at least one other city.
        :param city_names: a list of cities
        :return: A list of tuples representing some possible links between cities/ pairs of cities,
                each item in the list (a link) represents a route between two cities.
        """
        # routes = list(itertools.permutations(cities, 2))
        # random.shuffle(routes)
        # self.routes = routes[:10]

        visited = set()
        cities = [tuple(city) for city in cities]

        for city in cities:
            if city not in visited:
                visited.add(city)
                path = [city]
                self.dfs(city, cities, visited, path)

        self.routes = list(set(self.routes)) # remove repetitive elements
        # print(self.routes)
        return self.routes

    def dfs(self, current_city, cities, visited, path):
        if len(path) >= 2:
            route = [(path[i - 1], path[i]) for i in range(1, len(path))]
            self.routes.extend(route)
        for next_city in cities:
            if next_city not in visited:
                visited.add(next_city)
                self.dfs(next_city, cities, visited, path + [next_city])
                visited.remove(next_city)
                if 3 % random.randint(1, 3) == 0:
                    break


class Landscape:
    def __init__(self, size):
        self.size = size
        self.elevation = self.generate_elevation()

    def generate_elevation(self):
        xpix, ypix = self.size
        # https://pypi.org/project/perlin-noise/
        noise = PerlinNoise(octaves=20, seed=1)
        elevation = np.array([[noise([i / xpix, j / ypix]) for j in range(xpix)] for i in range(ypix)])
        return elevation

    def generate_elevation_to_rgba(self, cmap: str = 'gist_earth') -> np.array:
        xpix, ypix = np.array(self.elevation).shape
        colormap = plt.colormaps[cmap]

        elevation = (self.elevation - self.elevation.min()) / (self.elevation.max() - self.elevation.min())
        ''' You can play around with colormap to get a landscape of your preference if you want '''
        landscape = np.array([colormap(elevation[i, j])[0:3]
                              for i in range(xpix) for j in range(ypix)]).reshape(xpix, ypix, 3) * 255
        landscape = landscape.astype('uint8')
        return landscape

class GeneticAlgorithm:
    def __init__(self, size, n_cities, landscape):
        self.size = size
        self.n_cities = n_cities
        self.landscape = landscape
        self.fitness_function = None
        self.ga_instance = None

    def game_fitness(self, ga_instance, solution, idx):
        fitness = 0.0001  # Do not return a fitness of 0, it will mess up the algorithm.
        """
        Create your fitness function here to fulfill the following criteria:
        1. The cities should not be under water
        2. The cities should have a realistic distribution across the landscape
        3. The cities may also not be on top of mountains or on top of each other
        4. The cities should not be over safe boundary
        5. The cities should not be too far from each other
        """
        cities = self.solution_to_cities(solution)

        x_safe_boundary, y_safe_boundary = self.size[0] // 10, self.size[1] // 10
        for city in cities:
            x, y = city
            if self.landscape.elevation[x, y] < 0.1:
                fitness -= 2

            if abs(x - self.size[0]) < x_safe_boundary or x < x_safe_boundary:
                fitness -= 4
            if abs(y - self.size[1]) < y_safe_boundary or y < y_safe_boundary:
                fitness -= 4

        distances = []
        for i in range(len(cities)):
            for j in range(i + 1, len(cities)):
                x1, y1 = cities[i]
                x2, y2 = cities[j]
                distance = np.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)
                distances.append(distance)
        avg_distance = np.mean(distances)
        min_distance = np.min(distances)
        if min_distance < 30:
            fitness -= 10
        if avg_distance > 80:
            fitness -= 1

        for i in range(len(cities)):
            for j in range(i + 1, len(cities)):
                x1, y1 = cities[i]
                x2, y2 = cities[j]
                if abs(x1 - x2) <= 1 and abs(y1 - y2) <= 1:
                    fitness -= 1
                if self.landscape.elevation[x1, y1] > 0.8 or self.landscape.elevation[x2, y2] > 0.8:
                    fitness -= 1

        return fitness

    def setup_GA(self):
        """
        It sets up the genetic algorithm with the given fitness function,
        number of cities, and size of the map

        :return: The fitness function and the GA instance.
        """
        num_generations = 100
        num_parents_mating = 10

        solutions_per_population = 300
        num_genes = self.n_cities

        init_range_low = 0
        init_range_high = self.size[0] * self.size[1]

        parent_selection_type = "sss"
        keep_parents = 10

        crossover_type = "single_point"

        mutation_type = "random"
        mutation_percent_genes = 10

        self.ga_instance = pygad.GA(
            num_generations=num_generations,
            num_parents_mating=num_parents_mating,
            fitness_func=self.game_fitness,
            sol_per_pop=solutions_per_population,
            num_genes=num_genes,
            gene_type=int,
            init_range_low=init_range_low,
            init_range_high=init_range_high,
            parent_selection_type=parent_selection_type,
            keep_parents=keep_parents,
            crossover_type=crossover_type,
            mutation_type=mutation_type,
            mutation_percent_genes=mutation_percent_genes,
        )

        self.fitness_function = lambda ga_instance, cities, idx: self.game_fitness(ga_instance, cities, idx)
        # return self.game_fitness, ga_instance

    def solution_to_cities(self, solution):
        """
        It takes a GA solution and size of the map, and returns the city coordinates
        in the solution.

        :param solution: a solution to GA
        :return: The cities are being returned as a list of lists.
        """
        cities = np.array(
            list(map(lambda x: [int(x / self.size[0]), int(x % self.size[1])], solution))
        )
        return cities

    def show_cities(self, cities, landscape_pic, cmap="gist_earth"):
        """
        It takes a list of cities and a landscape picture, and plots the cities on top of the landscape

        :param cities: a list of (x, y) tuples
        :param cmap: the color map to use for the landscape picture, defaults to gist_earth (optional)
        """
        cities = np.array(cities)
        plt.imshow(landscape_pic, cmap=cmap)
        plt.plot(cities[:, 1], cities[:, 0], "r.")
        plt.show()


if __name__ == '__main__':
    size = 640, 480
    # # Route and City
    city_names = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J']
    # '''print the cities and routes'''
    route = Route()
    cities = route.generate_randomly_spread_cities(size, len(city_names))
    # routes = route.get_routes(cities=cities)
    # print('Cities:')
    # for i, city in enumerate(cities):
    #     print(f'{city_names[i]}: {city}')
    # print('Routes:')
    # for i, route in enumerate(routes):
    #     print(f'{i}: {route[0]} to {route[1]}')
    #
    # # Landscape
    # landscape = Landscape(size=size)
    # landscape_pic = landscape.generate_elevation_to_rgba()
    # # print(landscape_pic.shape)
    # # plt.imshow(pic)
    # # plt.show()
    #
    # # setup fitness function and GA
    # ga = GeneticAlgorithm(size, len(cities), landscape)
    # # fitness_function, ga_instance = ga.setup_GA()
    # ga.setup_GA()
    #
    # # Show one of the initial solutions.
    # cities = ga.ga_instance.initial_population[0]
    # cities = ga.solution_to_cities(cities)
    # ga.show_cities(cities, landscape_pic)
    #
    # # Run the GA to optimize the parameters of the function.
    # ga.ga_instance.run()
    # ga.ga_instance.plot_fitness()
    # print("Final Population")
    #
    # # Show the best solution after the GA finishes running.
    # cities = ga.ga_instance.best_solution()[0]
    # cities_t = ga.solution_to_cities(cities)
    # plt.imshow(landscape_pic, cmap="gist_earth")
    # plt.plot(cities_t[:, 1], cities_t[:, 0], "r.")
    # plt.show()
    # print(ga.fitness_function(ga.ga_instance, cities, 0))
    ms = MapSystem()
    img = ms.get_landscape_surface(size=size, city_names=city_names, city_locations=cities, route=route)
    print(img)