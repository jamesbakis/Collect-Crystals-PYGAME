import pygame
import os
import socket
from dotenv import load_dotenv

def startClient():
    load_dotenv()

    HOST = os.getenv("IP")
    PORT = 60000

    client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    client.bind((HOST, PORT))
    client.setblocking(False)

    pygame.init()
    screen = pygame.display.set_mode((1280, 720))
    font = pygame.font.Font(None, 50)
    running = True
    while running: 

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        try:
            data, addr = client.recvfrom(1024)
            
            print(data.decode(), "from", addr)

            
            gameData = data.decode()
            gameData = gameData.split(",")
            player_pos = pygame.Vector2(float(gameData[0]), float(gameData[1]))
            enemy_1_pos = pygame.Vector2(float(gameData[2]), float(gameData[3]))
            enemy_2_pos = pygame.Vector2(float(gameData[4]), float(gameData[5]))
            crystal = pygame.Vector2(float(gameData[6]), float(gameData[7]))
            score = int(gameData[8])
                
            screen.fill("orange")

            pygame.draw.circle(screen, "green", player_pos, 40)

            pygame.draw.circle(screen, "red", enemy_1_pos, 40)

            pygame.draw.circle(screen, "red", enemy_2_pos, 40)

            pygame.draw.circle(screen, "cyan", crystal, 30)

            text_surface = font.render(f"Score: {score}", True, (0, 0, 0))
            screen.blit(text_surface, (575, 550)) 

            pygame.display.flip()
        except BlockingIOError:
            pass
        

    client.close()

if __name__ == "__main__":
    startClient()