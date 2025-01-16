import random
import pygame
import conf


# Отображение текста на окне
def message(msg, color, font_type, dis_width, dis_height):
    shown_text = font_type.render(msg, True, color)
    dis.blit(shown_text, [dis_width/10, dis_height/2])


# Отрисовка положения нашей змейки
def redraw_snake(snake_block, snake_list):
    for item in snake_list:
        pygame.draw.rect(dis, conf.blue, [item[0], item[1], snake_block, snake_block])


# Отображение счёта яблок
def show_score(score):
    score_font = pygame.font.SysFont("comicsansms", 20)
    value = score_font.render("Score: " + str(score), True, conf.green)
    dis.blit(value, [0, 0])


# Инициализация библиотеки и шрифта
pygame.init()
font_style = pygame.font.SysFont(None, 25)


# Настройки окна
dis = pygame.display.set_mode((conf.display_horizontal_size_x, conf.display_vertical_size_y))
pygame.display.set_caption('Snake game by Roman Rudyuk')


# Функция запуска игры
def game_session():
    # Установка настроек игры (Скорость змеи, ее размер, координаты и т.д.)
    x1 = conf.x1
    y1 = conf.y1
    x1_change = 0
    y1_change = 0
    snake_list = []
    snake_length = 1
    clock = pygame.time.Clock()
    game_speed = conf.game_speed
    game_over = False
    game_quit = False

    # Начальные координаты еды
    food_x = round(random.randrange(0, conf.display_horizontal_size_x - conf.snake_size) / 20.0) * 20.0
    food_y = round(random.randrange(0, conf.display_vertical_size_y - conf.snake_size) / 20.0) * 20.0

    # Основной цикл игры
    while game_over is False:
        # Отрисовка окна при проигрыше
        while game_quit is True:
            dis.fill(conf.black)
            message("Game Over - Нажми q - Выход или r - заново", conf.red, font_style,
                    conf.display_horizontal_size_x,
                    conf.display_vertical_size_y)
            show_score(snake_length - 1)
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    game_over = True
                    game_quit = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        game_over = True
                        game_quit = False
                    if event.key == pygame.K_r:
                        game_session()

        # Проверка событий окна, и настройки управления
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    if x1_change != 20:
                        x1_change = -20
                        y1_change = 0
                elif event.key == pygame.K_RIGHT:
                    if x1_change != -20:
                        x1_change = 20
                        y1_change = 0
                elif event.key == pygame.K_UP:
                    if y1_change != 20:
                        y1_change = -20
                        x1_change = 0
                elif event.key == pygame.K_DOWN:
                    if y1_change != -20:
                        y1_change = 20
                        x1_change = 0

        # Проверка сталкивания змеи со стенками
        if x1 >= conf.display_horizontal_size_x or x1 < 0 \
                or y1 >= conf.display_vertical_size_y or y1 < 0:
            game_quit = True
        
        # Передвижение змеи
        x1 += x1_change
        y1 += y1_change
        dis.fill(conf.black)
        pygame.draw.rect(dis, conf.red, [food_x, food_y, conf.snake_size, conf.snake_size])
        snake_head = (x1, y1)
        snake_list.append(snake_head)

        # Убираем последний элемент во время движения змеи
        if len(snake_list) > snake_length:
            del snake_list[0]

        # Проверка столкновения змеи с частью себя
        for element in snake_list[:-1]:
            if element == snake_head:
                game_quit = True

        # Отрисовка змеи, счета на окне и обновление экрана
        redraw_snake(conf.snake_size, snake_list)
        show_score(snake_length - 1)
        pygame.display.update()

        # Проверка поедания еды
        if x1 == food_x and y1 == food_y:
            food_x = round(random.randrange(0, conf.display_horizontal_size_x - conf.snake_size) / 20.0) * 20.0
            food_y = round(random.randrange(0, conf.display_vertical_size_y - conf.snake_size) / 20.0) * 20.0
            snake_length += 1
            game_speed += 2

        # Установка задержки между кадрами
        clock.tick(game_speed)

    # Выход из программы
    pygame.quit()
    quit()

# Запуск игры
if __name__ == "__main__":
    game_session()
