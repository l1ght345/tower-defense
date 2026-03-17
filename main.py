from random import randint
import pygame

maxfps = 60
window_SIZE = (800, 600)


class Sprite:
    def __init__(self, center, image):
        self.image = image
        self.rect = image.get_frect()
        self.rect.center = center

    def render(self, surface):
        surface.blit(self.image, self.rect)


class MoveSprite(Sprite):
    def __init__(self, center, image, speed, direction):
        super().__init__(center, image)

        self.speed = speed
        self.direction = direction

    def update(self):
        vector = self.direction * self.speed
        self.rect.move_ip(vector)


pygame.init()

window = pygame.Window("Tower Defense", window_SIZE)
surface = window.get_surface()
surface_rect = surface.get_rect()
clock = pygame.Clock()
font = pygame.Font(None, 32)

pygame.mixer.music.load('yesterbreeze.mp3')
pygame.mixer.music.set_volume(0.1)
pygame.mixer.music.play(-1)

player_image = pygame.image.load('player.webp').convert_alpha()
player_image = pygame.transform.scale(player_image,[50,50])

bullet_image = pygame.image.load('bullet.webp').convert_alpha()
bullet_image = pygame.transform.scale(bullet_image,[100,100]) 

enemy_image = pygame.image.load('enemy.webp').convert_alpha()
enemy_image = pygame.transform.scale(enemy_image,[50,50])

background_image = pygame.image.load('background.jpeg').convert_alpha()
background_image = pygame.transform.scale(background_image, window_SIZE)

player = Sprite([window_SIZE[0] / 2, window_SIZE[1] / 2], player_image)

bullets = []
enemies = []

running = True
score = 0

while running:
    # обработка событий
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            center = pygame.Vector2(player.rect.center)
            pos = pygame.Vector2(pygame.mouse.get_pos())
            vector = (pos - center).normalize()
            bullet = MoveSprite(center, bullet_image, 7, vector)
            bullets.append(bullet)

    # обновление объектов
    if randint(0, 100) <= 30:
        r = randint(1, 4)
        if r == 1:
            pos = pygame.Vector2(
                randint(0, window_SIZE[0]),
                -100,
            )
        if r == 2:
            pos = pygame.Vector2(
                window_SIZE[0] + 100,
                randint(0, window_SIZE[1]),
            )
        if r == 3:
            pos = pygame.Vector2(
                randint(0, window_SIZE[0]),
                window_SIZE[1] + 100,
            )
        if r == 4:
            pos = pygame.Vector2(
                -100,
                randint(0, window_SIZE[1]),
            )
        center = pygame.Vector2(player.rect.center)
        vector = (center - pos).normalize()
        speed = randint(200, 600) / 100
        enemy = MoveSprite(pos,enemy_image, speed, vector)
        enemies.append(enemy)

    for bullet in bullets:
        bullet.update()
        if not bullet.rect.colliderect(surface_rect):
            bullets.remove(bullet)
    for enemy in enemies:
        enemy.update()
    print('Кол-во пуль в игре',len(bullets))
    for enemy in enemies:
        for bullet in bullets:
            # colliderect - проверка на столкновение 2-х прямоугольников
            if bullet.rect.colliderect(enemy.rect):
                score += 1
                enemies.remove(enemy)
                bullets.remove(bullet)
                break

    for enemy in enemies:
        if player.rect.colliderect(enemy.rect):
            score = 0
            enemies.clear()
            bullets.clear()
            break

    # отрисовка
    surface.blit(background_image,(0,0))

    for bullet in bullets:
        bullet.render(surface)
    for enemy in enemies:
        enemy.render(surface)
    player.render(surface)

    text = "Баллы: " + str(score)
    image = font.render(text, True, "black")
    surface.blit(image, [10, 10])

    window.flip()
    clock.tick(maxfps)

