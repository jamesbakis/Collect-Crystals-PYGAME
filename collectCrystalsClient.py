import pygame
import os
import socket
from dotenv import load_dotenv



def startClient():
    load_dotenv()

    HOST = os.getenv("IP")
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
    while running: 

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        try:
            data, addr = client.recvfrom(buffer)
            
            print(data.decode(), "from", addr)

            
            gameData = data.decode()
            gameData = gameData.split(",")
            
            player_pos = pygame.Vector2(float(gameData[0]), float(gameData[1]))
            enemy_1_pos = pygame.Vector2(float(gameData[2]), float(gameData[3]))
            enemy_2_pos = pygame.Vector2(float(gameData[4]), float(gameData[5]))
            crystal = pygame.Vector2(float(gameData[6]), float(gameData[7]))
            score = int(gameData[8])
                
            screen.fill("orange")

            pygame.draw.circle(screen, "purple", player_2, 40)

            pygame.draw.circle(screen, "green", player_pos, 40)

            pygame.draw.circle(screen, "red", enemy_1_pos, 40)

            pygame.draw.circle(screen, "red", enemy_2_pos, 40)

            pygame.draw.circle(screen, "cyan", crystal, 30)

            text_surface = font.render(f"Score: {score}", True, (0, 0, 0))
            screen.blit(text_surface, (575, 550)) 
            dt = clock.tick(60) / 1000
            keys = pygame.key.get_pressed()
            if keys[pygame.K_w] and player_2.y > 40:
                player_2.y -= speed * dt
                    
            if keys[pygame.K_s] and player_2.y < 680:
                player_2.y += speed * dt
                    
            if keys[pygame.K_a] and player_2.x > 40:
                player_2.x -= speed * dt    
                
            if keys[pygame.K_d] and player_2.x < 1240:
                player_2.x += speed * dt

            pygame.display.flip()
        except BlockingIOError:
            pass

        while True:
            try:
                # Drain the buffer: keep reading until it throws BlockingIOError
                client.recvfrom(buffer)
            except BlockingIOError:
                break

        player_data = (f"{player_2.x},{player_2.y}").encode()    
        client.sendto(player_data, (os.getenv("IP"), 5000))

    client.close()

if __name__ == "__main__":
    startClient()