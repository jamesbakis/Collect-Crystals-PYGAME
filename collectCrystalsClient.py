import pygame
import os
import socket
from dotenv import load_dotenv



def startClient():
    load_dotenv()

    HOST = "0.0.0.0"
    PORT = 60000
    buffer = 1024
    client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    client.bind((HOST, PORT))
    client.setblocking(False)

    pygame.init()
    screen = pygame.display.set_mode((1280, 720))
    font = pygame.font.Font(None, 50)
    clock = pygame.time.Clock()
    running = True
    speed = 500
    dt = 0
    player_2 = pygame.Vector2(screen.get_width() / 2, (screen.get_height() / 2) + 200)
    player_pos = pygame.Vector2(-1000, -1000)
    enemy_1_pos = pygame.Vector2(-1000, -1000)
    enemy_2_pos = pygame.Vector2(-1000, -1000)
    crystal = pygame.Vector2(-1000, -1000)
    p1Win = False
    p2Win = False
    score = 0
    score2 = 0
    data = None
    while running: 

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        while True:
            try:
                data, addr = client.recvfrom(buffer)
            except BlockingIOError:
                break
        if data:
            gameData = data.decode().split(",")
        
            player_pos = pygame.Vector2(float(gameData[0]), float(gameData[1]))
            enemy_1_pos = pygame.Vector2(float(gameData[2]), float(gameData[3]))
            enemy_2_pos = pygame.Vector2(float(gameData[4]), float(gameData[5]))
            crystal = pygame.Vector2(float(gameData[6]), float(gameData[7]))
            score = int(gameData[8])
            score2 = int(gameData[9])
            p1Win = gameData[10] == "True"
            p2Win = gameData[11] == "True"
            print(p1Win)
            print(p2Win)
                
        screen.fill("orange")

        pygame.draw.circle(screen, "purple", player_2, 40)
        pygame.draw.circle(screen, "green", player_pos, 40)
        pygame.draw.circle(screen, "red", enemy_1_pos, 40)
        pygame.draw.circle(screen, "red", enemy_2_pos, 40)
        pygame.draw.circle(screen, "cyan", crystal, 30)

        if p1Win:
            text_surface = font.render(f"Score: {score}\nPlayer 1 Wins!", True, (0, 0, 0))
        else:
            text_surface = font.render(f"Score: {score}", True, (0, 0, 0))
        screen.blit(text_surface, (300, 550))
        if p2Win:
            text_surface2 = font.render(f"Score: {score2}\nPlayer 2 Wins!", True, (0, 0, 0))
        else:
            text_surface2 = font.render(f"Score: {score2}", True, (0, 0, 0))
        screen.blit(text_surface2, (880, 550)) 
        dt = clock.tick(60) / 1000
        
        keys = pygame.key.get_pressed()
        if not (p1Win or p2Win):
            if keys[pygame.K_w] and player_2.y > 40:
                player_2.y -= speed * dt
                    
            if keys[pygame.K_s] and player_2.y < 680:
                player_2.y += speed * dt
                    
            if keys[pygame.K_a] and player_2.x > 40:
                player_2.x -= speed * dt    
                
            if keys[pygame.K_d] and player_2.x < 1240:
                player_2.x += speed * dt
        else: 
            pass
        pygame.display.flip()

        player_data = (f"{player_2.x},{player_2.y}").encode()    
        client.sendto(player_data, (os.getenv("IP", "127.0.0.1"), 5000))

    client.close()

if __name__ == "__main__":
    startClient()