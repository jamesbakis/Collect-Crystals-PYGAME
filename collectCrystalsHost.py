# Example file showing a circle moving on screen
import os
import pygame
import random
import math
import socket
from dotenv import load_dotenv
def startHost():
    load_dotenv()
    HOST = "0.0.0.0"
    PORT = 5000

    buffer = 1024

    server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server.bind((HOST, PORT))
    server.setblocking(False)

    # pygame setup
    pygame.init()
    screen = pygame.display.set_mode((1280, 720))
    clock = pygame.time.Clock()
    running = True
    dt = 0
    timer = 0
    score = 0
    gameOver = False
    twoPlayers = False
    start_game = False

    player_pos = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)
    player_2_pos = pygame.Vector2(-1000, -1000)
    enemy_1_pos = pygame.Vector2(300, 360)
    enemy_2_pos = pygame.Vector2(980, 360)
    crystal = pygame.Vector2(640, 500)
    enemies = [[enemy_1_pos, 0], [enemy_2_pos, 0]]

    font = pygame.font.Font(None, 50)
    text_surface = None
    data = None

    def change_momentum(enemy_count):
        return [(random.random() * 4).__ceil__() for i in range(enemy_count)]
        
    while running:
        # poll for events
        # pygame.QUIT event means the user clicked X to close your window
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # fill the screen with a color to wipe away anything from last frame
        screen.fill("white")

        pygame.draw.circle(screen, "green", player_pos, 40)

        pygame.draw.circle(screen, "red", enemy_1_pos, 40)

        pygame.draw.circle(screen, "red", enemy_2_pos, 40)

        pygame.draw.circle(screen, "cyan", crystal, 30)

        
        text_surface = font.render(f"Score: {score}", True, (0, 0, 0))
        screen.blit(text_surface, (500, 550))  
        while True:
            try:
                data, addr = server.recvfrom(buffer)
            except (BlockingIOError, ConnectionResetError):
                break

        if data:
            player_2_data = data.decode().split(",")
            player_2_pos = pygame.Vector2(float(player_2_data[0]), float(player_2_data[1]))
            pygame.draw.circle(screen, "purple", player_2_pos, 40)
            twoPlayers = True
        speed = 500
        enemyTax = 200
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            start_game = True
        dt = clock.tick(60) / 1000
        timer += dt
        if not gameOver and twoPlayers and start_game:
            
            if keys[pygame.K_w] and player_pos.y > 40:
                player_pos.y -= speed * dt
                    
            if keys[pygame.K_s] and player_pos.y < 680:
                player_pos.y += speed * dt
                    
            if keys[pygame.K_a] and player_pos.x > 40:
                player_pos.x -= speed * dt    
                
            if keys[pygame.K_d] and player_pos.x < 1240:
                player_pos.x += speed * dt

            if timer >= 1.0 and twoPlayers:
                enemies[0][1], enemies[1][1] = change_momentum(2)
                timer = 0

            for enemy in enemies:
                if enemy[1] == 1:
                    if enemy[0].y > 40:
                        pass
                    else:
                        enemy[0].y = 680
                    enemy[0].y -= (speed - enemyTax) * dt
                if enemy[1] == 2:
                    if enemy[0].y < 680:
                        pass
                    else:
                        enemy[0].y = 40
                    enemy[0].y += (speed - enemyTax) * dt
                if enemy[1] == 3:
                    if enemy[0].x > 40:
                        pass
                    else:
                        enemy[0].x = 1240
                    enemy[0].x -= (speed - enemyTax) * dt
                if enemy[1] == 4:
                    if enemy[0].x < 1240:
                        pass
                    else:
                        enemy[0].x = 40
                    enemy[0].x += (speed - enemyTax) * dt

        for enemy in enemies:
            if math.sqrt((player_pos[0] - enemy[0][0])**2 + (player_pos[1] - enemy[0][1])**2) < 50:
                text_surface = font.render(f"Score: {score}\nGAME OVER", True, (0, 0, 0))
                screen.blit(text_surface, (500, 550))
                gameOver = True
            if math.sqrt((player_2_pos[0] - enemy[0][0])**2 + (player_2_pos[1] - enemy[0][1])**2) < 50:
                text_surface = font.render(f"Score: {score}\nGAME OVER", True, (0, 0, 0))
                screen.blit(text_surface, (500, 550))
                gameOver = True

        if math.sqrt((player_pos[0] - crystal[0])**2 + (player_pos[1] - crystal[1])**2) < 50:
            crystal[0] = (random.random() * 1280).__ceil__()
            crystal[1] = (random.random() * 720).__ceil__()
            score += 1

        if math.sqrt((player_2_pos[0] - crystal[0])**2 + (player_2_pos[1] - crystal[1])**2) < 50:
                crystal[0] = (random.random() * 1280).__ceil__()
                crystal[1] = (random.random() * 720).__ceil__()
                score += 1
        
                
        try:
            gameData = (f"{player_pos.x},{player_pos.y},{enemy_1_pos.x},{enemy_1_pos.y},{enemy_2_pos.x},{enemy_2_pos.y},{crystal.x},{crystal.y},{score},{gameOver},{start_game}").encode()
            server.sendto(gameData, (os.getenv("IP", "127.0.0.1"), 60000))
        except ConnectionResetError:
            pass

        pygame.display.flip()
   