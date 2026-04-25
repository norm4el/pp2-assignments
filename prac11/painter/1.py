import pygame

def main():
    pygame.init()
    screen = pygame.display.set_mode((640, 480))
    pygame.display.set_caption("Paint")
    clock = pygame.time.Clock()

    radius = 2
    tool = 'pencil'
    color = (0, 0, 255)

    points = []
    shape_start = None

    canvas = pygame.Surface((640, 480))
    canvas.fill((0, 0, 0))

    palette_colors = [
        (255, 0, 0), (0, 255, 0), (0, 0, 255),
        (255, 255, 0), (255, 165, 0), (255, 255, 255)
    ]

    palette_rects = [pygame.Rect(10 + i * 30, 450, 25, 25) for i in range(len(palette_colors))]

    while True:
        pressed = pygame.key.get_pressed()
        mouse_buttons = pygame.mouse.get_pressed()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return

            if event.type == pygame.KEYDOWN:
                # переключение инструментов
                if event.key == pygame.K_p:
                    tool = 'pencil'
                elif event.key == pygame.K_r:
                    tool = 'rect'
                elif event.key == pygame.K_c:
                    tool = 'circle'
                elif event.key == pygame.K_e:
                    tool = 'eraser'
                elif event.key == pygame.K_s:
                    tool = 'square'
                elif event.key == pygame.K_t:
                    tool = 'triangle'
                elif event.key == pygame.K_y:
                    tool = 'eq_triangle'
                elif event.key == pygame.K_h:
                    tool = 'rhombus'

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    mx, my = event.pos

                    # проверяю, нажал ли на палитру
                    clicked_palette = False
                    for i, rect in enumerate(palette_rects):
                        if rect.collidepoint(mx, my):
                            color = palette_colors[i]
                            clicked_palette = True
                            break

                    # если не на палитре — начинаю рисование
                    if not clicked_palette:
                        if tool in ['pencil', 'eraser']:
                            points = [event.pos]
                        else:
                            shape_start = event.pos

            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1 and shape_start:
                    ex, ey = event.pos
                    sx, sy = shape_start

                    # обычный прямоугольник
                    if tool == 'rect':
                        pygame.draw.rect(canvas, color,
                                         (min(sx, ex), min(sy, ey),
                                          abs(ex - sx), abs(ey - sy)), 2)

                    # квадрат (беру минимальную сторону)
                    elif tool == 'square':
                        size = min(abs(ex - sx), abs(ey - sy))
                        pygame.draw.rect(canvas, color, (sx, sy, size, size), 2)

                    # прямоугольный треугольник
                    elif tool == 'triangle':
                        pygame.draw.polygon(canvas, color,
                                            [(sx, sy), (ex, ey), (sx, ey)], 2)

                    # равносторонний треугольник
                    elif tool == 'eq_triangle':
                        size = abs(ex - sx)
                        pygame.draw.polygon(canvas, color,
                                            [(sx, sy),
                                             (sx + size, sy),
                                             (sx + size // 2, sy - size)], 2)

                    # ромб
                    elif tool == 'rhombus':
                        cx = (sx + ex) // 2
                        cy = (sy + ey) // 2
                        pygame.draw.polygon(canvas, color,
                                            [(cx, sy), (ex, cy), (cx, ey), (sx, cy)], 2)

                    shape_start = None
                    points = []

            if event.type == pygame.MOUSEMOTION:
                if mouse_buttons[0]:
                    if tool == 'pencil' and points:
                        pygame.draw.line(canvas, color, points[-1], event.pos, 2)
                        points.append(event.pos)

                    # ластик просто рисует черным
                    elif tool == 'eraser':
                        pygame.draw.circle(canvas, (0, 0, 0), event.pos, 10)

        screen.blit(canvas, (0, 0))

        # рисую палитру
        for i, rect in enumerate(palette_rects):
            pygame.draw.rect(screen, palette_colors[i], rect)

        pygame.display.flip()
        clock.tick(60)

main()