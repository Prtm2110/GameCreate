from sys import exit

import pygame


def score():
    current = int(pygame.time.get_ticks() / 100) - start
    score_text = font.render(f"Score: {current}", True, (64, 64, 64))
    score_rect = score_text.get_rect(center=(400, 50))
    pygame.draw.rect(screen, "#c0e8ec", score_rect)
    pygame.draw.rect(screen, "#c0e8ec", score_rect, 10)
    screen.blit(score_text, score_rect)


def start_screen():
    stand = pygame.image.load("graphics/player/player_stand.png").convert_alpha()
    stand_rect = stand.get_rect(center=(400, 200))

    name = font.render("RatRace", True, (64, 64, 64))
    name_rect = name.get_rect(center=(400, 50))

    message = font.render("Press space to Start", True, (64, 64, 64))
    message_rect = message.get_rect(center=(400, 300))

    screen.fill((94, 129, 162))
    screen.blit(name, name_rect)
    screen.blit(stand, stand_rect)
    screen.blit(message, message_rect)
    pygame.display.update()


def game_over_screen():
    menu = font.render("Restart Game? [Y/N]", True, (64, 64, 64))
    menu_rect = menu.get_rect(center=(400, 200))

    pygame.draw.rect(screen, "Yellow", menu_rect)
    pygame.draw.rect(screen, "Yellow", menu_rect, 40)
    screen.blit(menu, menu_rect)
    pygame.display.update()


# Initialize Pygame
pygame.init()

# Constants
GRAVITY = 1.1
start = 0

# Game states
game_active = False
show_start_screen = True
game_over = False

# Set up the screen
screen = pygame.display.set_mode((800, 400))
pygame.display.set_caption("Runner")
clock = pygame.time.Clock()

# Load assets
sky = pygame.image.load("graphics/Sky.png").convert()
ground = pygame.image.load("graphics/ground.png").convert()
font = pygame.font.Font("font/Pixeltype.ttf", 50)

snail = pygame.image.load("graphics/snail/snail1.png").convert_alpha()
snail_rect = snail.get_rect(midbottom=(800 - 100, 300))

player = pygame.image.load("graphics/player/player_walk_1.png").convert_alpha()
player_rect = player.get_rect(midbottom=(80, 300))

# Game variables
gravity = 0

# Main game loop
while True:
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        if game_active:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if player_rect.bottom == 300:
                        gravity = -22

            if event.type == pygame.MOUSEBUTTONDOWN:
                if player_rect.collidepoint(event.pos):
                    if player_rect.bottom == 300:
                        gravity = -22

        elif show_start_screen:
            start_screen()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    game_active = True
                    show_start_screen = False
                    snail_rect.x = 600
                    player_rect.y = 300
                    gravity = 0
                    start = int(pygame.time.get_ticks() / 100)

        elif game_over:
            game_over_screen()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_y:
                    game_active = True
                    game_over = False
                    snail_rect.x = 600
                    player_rect.y = 300
                    gravity = 0
                    start = int(pygame.time.get_ticks() / 100)
                elif event.key == pygame.K_n:
                    pygame.quit()
                    exit()

    if game_active:
        # Update game state
        gravity += GRAVITY
        player_rect.y += gravity

        # Check player falling below ground
        if player_rect.bottom > 300:
            player_rect.bottom = 300
            gravity = 0

        # Update snail position
        snail_rect.left -= 5
        if snail_rect.right < 0:
            snail_rect.left = 800

        # Drawing
        screen.blit(sky, (0, 0))
        screen.blit(ground, (0, 300))
        screen.blit(player, player_rect)
        screen.blit(snail, snail_rect)
        score()
        if snail_rect.colliderect(player_rect):
            game_active = False
            game_over = True

    # Update display
    pygame.display.update()
    clock.tick(60)
