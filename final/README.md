# Final Project

## Abstract

As a brave adventurer, you set out on a quest to find this legendary treasure and become the hero. Your journey takes you through lush forests, winding rivers, and towering mountains, where you encounter friendly woodland creatures and helpful villagers.

In this wonderful adventure, the journey is full of opportunities and challenges. You may be blessed by the goddess of luck, making your journey easy and enjoyable. But you may also encounter disasters and lose all your travel expenses. 

The biggest challenge is to keep the travel funds sufficient. Because once you lose all the funds, you will be forced to interrupt your trip and be sent to a homeless shelter. There, you will not be able to continue your adventure.

This project aims to build a game by integrating various AI components to improve gameplay. The game involves traveling between cities and encountering various events. It also utilizes random generation to generate landscapes, city locations, routs amount cities, and events. Three components should be integrated into the game: a Genetic Algorithm (GA) system to realistically spread out cities, a cost of travel based on terrain elevation, and a restriction on movement between cities without established routes. Additionally, this game introduces a gain or lose money event to add variability and consequence to gameplay.  This event applies text generation models as an additional AI technique to enhance player immersion. This report provides detailed descriptions of each AI component and their contributions to solving specific problems within the game.

## List of AI components in the project

1. Genetic Algorithm (GA) system for city distribution
2. Gain or lose money event text generation
3. Routes generation
4. Goal-based AI player

## Problems Solved by AI

### Genetic Algorithm

#### Problem Description

Since the city locations are generated in random, the distribution can be a nightmare. Some cities might be at the top of another city or under water. Some cities might be at the edge of the map or very far away from other cities. So, the distribution of cities should be refined after predefined. 

#### Solution

**Description**: 

Generic algorithm can generate the distribution of cities in the game to ensure that the cities are reasonably distributed on the terrain and meet the setting requirements of the game:


1. The cities should not be under water
2. The cities should have a realistic distribution across the landscape
3. The cities may also not be on top of mountains or on top of each other
4. The cities should not be over safe boundary
5. The cities should not be too far from each other

The algorithm follows the steps below:

1. Initialized GA system and set parameters including the population size, genetic generation, selection, crossover and mutation.
2. Define the fitness function and evaluate the distribution of cities according to specific criteria, and give the fitness value. 
3. During the iteration, the algorithm will evaluate and select individuals based on the fitness function.

**Input:** 

- size: the size of the map, represented by a tuple, such as (size[0], size[1]), which represents the width and height of the map. 
- n_cities: the number of cities. 
- landscape: terrain data, used to evaluate the rationality of city distribution.

**Output:**

- cities: new city coordinates with a reasonable city distribution.

### Gain or lose money event text generation

#### Problem Description

A fun game should have rich stories. It is crucial for imbuing a game with rich narratives and engaging experiences. However, designing different event texts is time-consuming. To mitigate this challenge, leveraging AI-driven text generation models presents a promising solution.

By using text generation technology, the game system can dynamically generate event text in the game, providing players with a richer and more vivid gaming experience. In this system, there are two types of events, positive and negative events. The positive one allows the to gain some coins while the negative one lets the player lose some coins. 

#### Solution

**Description**: Based on the randomly selected input text, this component determines the type of event (earning money or losing money) and the amount of money. Next, it uses a text generation model, ollama, to generate the corresponding event text and supplement the details of the event description. Then, it combines the generated event text with the amount of money to form the final event description. After that, the component interacts with the GUI and updates the player's coin state based on the event type and the amount of coins.

The screen should be able to show the entire event message and update the coin label on the top-left corner. 

**Input:**  state object, including the player's money status.

**Output:** Generated event text describing the situation of the player earning or losing money, It also includes the amount text such as "Gained 5 coins!" or "Lost 10 coins!".


### Routes generation

#### Problem Description

In the game, it's essential to generate valid routes between cities to facilitate the player's travel experience or add more challenges. However, creating these routes poses several challenges:

1. **Connectivity**: Ensuring that each city in the game is connected to at least one other city is crucial for maintaining a coherent and navigable game world. Without proper connectivity, players may encounter dead ends or inaccessible areas, leading to frustration and disengagement.
2. **Limiting Movement**: To add strategic depth and challenge to the game, restricting the player's movement to predetermined routes is necessary. This limitation encourages players to plan their journeys carefully, consider alternative routes, and strategize their movements based on available options.
3. **Validity**: Validating the generated routes to ensure they adhere to game rules and constraints is essential. Routes should respect geographical constraints, avoid overlapping paths, and maintain a logical flow between cities to provide a seamless and immersive gameplay experience.

#### Solution

**Description**: 

This algorithm uses a depth-first search (DFS) algorithm to generate routes between cities. This algorithm efficiently explores the interconnected network of cities, ensuring connectivity and validity of routes while stopping to add some routes randomly to add challenges in player movement.

The algorithm starts from each city, gradually explores other cities connected to it, and records feasible routes. By recursively exploring the connections between cities, the algorithm can ensure that the generated routes are valid and that each city is connected to at least one other city. There are one-third possibility to stop to connect one city to another after this city has got at least one adjacent city.  Once the exploration is complete, the algorithm removes duplicate routes.

In the main loop, if the player selects the invalid route, they will have to stay at the current city.

**Input**: A list containing all the cities in the game, each city is represented by a tuple of its coordinates.

**Output**: A list containing all the valid routes between cities in the game, each route is represented by a tuple containing two city tuples.

### Other Problems Solved

#### Map System

#### Problem Description

The GA system improves the city locations to make them have reasonable distribution. However, this update increases the risk of inconsistency of information about cities and routes in the entire system. In addition, drawing cities and routes on the screen during each iteration of the main loop can be resource-intensive and inefficient. Therefore, the map system class is introduced as a management class for all map-related classes. 

#### Solution

The  `MapSystem` provides the attribute `cities_t`, so the main function can get the updated city location conveniently. 

The `get_landscape_surface` method within the `MapSystem` class optimizes resource usage by generating the landscape surface only when necessary, rather than continuously regenerate it. This approach minimizes unnecessary computations and enhances overall performance.

**Inputs:** size of the game map, city names, predefined city locations, and a route object.

**Output:** It returns a pygame surface representing the landscape, with cities and routes drawn on it.

## Appendix

### Appendix 1: ChatGPT transcript on Game Story

```
User
give me the story of this adventure game
ChatGPT
In the heart of a vibrant and mystical land lies the Kingdom of Eldoria, a realm teeming with wonder, danger, and untold treasures. As a valiant adventurer seeking fame and fortune, you embark on a daring journey across Eldoria's diverse landscapes, from enchanted forests to treacherous mountain ranges, in search of legendary artifacts and ancient secrets.

Your quest begins in the bustling city of Ardenia, where you receive a cryptic message from the kingdom's wise sage, foretelling of an imminent threat looming over Eldoria. Armed with courage and determination, you set out to uncover the truth behind the prophecy and protect the kingdom from impending doom.

Along your journey, you encounter a colorful cast of characters, from cunning thieves to noble knights, each with their own motives and secrets to uncover. You forge alliances, unravel mysteries, and navigate treacherous terrain, all while facing perilous challenges and cunning adversaries.

As you traverse the vast expanse of Eldoria, you uncover ancient ruins, hidden temples, and forgotten civilizations, each holding clues to the kingdom's rich history and the source of its power. Along the way, you must make crucial decisions that shape your destiny, determining the fate of Eldoria and its inhabitants.

But beware, for dark forces lurk in the shadows, seeking to thwart your quest and claim the kingdom's riches for themselves. From malevolent sorcerers to fearsome beasts, you must overcome formidable obstacles and confront your deepest fears to emerge victorious.

Ultimately, your journey culminates in a climactic showdown against the forces of darkness, where you must harness all your skills and courage to vanquish the threat and save Eldoria from destruction. Will you rise to the challenge and become a legendary hero, or will Eldoria fall into darkness forever? The fate of the kingdom lies in your hands.

User
simple one please
ChatGPT
Certainly! Here's a simplified version:

In the peaceful kingdom of Evergreen, a great treasure is said to be hidden deep within the enchanted Forest of Whispers. As a brave adventurer, you set out on a quest to find this legendary treasure and become the hero of Evergreen.

Your journey takes you through lush forests, winding rivers, and towering mountains, where you encounter friendly woodland creatures and helpful villagers. Along the way, you must solve puzzles, overcome obstacles, and outsmart cunning traps to reach your goal.

But beware! The forest is also home to fearsome monsters and mischievous bandits who will stop at nothing to claim the treasure for themselves. You'll need all your wits and courage to outmaneuver them and reach the treasure's hidden location.

As you delve deeper into the forest, you uncover ancient ruins and forgotten temples, each holding clues to the treasure's whereabouts. With the help of your loyal companions and your trusty map, you navigate the twists and turns of the forest, inching closer to your goal with each step.

Finally, after a series of thrilling adventures and heart-pounding encounters, you reach the heart of the Forest of Whispers and discover the legendary treasure. With it, you return triumphantly to Evergreen, hailed as a hero and savior of the kingdom.
```

### Appendix 2: Return the Landscape as Pygame Surface

``` 
User
# Show the best solution after the GA finishes running.
        cities = ga.ga_instance.best_solution()[0]
        cities_t = ga.solution_to_cities(cities)

        fig, ax = plt.subplots()
        ax.imshow(landscape_pic)

        if cities_t is not None:
            cities_x, cities_y = cities_t[:, 1], cities_t[:, 0]
            ax.plot(cities_x, cities_y, "r.")

        fig.canvas.draw()


here I do not want to use matplotlib to draw the cities on image. I wanna use PIL
ChatGPT
If you want to use PIL (Python Imaging Library) to draw the cities on the image instead of matplotlib, you can achieve this by creating a PIL image from the landscape image and then drawing the cities on that image. Here's how you can modify your code to do that:

python
Copy code
from PIL import Image, ImageDraw
import numpy as np

# Convert the NumPy array to a PIL image
landscape_img = Image.fromarray(landscape_pic)

# Create a drawing object
draw = ImageDraw.Draw(landscape_img)

# Draw the cities on the image
if cities_t is not None:
    cities_x, cities_y = cities_t[:, 1], cities_t[:, 0]
    for x, y in zip(cities_x, cities_y):
        draw.rectangle([x-2, y-2, x+2, y+2], fill="red")  # Draw a small rectangle representing the city

# Show or save the image as needed
landscape_img.show()  # Show the image
# landscape_img.save("output_image.png")  # Save the image to a file
This code will draw red rectangles on the cities' positions on the image. Adjust the size and style of the rectangles as needed to suit your visualization requirements.

User
may I return the image and set as a pygame surface
ChatGPT
Yes, you can return the PIL image and convert it to a Pygame surface. Here's how you can modify the code to do that:

python
Copy code
import pygame
from PIL import Image, ImageDraw
import numpy as np

def draw_cities_on_image(landscape_pic, cities_t):
    # Convert the NumPy array to a PIL image
    landscape_img = Image.fromarray(landscape_pic)

    # Create a drawing object
    draw = ImageDraw.Draw(landscape_img)

    # Draw the cities on the image
    if cities_t is not None:
        cities_x, cities_y = cities_t[:, 1], cities_t[:, 0]
        for x, y in zip(cities_x, cities_y):
            draw.rectangle([x-2, y-2, x+2, y+2], fill="red")  # Draw a small rectangle representing the city

    # Convert PIL image to Pygame surface
    pil_image = landscape_img.convert("RGBA")
    image_data = pil_image.tobytes("raw", "RGBA")
    pygame_surface = pygame.image.fromstring(image_data, pil_image.size, "RGBA")

    return pygame_surface

# Usage example
pygame.init()

# Assuming you have the landscape_pic and cities_t variables defined
landscape_pic = np.zeros((100, 100))  # Example landscape_pic
cities_t = np.array([[20, 30], [50, 70], [80, 10]])  # Example cities_t

pygame_surface = draw_cities_on_image(landscape_pic, cities_t)

# Now you can use the pygame_surface as needed in your Pygame application
This code will return a Pygame surface with the cities drawn on the image. You can then use this surface as needed in your Pygame application, such as blitting it onto the screen. Adjust the size and style of the drawn cities as needed to suit your visualization requirements.
```

### Appendix 3: Display the Message in the Center of Screen

```
User
How to show the event message in the center of the screen
ChatGPT
To display the event message in the center of the screen, you need to calculate the position of the text based on the screen dimensions and the size of the text. Here's how you can do it:

python
Copy code
import pygame
import sys

# Initialize Pygame
pygame.init()

# Set screen size and title
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Event Message Example")

# Set font
font = pygame.font.Font(None, 36)

# Define event message
event_message = "Something happened!"

# Render text
def render_text():
    text = font.render(event_message, True, (255, 255, 255))
    text_rect = text.get_rect(center=(screen_width // 2, screen_height // 2))
    screen.blit(text, text_rect)

# Game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Add code to handle your specific events here

    # Clear the screen
    screen.fill((0, 0, 0))

    # Update and render text
    render_text()

    # Refresh the screen
    pygame.display.flip()

# Quit Pygame
pygame.quit()
sys.exit()
In this example, the event message is rendered in the center of the screen by using the get_rect() method to get the rectangle of the text surface and then setting its center to the center of the screen using screen_width // 2 and screen_height // 2.
```

