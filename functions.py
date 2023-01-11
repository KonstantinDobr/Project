import pygame
import os
import sys

WIDTH, HEIGHT = 800, 900

# Поворот


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

# Выход из приложения


def terminate():
    pygame.quit()
    sys.exit()

# Установка текста


def setText(screen, text, font, font_size, color, x, y, center=False):
    # Установка шрифта
    font = pygame.font.SysFont(font, font_size)
    # Поверхность с текстом
    string_rendered = font.render(text, 0, pygame.Color(color))
    # Размеры текста
    intro_rect = string_rendered.get_rect()
    # Расположение
    intro_rect.x = x
    if center:
        intro_rect.x = WIDTH // 2 - string_rendered.get_width() // 2
    intro_rect.y = y
    # Наложение на экран текста
    screen.blit(string_rendered, intro_rect)
