import pygame
from functions import load_image, terminate, setText
import sqlite3
from game import main_window


FPS = 50
WIDTH, HEIGHT = 800, 900
clock = pygame.time.Clock()

# Подключение к БД
con = sqlite3.connect("database\scores.sqlite")

# Создание курсора
cur = con.cursor()
# Выполнение запроса и получение всех результатов
scores = list(cur.execute("""SELECT score FROM scores""").fetchall())

best_score = max(scores)[0]
last_score = scores[-1][0]

con.close()



def start_screen(screen):
    # Заголовок окна
    pygame.display.set_caption('start window')

    # Загрузка текста
    text = pygame.transform.scale(load_image('text.png'), (600, 120))
    # Загрузка картинки корабля
    starship_image = pygame.transform.scale(
        load_image('starship.png'), (150, 150))

    # Загрузка фона
    image = load_image('stars2.jpg')
    fon1 = pygame.transform.scale(
        image, (image.get_rect().width, image.get_rect().height))
    # Пользовательское событие
    pygame.time.set_timer(pygame.USEREVENT, 15)
    # setText(screen, 'Click to continue', pygame.font.get_fonts()[52])
    step1 = 0
    step2 = 1
    y_pos = 100
    while True:
        # внутри игрового цикла ещё один цикл
        # приема и обработки сообщений
        for event in pygame.event.get():
            # при закрытии окна
            if event.type == pygame.QUIT:
                # Выход из приложения
                terminate()
            if event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                # Продолжение
                if event.type == pygame.MOUSEBUTTONDOWN:
                    main_window(screen, step1, None)
                else:
                    main_window(screen, step1, event.key)
            if event.type == pygame.USEREVENT:
                # Отрисовка двух поверхностей
                screen.blit(fon1, (-13, step1 - 26))
                screen.blit(fon1, (-13, step1 - 952))
                # Увеличение сдвига по оси ординат
                step1 += 1
                # Сброс шага в крайней позиции
                if step1 == 952:
                    step1 = 30

                # Отрисовка текста
                setText(screen, 'Click to play', pygame.font.get_fonts()
                        [9], 70, 'white', 0, y_pos, True)
                # Сброс шага в крайней позиции
                if (y_pos == 100 and step2 == -1):
                    step2 = 1
                if (y_pos == 120 and step2 == 1):
                    step2 = -1
                # Сдвиг
                y_pos += step2

        # Лучший и последний счёт
        setText(screen, f'Best score: {best_score}', pygame.font.get_fonts()
                [9], 40, 'white', 100, 300)
        setText(screen, f'Last score: {last_score}', pygame.font.get_fonts()
                [9], 40, 'white', 100, 400)

        # Отрисовка звезолёта
        screen.blit(starship_image, (325, 750))
        # Отрисовка кадров
        clock.tick(FPS)
        pygame.display.flip()


pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
start_screen(screen)
