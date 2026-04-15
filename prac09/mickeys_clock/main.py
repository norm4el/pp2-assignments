import pygame
import os
from clock import MickeyClock

pygame.init()

WIDTH, HEIGHT = 800, 700
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Mickey's Clock")

fps_clock = pygame.time.Clock()

base_dir = os.path.dirname(os.path.abspath(__file__))
images_dir = os.path.join(base_dir, "images")

minute_hand_path = os.path.join(images_dir, "minute_hand.png")
second_hand_path = os.path.join(images_dir, "second_hand.png")

minute_hand = pygame.image.load(minute_hand_path).convert_alpha()
second_hand = pygame.image.load(second_hand_path).convert_alpha()

mickey_clock = MickeyClock(WIDTH // 2, HEIGHT // 2, minute_hand, second_hand)

running = True
while running:
    screen.fill((230, 230, 230))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    mickey_clock.draw(screen)

    pygame.display.flip()
    fps_clock.tick(1)

pygame.quit()