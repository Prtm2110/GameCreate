import pygame
from sys import exit

pygame.init()
screen = pygame.display.set_mode((800,400))
pygame.display.set_caption('Runner')
clock =pygame.time.Clock()
sky=pygame.image.load('graphics/Sky.png').convert()
font=pygame.font.Font('font\Pixeltype.ttf',50)
ground=pygame.image.load('graphics/ground.png').convert()

text=font.render('RatRace',1,(64,64,64))
text_rect=text.get_rect(center=(400,50))
snail=pygame.image.load('graphics\snail\snail1.png').convert_alpha()
snail_x=600
snail_rect=snail.get_rect(midbottom=(snail_x,300))
player=pygame.image.load('graphics\player\player_walk_1.png').convert_alpha()
player_rect=player.get_rect(midbottom=(80,300))


while True:
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            pygame.quit()
            exit()
    # mouse=pygame.mouse.get_pos()
    # if player_rect.collidepoint((mouse)):
    #     print(pygame.mouse.get_pressed()) 
    # if event.type==pygame.MOUSEMOTION:
    #     mouse=event.pos

    # if player_rect.collidepoint(mouse):
    #     print('collision')

    screen.blit(sky,(0,0))
    screen.blit(ground,(0,300))
    pygame.draw.rect(screen,'#c0e8ec',text_rect)
    pygame.draw.rect(screen,'#c0e8ec',text_rect,10)
    screen.blit(text,text_rect)
   
    player_rect.left+=1
    screen.blit(player,player_rect)
   
    snail_rect.left-=5
    if snail_rect.left<-100:
         snail_rect.left=800
    screen.blit(snail,snail_rect)

    pygame.display.update()
    clock.tick(60)



