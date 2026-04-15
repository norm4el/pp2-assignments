import pygame
import math
import datetime


class MickeyClock:
    def __init__(self, center_x, center_y, minute_hand_img, second_hand_img):
        self.center_x = center_x
        self.center_y = center_y

        self.minute_hand_img = pygame.transform.smoothscale(minute_hand_img, (80, 220))
        self.second_hand_img = pygame.transform.smoothscale(second_hand_img, (55, 180))

        self.font = pygame.font.SysFont("arial", 36, bold=True)

    def draw_clock_face(self, screen):
        pygame.draw.circle(screen, (250, 250, 250), (self.center_x, self.center_y), 220)
        pygame.draw.circle(screen, (0, 0, 0), (self.center_x, self.center_y), 220, 4)

        for i in range(60):
            angle = math.radians(i * 6 - 90)

            if i % 5 == 0:
                inner = 180
                outer = 205
                width = 4
            else:
                inner = 190
                outer = 205
                width = 2

            x1 = self.center_x + inner * math.cos(angle)
            y1 = self.center_y + inner * math.sin(angle)
            x2 = self.center_x + outer * math.cos(angle)
            y2 = self.center_y + outer * math.sin(angle)

            pygame.draw.line(screen, (0, 0, 0), (x1, y1), (x2, y2), width)

        labels = {
            "12": (self.center_x, self.center_y - 150),
            "3": (self.center_x + 150, self.center_y),
            "6": (self.center_x, self.center_y + 150),
            "9": (self.center_x - 150, self.center_y)
        }

        for text, pos in labels.items():
            surf = self.font.render(text, True, (0, 0, 0))
            rect = surf.get_rect(center=pos)
            screen.blit(surf, rect)

    def draw_hand(self, screen, image, angle):
        pivot = pygame.math.Vector2(self.center_x, self.center_y)


        image_rect = image.get_rect(midbottom=(self.center_x, self.center_y))

        offset = pygame.math.Vector2(image_rect.center) - pivot

        rotated_offset = offset.rotate(angle)

        rotated_image = pygame.transform.rotate(image, -angle)

        rotated_rect = rotated_image.get_rect(center=pivot + rotated_offset)

        screen.blit(rotated_image, rotated_rect)

    def draw(self, screen):
        now = datetime.datetime.now()
        minute = now.minute
        second = now.second

        minute_angle = minute * 6
        second_angle = second * 6

        self.draw_clock_face(screen)

        
        self.draw_hand(screen, self.minute_hand_img, minute_angle)
        self.draw_hand(screen, self.second_hand_img, second_angle)

        pygame.draw.circle(screen, (0, 0, 0), (self.center_x, self.center_y), 8)
        pygame.draw.circle(screen, (200, 0, 0), (self.center_x, self.center_y), 4)