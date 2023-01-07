import pygame
import os
import sys
from random import randint

FPS = 50
WIDTH, HEIGHT = 800, 900
clock = pygame.time.Clock()
regulator = pygame.time.Clock()


def blitRotate(surf, image, pos, originPos, angle):

    # offset from pivot to center
    image_rect = image.get_rect(
        topleft=(originPos))
    offset_center_to_pivot = pygame.math.Vector2(pos) - image_rect.center

    # roatated offset from pivot to center
    rotated_offset = offset_center_to_pivot.rotate(-angle)

    # roatetd image center
    rotated_image_center = (pos[0] - rotated_offset.x,
                            HEIGHT - 150 / 2)

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


def main_window(screen, step1, key):
    # Заголовок окна
    pygame.display.set_caption('main window')

    # Загрузка фона
    image = load_image('stars2.jpg')
    fon1 = pygame.transform.scale(
        image, (image.get_rect().width, image.get_rect().height))

    # Пользовательские события
    pygame.time.set_timer(pygame.USEREVENT, 15)
    pygame.time.set_timer(pygame.USEREVENT + 1, 1000)
    # setText(screen, 'Click to continue', pygame.font.get_fonts()[52])

    class Starship(pygame.sprite.Sprite):
        # подгрузка картинки
        image = load_image("starship.png")

        def __init__(self, *group):
            # НЕОБХОДИМО вызвать конструктор родительского класса Sprite.
            # Это очень важно!!!
            super().__init__(*group)
            # получение переменной из класса
            self.image = Starship.image
            # получение размеров изображения
            self.rect = self.image.get_rect()
            # изначальное расположение
            self.rect.x = WIDTH / 2 - self.rect.width / 2
            self.rect.y = HEIGHT - self.rect.height
            # Поворот
            self.is_right = False
            self.is_left = False
            self.is_stop = False
            self.angle = 0
            self.is_shoot = False

        def update(self, key):
            # перемещение
            if key == pygame.K_d:
                self.is_right = 1
            if key == pygame.K_a:
                self.is_left = 1
            if key == pygame.K_SPACE:
                self.is_shoot = True

        def shooting(self):
            if regulator.tick() > 30:
                Bullet(bullets, self.rect.x + 35, self.rect.y + 20)
                Bullet(bullets, self.rect.x + 65, self.rect.y + 20)

    class Bullet(pygame.sprite.Sprite):
        # подгрузка картинки
        image = load_image("bullet.png")

        def __init__(self, group, x, y):
            # НЕОБХОДИМО вызвать конструктор родительского класса Sprite.
            # Это очень важно!!!
            super().__init__(group)
            # получение переменной из класса
            self.image = Bullet.image
            # получение размеров изображения
            self.rect = self.image.get_rect()
            # изначальное расположение
            self.rect.x = x
            self.rect.y = y
            self.is_del = False

        def update(self):
            # перемещение
            self.rect.y -= 15
            if self.is_del:
                self.rect.x = WIDTH * 20
                self.image = pygame.Surface([0, 0])
            if pygame.sprite.spritecollideany(self, meteors):
                self.is_del = True

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
            self.rect.x = randint(0, 630)
            self.rect.y = -150
            # Скорости
            self.x_speed = randint(-10, 10)
            self.y_speed = randint(1, 10)
            # Скорость поворота и угол
            self.angle = 0
            self.change = randint(-5, 5)
            self.damage = 0

        def update(self):
            # перемещение
            self.rect = self.rect.move(self.x_speed, self.y_speed)
            if pygame.sprite.spritecollideany(self, vertical_borders):
                self.x_speed = -self.x_speed
            if pygame.sprite.spritecollideany(self, bullets):
                self.damage += 1
                print(self.damage)
                if self.damage >= 1:
                    self.rect.x = WIDTH * 20
                    self.image = pygame.Surface([0, 0])

    class Border(pygame.sprite.Sprite):
        # строго вертикальный отрезок
        def __init__(self, x1, y1, x2, y2, group):
            # вертикальная стенка
            super().__init__(group)
            self.image = pygame.Surface([1, y2 - y1])
            self.rect = pygame.Rect(x1, y1, 1, y2 - y1)

    # создадим группу, содержащую все спрайты
    all_sprites = pygame.sprite.Group()
    # Создание группы, содержащей спрайты снарядов
    bullets = pygame.sprite.Group()
    # Создание группы, содержащей спрайты метеоритов
    meteors = pygame.sprite.Group()
    # Создание группы, содержащей границы
    vertical_borders = pygame.sprite.Group()

    # создадим спрайт, в группе all_sprites
    starship = Starship(all_sprites)
    # Создадим спрайты границ
    Border(0, -200, 0, HEIGHT, vertical_borders)
    Border(WIDTH, -200, WIDTH, HEIGHT, vertical_borders)

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
            if event.type == pygame.USEREVENT:
                # Отрисовка двух поверхностей
                screen.blit(fon1, (-13, step1 - 26))
                screen.blit(fon1, (-13, step1 - 952))
                # Увеличение сдвига по оси ординат
                step1 += 1
                # Сброс шага в крайней позиции
                if step1 == 952:
                    step1 = 30
            if event.type == pygame.KEYDOWN:
                # Обработка нажатия на клавишу
                key = event.key
                if key != pygame.K_SPACE:
                    starship.is_stop = False
            if event.type == pygame.KEYUP:
                key = None
                # Обработка остановки поворота
                if event.key == pygame.K_a:
                    starship.is_right = 0
                    starship.is_left = 2
                elif event.key == pygame.K_d:
                    starship.is_right = 2
                    starship.is_left = 0
                elif event.key == pygame.K_SPACE:
                    starship.is_shoot = False
                starship.is_stop = True
            if event.type == pygame.USEREVENT + 1:
                Meteorite(meteors)

        # Координаты точки поворота
        pos = (starship.rect.x + starship.rect.width / 2,
               starship.rect.y + starship.rect.height / 2)

        # Поворот направо
        if starship.is_right == 1 and starship.angle != 25:
            starship.angle += 1
            blitRotate(screen, starship.image, pos, (starship.rect.x,
                                                     starship.rect.y), -starship.angle)
        # Поворот налево
        elif starship.is_left == 1 and starship.angle != 25:
            starship.angle += 1
            blitRotate(screen, starship.image, pos, (starship.rect.x,
                                                     starship.rect.y), starship.angle)
        # Поворот направо при крайних значениях
        elif starship.is_right == 1 and starship.angle == 25:
            blitRotate(screen, starship.image, pos, (starship.rect.x,
                                                     starship.rect.y), -starship.angle)
        # Поворот налево при крайних значениях
        elif starship.is_left == 1 and starship.angle == 25:
            blitRotate(screen, starship.image, pos, (starship.rect.x,
                                                     starship.rect.y), starship.angle)
        # Состояние покоя
        elif starship.angle == 0:
            blitRotate(screen, starship.image, pos, (starship.rect.x,
                                                     starship.rect.y), starship.angle)
        # Возвращение в состояние покоя при повороте направо
        elif starship.is_stop and starship.is_right == 2 and starship.angle != 0:
            starship.angle -= 1
            blitRotate(screen, starship.image, pos, (starship.rect.x,
                                                     starship.rect.y), -starship.angle)
        # Возвращение в состояние покоя при повороте налево
        elif starship.is_stop and starship.is_left == 2 and starship.angle != 0:
            starship.angle -= 1
            blitRotate(screen, starship.image, pos, (starship.rect.x,
                                                     starship.rect.y), starship.angle)
        # Стабилизация
        elif starship.is_stop and starship.is_right == 2 and starship.angle == 0:
            starship.is_right == 0
        elif starship.is_stop and starship.is_left == 2 and starship.angle == 0:
            starship.is_left == 0

        if starship.is_shoot:
            starship.shooting()
        if starship.is_right == 1 and starship.rect.x + 10 < WIDTH - starship.rect.width:
            starship.rect.x += 10
        if starship.is_left == 1 and starship.rect.x - 10 > 0:
            starship.rect.x -= 10

        # вызов метода update для КАЖДОГО спрайта
        all_sprites.update(key)
        bullets.draw(screen)
        bullets.update()
        meteors.draw(screen)
        meteors.update()

        # Отрисовка кадров
        clock.tick(FPS)
        pygame.display.flip()


pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
main_window(screen, 0, None)