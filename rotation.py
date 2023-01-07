import pygame
import os
import sys

pygame.init()
WIDTH, HEIGHT = 800, 900
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()


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


def blitRotate(surf, image, pos, originPos, angle):

    # offset from pivot to center
    image_rect = image.get_rect(
        topleft=(pos[0] - originPos[0], pos[1]-originPos[1]))
    offset_center_to_pivot = pygame.math.Vector2(pos) - image_rect.center

    # roatated offset from pivot to center
    rotated_offset = offset_center_to_pivot.rotate(-angle)

    # roatetd image center
    rotated_image_center = (pos[0] - rotated_offset.x,
                            300)

    # get a rotated image
    rotated_image = pygame.transform.rotate(image, angle)
    rotated_image_rect = rotated_image.get_rect(center=rotated_image_center)

    # Наложение на экран
    surf.blit(rotated_image, rotated_image_rect)


def main_window():
    # Загрузка картинки
    image = pygame.image.load('data/planet2.png')
    # Размеры картинки
    w, h = image.get_size()

    angle = 0
    done = False
    # Середина экрана
    pos = (screen.get_width()/2, screen.get_height()/2)

    fon = pygame.transform.scale(load_image('fon.jpg'), (WIDTH, HEIGHT))
    screen.blit(fon, (0, 0))

    while not done:
        # Отрисовка 60 кадров
        clock.tick(70)
        # Проверка на выход их программы
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True

        screen.blit(fon, (0, 0))
        blitRotate(screen, image, pos, (w/2, h/2), angle)

        angle -= 1
        pygame.display.flip()

    pygame.quit()
    exit()


main_window()