import pygame
from sys import exit

def display_score():
    current_time = int(pygame.time.get_ticks() / 1000) - start_time
    score_surf = test_font.render(f'Score: {current_time}', False, (64, 64, 64))
    score_rect = score_surf.get_rect(center = (400, 50))
    screen.blit(score_surf, score_rect)
    return current_time

def add_game_title():
    game_title = test_font.render(f'Pixle Runner', False, (111, 196, 169))
    game_title_rect = game_title.get_rect(center = (400, 80))
    screen.blit(game_title, game_title_rect)

def add_game_instruct():
    game_instruct = test_font.render(f"Press 'Space' To Play", False, (111, 196, 169))
    game_instruct_rect = game_instruct.get_rect(center = (400, 330))
    screen.blit(game_instruct, game_instruct_rect)

def add_game_score():
    game_score = test_font.render(f'Your Score: {score}', False, (111, 196, 169))
    game_score_rect = game_score.get_rect(center = (400, 330))
    screen.blit(game_score, game_score_rect)

pygame.init()
screen = pygame.display.set_mode((800,400))
pygame.display.set_caption("Runner")
clock = pygame.time.Clock()
test_font = pygame.font.Font('Runner_fonts/pixeltype.ttf', 50)
game_active = False
start_time = 0
score = 0


sky_surface = pygame.image.load('Runner_graphics/Sky.png').convert()
ground_surface = pygame.image.load('Runner_graphics/ground.png').convert()

# score_surf = test_font.render('My game', False, (64,64,64))
# score_rect = score_surf.get_rect(center = (400, 50))

snail_surf = pygame.image.load('Runner_graphics/Snail/snail1.png').convert_alpha()
snail_rect = snail_surf.get_rect(midbottom = (600, 300))

player_surf = pygame.image.load('Runner_graphics/Player/player_walk_1.png').convert_alpha()
player_rect = player_surf.get_rect(midbottom = (80, 300))
player_gravity = 0

#Intro screen
player_stand = pygame.image.load('Runner_graphics/Player/player_stand.png').convert_alpha()
player_stand = pygame.transform.rotozoom(player_stand, 0, 2)
player_stand_rect = player_stand.get_rect(center = (400, 200))

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        if game_active:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if player_rect.collidepoint(event.pos) and player_rect.bottom >= 300:
                    player_gravity = -20

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and player_rect.bottom >= 300:
                    player_gravity = -20
        else:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                snail_rect.left = 800
                game_active = True
                start_time = int(pygame.time.get_ticks() / 1000)

    if game_active:
        screen.blit(sky_surface, (0,0))
        screen.blit(ground_surface, (0,300))
        # pygame.draw.rect(screen, '#c0e8ec', score_rect.inflate(10, 10)) 
        # screen.blit(score_surf, score_rect)
        score = display_score()

        snail_rect.x -= 4
        if snail_rect.right <= 0:
            snail_rect.left = 800
        screen.blit(snail_surf, snail_rect)

        # Player
        player_gravity += 1
        player_rect.y += player_gravity
        if player_rect.bottom >= 300:
            player_rect.bottom = 300
        screen.blit(player_surf, player_rect)

        # Collision
        if snail_rect.colliderect(player_rect):
            game_active = False
    else:
        screen.fill((94,129,162))
        screen.blit(player_stand, player_stand_rect)
        add_game_title()
        if score == 0:
            add_game_instruct()
        else:
            add_game_score()

    pygame.display.update()
    clock.tick(60)