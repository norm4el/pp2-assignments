import pygame
import random

# просто цвета
colorBLACK  = (0, 0, 0)
colorWHITE  = (255, 255, 255)
colorGRAY   = (40, 40, 40)
colorRED    = (220, 50, 50)
colorYELLOW = (240, 200, 60)
colorGREEN  = (60, 200, 90)
colorCYAN   = (80, 220, 220)
colorORANGE = (255, 150, 30)

pygame.init()

WIDTH = 600
HEIGHT = 660
CELL = 30

GRID_COLS = WIDTH // CELL
PLAY_ROWS = 20

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake")

font_big = pygame.font.SysFont("consolas", 26, bold=True)
font_small = pygame.font.SysFont("consolas", 18)

FOODS_PER_LEVEL = 3
BASE_FPS = 5
SPEED_INCREMENT = 2
FOOD_LIFETIME = 5000  # через 5 сек еда исчезает


def draw_grid():
    # просто сетка для удобства
    for row in range(PLAY_ROWS):
        for col in range(GRID_COLS):
            pygame.draw.rect(screen, colorGRAY,
                             (col * CELL, row * CELL, CELL, CELL), 1)


def draw_hud(score, level, fps):
    # нижняя панель с инфой
    hud_y = PLAY_ROWS * CELL

    pygame.draw.rect(screen, (15, 15, 15), (0, hud_y, WIDTH, HEIGHT - hud_y))
    pygame.draw.line(screen, colorCYAN, (0, hud_y), (WIDTH, hud_y), 2)

    screen.blit(font_big.render(f"SCORE: {score}", True, colorCYAN), (10, hud_y + 8))
    screen.blit(font_big.render(f"LEVEL: {level}", True, colorORANGE), (220, hud_y + 8))
    screen.blit(font_small.render(f"speed {fps}", True, colorGRAY), (430, hud_y + 18))


def draw_overlay(lines, color=colorWHITE):
    # затемнение + текст (game over или level)
    overlay = pygame.Surface((WIDTH, PLAY_ROWS * CELL), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 160))
    screen.blit(overlay, (0, 0))

    total_h = len(lines) * 44
    start_y = (PLAY_ROWS * CELL - total_h) // 2

    for i, line in enumerate(lines):
        surf = font_big.render(line, True, color)
        rect = surf.get_rect(center=(WIDTH // 2, start_y + i * 44))
        screen.blit(surf, rect)


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y


class Snake:
    def __init__(self):
        mid = PLAY_ROWS // 2

        # начальная змейка
        self.body = [
            Point(10, mid),
            Point(9, mid),
            Point(8, mid)
        ]

        self.dx = 1
        self.dy = 0
        self.alive = True

        # сюда записываю сколько еще нужно вырасти
        self.pending_growth = 0

    def set_direction(self, dx, dy):
        # не даю развернуться назад
        if dx == -self.dx and dy == -self.dy:
            return

        self.dx = dx
        self.dy = dy

    def move(self):
        # сохраняю хвост, вдруг надо будет добавить
        old_tail = Point(self.body[-1].x, self.body[-1].y)

        # тело двигается за головой
        for i in range(len(self.body) - 1, 0, -1):
            self.body[i].x = self.body[i - 1].x
            self.body[i].y = self.body[i - 1].y

        # двигаю голову
        self.body[0].x += self.dx
        self.body[0].y += self.dy

        # если надо расти — добавляю сегмент
        if self.pending_growth > 0:
            self.body.append(old_tail)
            self.pending_growth -= 1

        head = self.body[0]

        # проверка на выход за карту
        if not (0 <= head.x < GRID_COLS and 0 <= head.y < PLAY_ROWS):
            self.alive = False
            return

        # проверка на себя
        for seg in self.body[1:]:
            if head.x == seg.x and head.y == seg.y:
                self.alive = False
                return

    def occupies(self, x, y):
        # проверяю занята ли клетка змейкой
        return any(p.x == x and p.y == y for p in self.body)

    def check_food(self, food):
        head = self.body[0]

        if head.x == food.pos.x and head.y == food.pos.y:
            # расту на вес еды
            self.pending_growth += food.weight
            return True

        return False

    def draw(self):
        head = self.body[0]

        pygame.draw.rect(screen, colorRED,
                         (head.x * CELL + 1, head.y * CELL + 1, CELL - 2, CELL - 2))

        for seg in self.body[1:]:
            pygame.draw.rect(screen, colorYELLOW,
                             (seg.x * CELL + 2, seg.y * CELL + 2, CELL - 4, CELL - 4))


class Food:
    def __init__(self):
        self.pos = Point(15, 10)
        self.weight = 1
        self.spawn_time = pygame.time.get_ticks()

    def generate_random_pos(self, snake):
        # случайный вес еды
        self.weight = random.choice([1, 2, 3])

        # запоминаю время появления
        self.spawn_time = pygame.time.get_ticks()

        while True:
            x = random.randint(0, GRID_COLS - 1)
            y = random.randint(0, PLAY_ROWS - 1)

            # чтобы не появлялась в змейке
            if not snake.occupies(x, y):
                self.pos.x = x
                self.pos.y = y
                return

    def is_expired(self):
        # если прошло больше времени — меняю еду
        return pygame.time.get_ticks() - self.spawn_time > FOOD_LIFETIME

    def draw(self):
        # цвет зависит от веса
        if self.weight == 1:
            c = colorGREEN
        elif self.weight == 2:
            c = colorORANGE
        else:
            c = colorCYAN

        pygame.draw.rect(screen, c,
                         (self.pos.x * CELL + 2, self.pos.y * CELL + 2, CELL - 4, CELL - 4))

        # пишу вес прямо на еде
        text = font_small.render(str(self.weight), True, colorBLACK)
        rect = text.get_rect(center=(self.pos.x * CELL + CELL // 2,
                                     self.pos.y * CELL + CELL // 2))
        screen.blit(text, rect)


def reset_game():
    snake = Snake()
    food = Food()
    food.generate_random_pos(snake)

    return snake, food, 0, 1, BASE_FPS, 0


clock = pygame.time.Clock()

snake, food, score, level, current_fps, foods_eaten = reset_game()

game_over = False
level_flash = 0

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if not game_over:
                if event.key in (pygame.K_RIGHT, pygame.K_d):
                    snake.set_direction(1, 0)
                elif event.key in (pygame.K_LEFT, pygame.K_a):
                    snake.set_direction(-1, 0)
                elif event.key in (pygame.K_DOWN, pygame.K_s):
                    snake.set_direction(0, 1)
                elif event.key in (pygame.K_UP, pygame.K_w):
                    snake.set_direction(0, -1)
            else:
                if event.key in (pygame.K_RETURN, pygame.K_SPACE):
                    snake, food, score, level, current_fps, foods_eaten = reset_game()
                    game_over = False
                    level_flash = 0

    if not game_over:
        snake.move()

        if not snake.alive:
            game_over = True
        else:
            if snake.check_food(food):
                # очки зависят от веса
                score += food.weight * 10
                foods_eaten += 1

                food.generate_random_pos(snake)

                # каждые 3 еды уровень растет
                if foods_eaten >= FOODS_PER_LEVEL:
                    level += 1
                    foods_eaten = 0
                    current_fps += SPEED_INCREMENT
                    level_flash = int(current_fps * 1.5)

            # если еду долго не съели — обновляю
            if food.is_expired():
                food.generate_random_pos(snake)

        if level_flash > 0:
            level_flash -= 1

    screen.fill(colorBLACK)
    draw_grid()
    food.draw()
    snake.draw()
    draw_hud(score, level, current_fps)

    if level_flash > 0 and not game_over:
        draw_overlay([f"LEVEL {level}!"], colorORANGE)

    if game_over:
        draw_overlay(["GAME OVER", f"Score: {score}"], colorRED)

    pygame.display.flip()
    clock.tick(current_fps)

pygame.quit()