import pygame
import os
import sys
from random import *
from game import main_window

FPS = 50
WIDTH, HEIGHT = 800, 900
clock = pygame.time.Clock()

# Обработка изображения


def load_image(name, colorkey=None):
    # локальное имя
    fullname = os.path.join('data', name)
    # если файл не существует, то выходим
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    # загрузка изображения
    image = pygame.image.load(fullname)

    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            # первый пиксель
            colorkey = image.get_at((0, 0))
        # прозрачность фона
        image.set_colorkey(colorkey)
    else:
        #  сохранение прозрачности
        image = image.convert_alpha()
    # возвращение картинки
    return image

# Выход из приложения


def terminate():
    pygame.quit()
    sys.exit()

def start_screen(screen):
    # Заголовок окна
    pygame.display.set_caption('start window')

    # Загрузка текста
    text = pygame.transform.scale(load_image('text.png'), (600, 120))
    # Загрузка картинки корабля
    starship_image = pygame.transform.scale(load_image('starship.png'), (150, 150))

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
                screen.blit(text, (100, y_pos))
                # Сброс шага в крайней позиции
                if (y_pos == 100 and step2 == -1):
                    step2 = 1
                if (y_pos == 120 and step2 == 1):
                    step2 = -1
                # Сдвиг
                y_pos += step2

        # Отрисовка звезолёта
        screen.blit(starship_image, (325,  750))
        # Отрисовка кадров
        clock.tick(FPS)
        pygame.display.flip()


pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
start_screen(screen)
