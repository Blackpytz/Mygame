import pygame
from sys import exit
from random import randint, choice

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        player_walk_1 = pygame.image.load('Runner_graphics/Player/player_walk_1.png').convert_alpha()
        player_walk_2 = pygame.image.load('Runner_graphics/Player/player_walk_2.png').convert_alpha()
        self.player_walk = [player_walk_1, player_walk_2]
        self.player_index = 0
        self.player_jump = pygame.image.load('Runner_graphics/Player/jump.png').convert_alpha()

        self.image = self.player_walk[self.player_index]
        self.rect = self.image.get_rect(midbottom = (80, 300))
        self.gravity = 0

    def player_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and self.rect.bottom >= 300:
            self.gravity = -20

    def apply_gravity(self):
        self.gravity += 1
        self.rect.y += self.gravity
        if self.rect.bottom >= 300:
            self.rect.bottom = 300

    def animation_state(self):
        if self.rect.bottom < 300:
            self.image = self.player_jump
        else:
            self.player_index += 0.1
            if self.player_index >= len(self.player_walk):
                self.player_index = 0
            self.image = self.player_walk[int(self.player_index)]

    def update(self):
        self.player_input()
        self.apply_gravity()
        self.animation_state()

class Obstacle(pygame.sprite.Sprite):
    def __init__(self, type):
        super().__init__()

        if type == 'fly':
            fly_1 = pygame.image.load('Runner_graphics/Fly/fly1.png').convert_alpha()
            fly_2 = pygame.image.load('Runner_graphics/Fly/fly2.png').convert_alpha()
            self.frames = [fly_1, fly_2]
            y_pos = 210
        else:
            snail_1 = pygame.image.load('Runner_graphics/Snail/snail1.png').convert_alpha()
            snail_2 = pygame.image.load('Runner_graphics/Snail/snail2.png').convert_alpha()
            self.frames = [snail_1, snail_2]
            y_pos = 300

        self.animation_index = 0
        self.image = self.frames[self.animation_index]
        self.rect = self.image.get_rect(midbottom = (randint(900, 1100), y_pos))

    def animation_state(self):
            self.animation_index += 0.1
            if self.animation_index >= len(self.frames):
                self.animation_index = 0
            self.image = self.frames[int(self.animation_index)]

    def update(self):
            self.animation_state()
            self.rect.x -= 6
            self.destroy()

    def destroy(self):
        if self.rect.x <= -100:
            self.kill()

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
    game_instruct = test_font.render(f'Press Space To Play', False, (111, 196, 169))
    game_instruct_rect = game_instruct.get_rect(center = (400, 330))
    screen.blit(game_instruct, game_instruct_rect)

def add_game_score():
    game_score = test_font.render(f'Your Score: {score}', False, (111, 196, 169))
    game_score_rect = game_score.get_rect(center = (400, 330))
    screen.blit(game_score, game_score_rect)

def collision_sprite():
    if pygame.sprite.spritecollide(player.sprite, obstacle_group, False):
        obstacle_group.empty()
        return False
    else:
        return True


pygame.init()
screen = pygame.display.set_mode((800,400))
pygame.display.set_caption("Runner")
clock = pygame.time.Clock()
test_font = pygame.font.Font('Runner_fonts/pixeltype.ttf', 50)
game_active = False
start_time = 0
score = 0 

#Groups
player = pygame.sprite.GroupSingle()
player.add(Player())

obstacle_group = pygame.sprite.Group()

sky_surface = pygame.image.load('Runner_graphics/Sky.png').convert()
ground_surface = pygame.image.load('Runner_graphics/ground.png').convert()

player_gravity = 0

#Intro screen
player_stand = pygame.image.load('Runner_graphics/Player/player_stand.png').convert_alpha()
player_stand = pygame.transform.rotozoom(player_stand, 0, 2)
player_stand_rect = player_stand.get_rect(center = (400, 200))

# Timer
obstacle_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_timer, 1500)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        if not game_active:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                game_active = True
                start_time = int(pygame.time.get_ticks() / 1000)
        else:
            if event.type == obstacle_timer:
                obstacle_group.add(Obstacle(choice(['fly', 'snail', 'snail', 'snail'])))

    if game_active:
        screen.blit(sky_surface, (0,0))
        screen.blit(ground_surface, (0,300))
        score = display_score()

        player.draw(screen)
        player.update()

        obstacle_group.draw(screen)
        obstacle_group.update()

        # # Collision
        game_active = collision_sprite()

    else:
        screen.fill((94, 129, 162))
        screen.blit(player_stand, player_stand_rect)

        add_game_title()
        if score == 0:
            add_game_instruct()
        else:
            add_game_score()

    pygame.display.update()
    clock.tick(60)