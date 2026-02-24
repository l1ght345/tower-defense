import pygame

MAXFPS = 60
WINDOW_SIZE = (800,600)

class Sprite():
    def __init__(self,center,image):
        self.image = image
        self.rect = image.get_frect()
        self.rect.center = center

    def render(self,surface):
        surface.blit(self.image,self.rect)

window = pygame.Window('Товер дефенс',WINDOW_SIZE)
surface = window.get_surface()
clock = pygame.Clock()

running = True
player_image = pygame.surface([50,50])
player = Sprite(([WINDOW_SIZE[0]/2,WINDOW_SIZE[1]/2]),player_image)


while running:
    # Обработка событий
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    # Обновление обьектов

    # Отрисовка
    surface.fill('blue')

    player.render(surface)

    window.flip()

    clock.tick(MAXFPS)