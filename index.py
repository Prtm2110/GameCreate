import pygame
from sys import exit
def score():
    current=int(pygame.time.get_ticks()/100)-start
    score=font.render(f'score: {current}',True,(64,64,64))
    score_rect=score.get_rect(center=(400,50))

    pygame.draw.rect(score, '#c0e8ec', score_rect)
    pygame.draw.rect(score, '#c0e8ec', score_rect, 10)
    screen.blit(score, score_rect)



# Initialize Pygame
pygame.init()

# Constants
# SCREEN_WIDTH, SCREEN_HEIGHT = 800, 400

GRAVITY = 2
start=0

game_active=1
# Set up the screen
screen = pygame.display.set_mode((800, 400))
pygame.display.set_caption('Runner')
clock = pygame.time.Clock()

# Load assets
sky = pygame.image.load('graphics/Sky.png').convert()
ground = pygame.image.load('graphics/ground.png').convert()
font = pygame.font.Font('font/Pixeltype.ttf', 50)
text = font.render('RatRace', True, (64, 64, 64))
text_rect = text.get_rect(center=(800// 2, 50))

snail = pygame.image.load('graphics/snail/snail1.png').convert_alpha()
snail_rect = snail.get_rect(midbottom=(800- 100, 300 ))

player = pygame.image.load('graphics/player/player_walk_1.png').convert_alpha()
player_rect = player.get_rect(midbottom=(80, 300))

menu=font.render('Restart Game ? [Y/N]', True, (64, 64, 64))
menu_rect=menu.get_rect(center=(400,200))



# Game variables
gravity = 0
count=1

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
                      gravity=-35  

            

            if event.type == pygame.MOUSEBUTTONDOWN:
                if player_rect.collidepoint(event.pos):
                    if player_rect.bottom == 300:
                        gravity = -30

        # if count==1:
 

        if game_active==False:
             
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_y:
                    game_active=True
                    snail_rect.x=600
                    player_rect.y=300
                    gravity=0
                    start=int(pygame.time.get_ticks()/100)

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_n: 
                    pygame.quit()   
                    exit()    

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
    if game_active==1:
 
        screen.blit(sky, (0, 0))
        screen.blit(ground, (0, 300))
        screen.blit(player, player_rect)
        screen.blit(snail, snail_rect)
        score()
        if snail_rect.colliderect(player_rect):
            game_active=0
    else:
       pygame.draw.rect(screen, 'Yellow', menu_rect)
       pygame.draw.rect(screen, 'Yellow', menu_rect, 40)
       screen.blit(menu, menu_rect)

    # Update display
    pygame.display.update()
    clock.tick(60)