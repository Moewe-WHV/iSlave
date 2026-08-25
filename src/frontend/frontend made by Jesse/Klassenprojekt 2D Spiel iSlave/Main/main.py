import pygame

pygame.init()

BREITE, HOEHE = 800, 800
bildschirm = pygame.display.set_mode((BREITE, HOEHE))
pygame.display.set_caption("Unser Roboter-Spiel")
uhr = pygame.time.Clock()
schrift = pygame.font.SysFont("Arial", 20)

laeuft = True
while laeuft:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            laeuft = False

    bildschirm.fill((0, 0, 0))
    fps_text = schrift.render(f"FPS: {int(uhr.get_fps())}", True, (255, 255, 255))
    bildschirm.blit(fps_text, (10, 10))
    pygame.display.flip()

    uhr.tick(60)

pygame.quit()