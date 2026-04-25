import pygame
import sys
import random
import time
from pygame.locals import *

pygame.init()
pygame.mixer.init()

FPS = 60
FramePerSec = pygame.time.Clock()

BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
ORANGE = (255, 165, 0)

SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600

SPEED = 5
SCORE = 0
NEXT_SPEED_SCORE = 5   # после каждых 5 очков увеличиваем скорость

DISPLAYSURF = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("F1 Racer")

font_big = pygame.font.SysFont("Arial", 60)
font_small = pygame.font.SysFont("Arial", 30)
game_over_text = font_big.render("Game Over", True, BLACK)

background = pygame.image.load("AnimatedStreet.png")
player_img = pygame.image.load("Player.png")
enemy_img = pygame.image.load("Enemy.png")

coin_sound = pygame.mixer.Sound("coin.wav")
crash_sound = pygame.mixer.Sound("crash.wav")


class Coin(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        # вес монеты = сколько очков она дает (рандомно 1, 2 или 3)
        self.weight = random.choice([1, 2, 3])

        # чем больше вес, тем больше сама монета
        self.radius = 10 + self.weight * 3

        side = self.radius * 2
        self.image = pygame.Surface((side, side), pygame.SRCALPHA)

        # рисуем монету (два круга,обводка и внутренняя часть)
        pygame.draw.circle(self.image, ORANGE, (self.radius, self.radius), self.radius)
        pygame.draw.circle(self.image, YELLOW, (self.radius, self.radius), self.radius - 3)

        # выводим цифру веса прямо на монете
        text = font_small.render(str(self.weight), True, BLACK)
        text_rect = text.get_rect(center=(self.radius, self.radius))
        self.image.blit(text, text_rect)

        # спавним монету случайно по ширине дороги сверху экрана
        x = random.randint(40, SCREEN_WIDTH - 40)
        y = -20
        self.rect = self.image.get_rect(center=(x, y))

    def move(self):
        # монета двигается вниз вместе с дорогой
        self.rect.move_ip(0, SPEED)

        # если ушла за экран — удаляем
        if self.rect.top > SCREEN_HEIGHT:
            self.kill()


class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = enemy_img
        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(40, SCREEN_WIDTH - 40), 0)

    def move(self):
        # враг движется вниз
        self.rect.move_ip(0, SPEED)

        # если уехал вниз то появляется снова сверху
        if self.rect.top > SCREEN_HEIGHT:
            self.rect.top = 0
            self.rect.center = (random.randint(40, SCREEN_WIDTH - 40), 0)


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = player_img
        self.rect = self.image.get_rect()
        self.rect.center = (160, 520)

    def move(self):
        pressed_keys = pygame.key.get_pressed()

        # движение влево и вправо, ноне выходим за границы экрана
        if pressed_keys[K_LEFT] and self.rect.left > 0:
            self.rect.move_ip(-5, 0)

        if pressed_keys[K_RIGHT] and self.rect.right < SCREEN_WIDTH:
            self.rect.move_ip(5, 0)


P1 = Player()
E1 = Enemy()

enemies = pygame.sprite.Group()
enemies.add(E1)

coins = pygame.sprite.Group()

all_sprites = pygame.sprite.Group()
all_sprites.add(P1)
all_sprites.add(E1)


def create_coin():
    # создаем новую монету и добавляем в группы
    new_coin = Coin()
    coins.add(new_coin)
    all_sprites.add(new_coin)


def show_score():
    # выводим счет и текущую скорость в правом верхнем углу
    score_text = font_small.render(f"Coins: {SCORE}", True, BLACK)
    speed_text = font_small.render(f"Speed: {round(SPEED, 1)}", True, BLACK)

    DISPLAYSURF.blit(score_text, (SCREEN_WIDTH - 130, 10))
    DISPLAYSURF.blit(speed_text, (SCREEN_WIDTH - 130, 40))


COIN_SPAWN = pygame.USEREVENT + 1
pygame.time.set_timer(COIN_SPAWN, 1500)


while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

        # каждые 1.5 секунды появляется новая монета
        if event.type == COIN_SPAWN:
            create_coin()

    DISPLAYSURF.blit(background, (0, 0))
    show_score()

    for entity in all_sprites:
        DISPLAYSURF.blit(entity.image, entity.rect)
        entity.move()

    # проверка столкновения с врагом → game over
    if pygame.sprite.spritecollideany(P1, enemies):
        crash_sound.play()
        time.sleep(0.5)

        DISPLAYSURF.fill(RED)
        DISPLAYSURF.blit(game_over_text, (60, 220))

        final_score_text = font_small.render(f"Coins collected: {SCORE}", True, BLACK)
        DISPLAYSURF.blit(final_score_text, (70, 320))

        pygame.display.update()
        time.sleep(3)

        pygame.quit()
        sys.exit()

    # проверка столкновения с монетами
    collected_coins = pygame.sprite.spritecollide(P1, coins, True)

    if collected_coins:
        coin_sound.play()

        # увеличиваем счет с учетом веса каждой монеты
        for c in collected_coins:
            SCORE += c.weight

        # каждые N очков увеличиваем скорость врагов
        if SCORE >= NEXT_SPEED_SCORE:
            SPEED += 1
            NEXT_SPEED_SCORE += 5

    pygame.display.update()
    FramePerSec.tick(FPS)