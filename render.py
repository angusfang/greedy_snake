import pygame
pygame.init()
win = pygame.display.set_mode((500, 500))
pygame.display.set_caption("greedy snake Game")
DRAW = True

for t in range(999999):
    if t %1==0:
        if DRAW:
            x = 50
            y = 50
            width = 90
            height = 60
            vel = 5
            win.fill((0, 0, 0))  # Fills the screen with black
            pygame.draw.rect(win, (255, 0, 0), (x+0.01*t, y+0.01*t, width, height))
            pygame.display.update()



