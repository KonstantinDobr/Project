import pygame
import os
import sys
from random import randint

FPS = 50
WIDTH, HEIGHT = 800, 900
clock = pygame.time.Clock()


def blitRotate(surf, image, pos, originPos, angle, y):

    # offset from pivot to center
    image_rect = image.get_rect(
        topleft=(originPos))
    offset_center_to_pivot = pygame.math.Vector2(pos) - image_rect.center

    # roatated offset from pivot to center
    rotated_offset = offset_center_to_pivot.rotate(-angle)

    # roatetd image center
    rotated_image_center = (pos[0] - rotated_offset.x, y)

    # get a rotated image
    rotated_image = pygame.transform.rotate(image, angle)
    rotated_image_rect = rotated_image.get_rect(center=rotated_image_center)

    # Наложение на экран
    surf.blit(rotated_image, rotated_image_rect)

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

# Установка текста


def setText(screen, text, font):
    # Установка шрифта
    font = pygame.font.SysFont(font, 70)
    # Поверхность с текстом
    string_rendered = font.render(text, 0, pygame.Color('white'))
    # Размеры текста
    intro_rect = string_rendered.get_rect()
    # Отступ сверху
    intro_rect.top = 150
    # Центрирование
    intro_rect.x = WIDTH / 2 - intro_rect.width / 2
    # Наложение на экран текста
    screen.blit(string_rendered, intro_rect)

# Выход из приложения


def terminate():
    pygame.quit()
    sys.exit()


def game_killer(screen, score):
    # Заголовок окна
    pygame.display.set_caption('end window')
    # Загрузка текста
    # text = pygame.transform.scale(load_image('text.png'), (600, 120))
    image = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA, 32)
    image = image.convert_alpha()
    transparency = 0
    pygame.time.set_timer(pygame.USEREVENT, 100)



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
                pass
            if event.type == pygame.USEREVENT and transparency != 255:
                transparency += 1

        image = pygame.Surface((WIDTH, HEIGHT))
        image = image.convert_alpha()
        image.fill((255, 255, 255, transparency))
        screen.blit(image, (0, 0))
        # Отрисовка кадров
        clock.tick(FPS)
        pygame.display.flip()
