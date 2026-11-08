# Example file showing a circle moving on screen
import pygame
import random

# pygame setup
pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True
dt = 0
count = 0

player_pos = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)
enemy_1_pos = pygame.Vector2(300, 360)
enemy_2_pos = pygame.Vector2(980, 360)

def change_momentum(enemy_1, enemy_2, count):
    if count > 60:
        for enemy_pos in [enemy_1, enemy_2]:
            val = (random.random() * 4).__ceil__()
            speed = 500
            if val == 1:
                enemy_pos.y -= speed * dt
            if val == 2:
                enemy_pos.y += speed * dt
            if val == 3:
                enemy_pos.x -= speed * dt
            if val == 4:
                enemy_pos.x += speed * dt
    count = 0


while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # fill the screen with a color to wipe away anything from last frame
    screen.fill("purple")

    pygame.draw.circle(screen, "green", player_pos, 40)

    pygame.draw.circle(screen, "red", enemy_1_pos, 40)

    pygame.draw.circle(screen, "red", enemy_2_pos, 40)

    speed = 500
    keys = pygame.key.get_pressed()
    if keys[pygame.K_w] and player_pos.y > 40:
        player_pos.y -= speed * dt
        change_momentum(enemy_1_pos, enemy_2_pos, count)
            
    if keys[pygame.K_s] and player_pos.y < 680:
        player_pos.y += speed * dt
        change_momentum(enemy_1_pos, enemy_2_pos, count)
            
    if keys[pygame.K_a] and player_pos.x > 40:
        player_pos.x -= speed * dt    
        change_momentum(enemy_1_pos, enemy_2_pos, count)
            
    if keys[pygame.K_d] and player_pos.x < 1240:
        player_pos.x += speed * dt
        change_momentum(enemy_1_pos, enemy_2_pos, count)
            
    # flip() the display to put your work on screen
    pygame.display.flip()

    # limits FPS to 60
    # dt is delta time in seconds since last frame, used for framerate-
    # independent physics.
    dt = clock.tick(60) / 1000
    count += 1

pygame.quit()