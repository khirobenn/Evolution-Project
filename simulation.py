import pygame
import model

WIDTH = 1500
HEIGHT = 900
RADIUS = 6
# pygame setup
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
running = True


while running:
    clock.tick(10)  # limits FPS to 60

    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if pygame.K_UP:
                g_adn, result, loop = model.meilleur_personne(WIDTH, HEIGHT, RADIUS, screen=screen)
                print("ADN trouvé!" , result[-1])
            elif pygame.K_DOWN:
                g_adn, result, loop = model.moran_v1(WIDTH, HEIGHT, RADIUSscreen=screen)
                print("ADN trouvé!" , result[-1])

pygame.quit()