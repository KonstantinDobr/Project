import pygame
import os
import sys
import random as rm

FPS = 50
WIDTH, HEIGHT = 800, 900
clock = pygame.time.Clock()
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
# Создание группы, содержащей границы
vertical_borders = pygame.sprite.Group()

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


class Meteorite(pygame.sprite.Sprite):
    # подгрузка картинки
    image = load_image("meteorite.png")

    def __init__(self, *group):
        # НЕОБХОДИМО вызвать конструктор родительского класса Sprite.
        # Это очень важно!!!
        super().__init__(*group)
        # получение переменной из класса
        self.image = Meteorite.image
        # получение размеров изображения
        self.rect = self.image.get_rect()
        # изначальное расположение
        self.rect.x = rm.randint(0, 630)
        self.rect.y = -150
        # Скорости
        self.x_speed = rm.randint(-10, 10)
        self.y_speed = rm.randint(1, 10)
        # Скорость поворота и угол
        self.angle = 0
        self.change = rm.randint(-5, 5)

    def update(self):
        # перемещение
        self.rect = self.rect.move(self.x_speed, self.y_speed)
        if pygame.sprite.spritecollideany(self, vertical_borders):
            self.x_speed = -self.x_speed


class Border(pygame.sprite.Sprite):
    # строго вертикальный отрезок
    def __init__(self, x1, y1, x2, y2, group):
        # вертикальная стенка
        super().__init__(group)
        self.image = pygame.Surface([1, y2 - y1])
        self.rect = pygame.Rect(x1, y1, 1, y2 - y1)
