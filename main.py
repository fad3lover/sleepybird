import pygame
import random
import sys
import math

pygame.init()

SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600
FPS = 60

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
SKY_BLUE = (135, 206, 235)
GROUND_COLOR = (222, 216, 149)
PIPE_COLOR = (50, 205, 50)

gravity = 0.5
bird_movement = 0
bird_rotation = 0
game_active = False
score = 0
high_score = 0
can_score = True

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Flappy Bird')
clock = pygame.time.Clock()
game_font = pygame.font.Font(None, 40)

bird_rect = pygame.Rect(100, SCREEN_HEIGHT // 2, 34, 24)

pipe_list = []
SPAWNPIPE = pygame.USEREVENT
pygame.time.set_timer(SPAWNPIPE, 1500)
pipe_height = [200, 250, 300, 350, 400]

ground_x = 0
ground_scroll_speed = 2


def create_pipe():
    random_pipe_pos = random.choice(pipe_height)
    gap = 150
    bottom_pipe = pygame.Rect(SCREEN_WIDTH, random_pipe_pos, 70, SCREEN_HEIGHT - random_pipe_pos)
    top_pipe = pygame.Rect(SCREEN_WIDTH, 0, 70, random_pipe_pos - gap)
    return bottom_pipe, top_pipe


def move_pipes(pipes):
    for pipe in pipes:
        pipe.centerx -= 3
    visible_pipes = [pipe for pipe in pipes if pipe.right > 0]
    return visible_pipes


def draw_pipes(pipes):
    for pipe in pipes:
        if pipe.bottom >= SCREEN_HEIGHT:
            pygame.draw.rect(screen, PIPE_COLOR, pipe)
            pygame.draw.rect(screen, PIPE_COLOR, (pipe.x - 5, pipe.y, pipe.width + 10, 30))
        else:
            pygame.draw.rect(screen, PIPE_COLOR, pipe)
            pygame.draw.rect(screen, PIPE_COLOR, (pipe.x - 5, pipe.bottom - 30, pipe.width + 10, 30))


def check_collision(pipes):
    if bird_rect.top <= 0 or bird_rect.bottom >= SCREEN_HEIGHT - 50:
        return False
    
    for pipe in pipes:
        if bird_rect.colliderect(pipe):
            return False
    
    return True


def draw_bird(rotation):
    bird_surface = pygame.Surface((40, 30), pygame.SRCALPHA)
    
    body_rect = pygame.Rect(3, 3, 34, 24)
    pygame.draw.ellipse(bird_surface, (255, 223, 0), body_rect)
    
    pygame.draw.ellipse(bird_surface, (255, 200, 0), (5, 10, 20, 18))
    
    wing_points = [
        (15, 18),
        (8, 22),
        (8, 28),
        (18, 24)
    ]
    pygame.draw.polygon(bird_surface, (255, 180, 0), wing_points)
    pygame.draw.aalines(bird_surface, (200, 140, 0), False, wing_points, 1)
    
    pygame.draw.circle(bird_surface, WHITE, (28, 10), 6)
    pygame.draw.circle(bird_surface, BLACK, (30, 10), 4)
    pygame.draw.circle(bird_surface, WHITE, (31, 9), 1)
    
    beak_points = [
        (37, 15),
        (44, 13),
        (44, 17)
    ]
    pygame.draw.polygon(bird_surface, (255, 140, 0), beak_points)
    pygame.draw.aalines(bird_surface, (200, 100, 0), True, beak_points, 1)
    
    rotated_bird = pygame.transform.rotate(bird_surface, rotation)
    rotated_rect = rotated_bird.get_rect(center=bird_rect.center)
    screen.blit(rotated_bird, rotated_rect)


def update_score(pipes):
    global score, can_score
    
    if pipe_list:
        for pipe in pipes:
            if 95 < pipe.centerx < 105 and can_score:
                score += 1
                can_score = False
            if pipe.centerx < 0:
                can_score = True


def display_score(game_state):
    if game_state == 'game_active':
        score_surface = game_font.render(str(int(score)), True, WHITE)
        score_rect = score_surface.get_rect(center=(SCREEN_WIDTH // 2, 50))
        screen.blit(score_surface, score_rect)
    else:
        score_surface = game_font.render(f'Score: {int(score)}', True, WHITE)
        score_rect = score_surface.get_rect(center=(SCREEN_WIDTH // 2, 50))
        screen.blit(score_surface, score_rect)
        
        high_score_surface = game_font.render(f'High Score: {int(high_score)}', True, WHITE)
        high_score_rect = high_score_surface.get_rect(center=(SCREEN_WIDTH // 2, 500))
        screen.blit(high_score_surface, high_score_rect)
        
        if score == 0:
            message_surface = game_font.render('Press SPACE to Start', True, WHITE)
        else:
            message_surface = game_font.render('Press SPACE to Restart', True, WHITE)
        message_rect = message_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        screen.blit(message_surface, message_rect)


running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if game_active:
                    bird_movement = 0
                    bird_movement -= 8
                else:
                    game_active = True
                    pipe_list.clear()
                    bird_rect.center = (100, SCREEN_HEIGHT // 2)
                    bird_movement = 0
                    score = 0
                    can_score = True
        
        if event.type == SPAWNPIPE and game_active:
            pipe_list.extend(create_pipe())
    
    screen.fill(SKY_BLUE)
    
    if game_active:
        bird_movement += gravity
        bird_rect.centery += bird_movement
        bird_rotation = -bird_movement * 3
        if bird_rotation < -30:
            bird_rotation = -30
        if bird_rotation > 90:
            bird_rotation = 90
        draw_bird(bird_rotation)
        
        pipe_list = move_pipes(pipe_list)
        draw_pipes(pipe_list)
        
        game_active = check_collision(pipe_list)
        
        update_score(pipe_list)
        display_score('game_active')
        
        if score > high_score:
            high_score = score
    else:
        draw_bird(0)
        display_score('game_over')
    
    pygame.draw.rect(screen, GROUND_COLOR, (0, SCREEN_HEIGHT - 50, SCREEN_WIDTH, 50))
    
    pygame.display.update()
    clock.tick(FPS)

pygame.quit()
sys.exit()