import random
import sys

import MapSystem
from CharacterSystem import pygame_ai_player, sprite, pygame_combat
import EventSystem
from EventSystem import GainOrLoseMoney
import pygame


pygame.font.init()
game_font = pygame.font.SysFont("Comic Sans MS", 15)

size = width, height = 640, 480
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)


def setup_window(width, height, caption):
    pygame.init()
    window = pygame.display.set_mode((width, height))
    pygame.display.set_caption(caption)
    return window


def get_combat_surface(size):
    landscape = MapSystem.Landscape(size)
    get_combat_bg = lambda pixel_map: landscape.generate_elevation_to_rgba("RdPu")
    landscape = get_combat_bg(size)
    print("Created a landscape of size", landscape.shape)
    pygame_surface = pygame.surfarray.make_surface(landscape[:, :, :3])
    return pygame_surface


def render_coin_text(coin_amount):
    coin_text = game_font.render("Player Money: $" + str(coin_amount), True, (255, 255, 255))
    screen.blit(coin_text, (10, 10))


def render_event_text(event_message):
    background_color = (50, 50, 50, 200)
    max_width = width // 2   # Limit message box width to half the screen width
    rendered_lines = [game_font.render(line, True, WHITE) for line in event_message.split('\n')]
    total_height = sum([text.get_height() for text in rendered_lines]) + 10

    background_surface = pygame.Surface((max_width, total_height), pygame.SRCALPHA)
    background_surface.fill(background_color)

    y_offset = 5
    for text in rendered_lines:
        background_surface.blit(text, (10, y_offset))
        y_offset += text.get_height() + 5

    screen.blit(background_surface, ((width - background_surface.get_width()) // 2, (height - background_surface.get_height()) // 2))


def show_game_over_screen():
    game_over_text = game_font.render("Game Over! Travel funds depleted.", True, WHITE)
    screen.blit(game_over_text, ((width - game_over_text.get_width()) / 2, height / 2))
    pygame.display.flip()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                sys.exit()



if __name__ == "__main__":
    black = 1, 1, 1
    start_city = 0
    end_city = 9
    sprite_speed = 1
    coins = 20

    screen = setup_window(width, height, "Final")

    city_names = [
        "Morkomasto",
        "Morathrad",
        "Eregailin",
        "Corathrad",
        "Eregarta",
        "Numensari",
        "Rhunkadi",
        "Londathrad",
        "Baernlad",
        "Forthyr",
    ]

    # get cities
    route = MapSystem.Route()
    city_locations = route.generate_randomly_spread_cities(size, len(city_names))

    # get surfaces
    ms = MapSystem.MapSystem()
    landscape_surface = ms.get_landscape_surface(
        size=size, city_names=city_names,
        city_locations=city_locations, route=route)
    # get routes
    routes = route.routes

    combat_surface = get_combat_surface(size)

    # set players
    sprite_path = "../assets/lego.png"
    player = pygame_ai_player.PyGameAIPlayer()
    player_sprite = sprite.Sprite(sprite_path, city_locations[start_city])

    state = MapSystem.State(
        current_city=start_city,
        destination_city=start_city,
        travelling=False,
        encounter_event=False,
        cities=ms.cities_t,
        routes=[tuple(route) for route in routes],
        coins=coins

    )

    money_event = EventSystem.GainOrLoseMoney(state)
    event_text = None
    show_event = False
    event_start_time = 0

    while True:
        action = player.selectAction(state)
        if 0 <= int(chr(action)) <= 9:

            if int(chr(action)) != state.current_city and not state.travelling:
                start = state.cities[state.current_city]
                state.destination_city = int(chr(action))
                destination = state.cities[state.destination_city]
                player_sprite.set_location(state.cities[state.current_city])

                route = (tuple(start), tuple(destination))
                reverse_route = (tuple(destination), tuple(start))

                if route not in state.routes and reverse_route not in state.routes:
                    print("Stay at", state.current_city)
                    continue

                else:
                    state.travelling = True
                    print(
                        "Travelling from", state.current_city, "to", state.destination_city
                    )

        screen.fill(black)
        screen.blit(landscape_surface, (0, 0))
        render_coin_text(state.coins)

        if state.travelling:
            state.travelling = player_sprite.move_sprite(destination, sprite_speed)
            state.encounter_event = random.randint(0, 1000) < 2
            if not state.travelling:
                print('Arrived at', state.destination_city)

        if not state.travelling:
            if 3 % random.randint(1, 3) == 0:
                event_text = money_event.execute()
                render_event_text(event_text)
                pygame.time.wait(30)

            state.current_city = state.destination_city
            render_coin_text(state.coins)

        if state.coins < 0:
            show_game_over_screen()

        if state.encounter_event:
            pygame_combat.run_pygame_combat(combat_surface, screen, player_sprite)
            state.encounter_event = False
        else:
            player_sprite.draw_sprite(screen)
        pygame.display.update()

        # wait ** ms
        pygame.time.wait(7)

        if state.current_city == end_city:
            print('You have reached the end of the game!')
            break
