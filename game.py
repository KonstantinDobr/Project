import pygame
from random import randint
from end import game_killer
from functions import blitRotate, load_image, terminate, setText
import sqlite3

FPS = 50
WIDTH, HEIGHT = 800, 900
SCORE = 0
clock = pygame.time.Clock()
regulator = pygame.time.Clock()


def main_window(screen, step1, key):
    # Заголовок окна
    pygame.display.set_caption('main window')

    # Загрузка фона
    image = load_image('stars2.jpg')
    fon1 = pygame.transform.scale(
        image, (image.get_rect().width, image.get_rect().height))

    # Пользовательские события
    pygame.time.set_timer(pygame.USEREVENT, 15)
    pygame.time.set_timer(pygame.USEREVENT + 1, 900)

    class Starship(pygame.sprite.Sprite):
        # подгрузка картинки
        image = load_image("starship.png")

        def __init__(self, *group):
            # НЕОБХОДИМО вызвать конструктор родительского класса Sprite.
            # Это очень важно!!!
            super().__init__(*group)
            # получение переменной из класса
            self.image = Starship.image
            self.mask = pygame.mask.from_surface(self.image)
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
            if key == pygame.K_d or pygame.K_d in pygame.key.get_pressed():
                self.is_right = 1
            if key == pygame.K_a or pygame.K_a in pygame.key.get_pressed():
                self.is_left = 1
            if key == pygame.K_w or pygame.K_w in pygame.key.get_pressed():
                self.is_shoot = True

        def shooting(self):
            if regulator.tick() > 28:
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
                # "Удаление" экземпляра класса
                bullets.remove(self)
            if pygame.sprite.spritecollideany(self, meteors) or self.rect.y < -50:
                # Сигнал об удалении при столкновении
                self.rect.y -= 40
                self.is_del = True

    class Meteorite(pygame.sprite.Sprite):
        global SCORE
        # подгрузка картинки
        image = load_image("meteorite.png")
        boom = load_image("boom.png")

        def __init__(self, *group):
            # НЕОБХОДИМО вызвать конструктор родительского класса Sprite.
            # Это очень важно!!!
            super().__init__(*group)
            # получение переменной из класса
            self.image = Meteorite.image
            self.mask = pygame.mask.from_surface(self.image)
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
            self.is_del = 0

        def update(self):
            global SCORE
            # перемещение
            self.rect = self.rect.move(self.x_speed, self.y_speed)

            # Проверка на столкновение с игроком
            if pygame.sprite.collide_mask(self, starship) and self.damage < 16:

                # Подключение к БД
                con = sqlite3.connect("database\scores.sqlite")

                # Создание курсора
                cur = con.cursor()
                # Добавление резултата в таблицу
                cur.execute(
                    f"""INSERT INTO scores(score) VALUES({SCORE})""")
                con.commit()
                con.close()

                game_killer(screen, SCORE)

            if pygame.sprite.spritecollideany(self, vertical_borders):
                if abs(self.x_speed // 1.5) > 2:
                    # Изменение направления и модуля скорости при столкновении
                    if self.x_speed > 0:
                        self.rect.x -= 5
                    else:
                        self.rect.x += 5
                    self.x_speed = -self.x_speed // 1.5
                else:
                    self.x_speed = -self.x_speed
                # Изменение скорости вращения при столкновении
                if self.change // 1.5 != 0:
                    self.change = self.change // 1.5
            if pygame.sprite.spritecollideany(self, bullets):
                # Увеличение урона при попадании
                self.damage += 1
            # "Удаление" экземпляра при столкновении
            if self.damage >= 16:
                meteors.remove(self)
                broken_meteors.add(self)
                self.is_del += 1
                self.image = Meteorite.boom
                self.angle, self.change, self.x_speed, self.y_speed = 0, 0, 0, 0
            if self.is_del == 40:
                broken_meteors.remove(self)
            pos = (self.rect.x + self.rect.width / 2,
                   self.rect.y + self.rect.height / 2)
            if self.rect.y > HEIGHT:
                meteors.remove(self)
            if self.damage == 16:
                SCORE += 1
            # Отрисовка метеорита с соответствующим поворотом
            blitRotate(screen, self.image, pos, (self.rect.x,
                       self.rect.y), self.angle, self.rect.y)
            # Изменение угла поворота
            self.angle += self.change

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
    # Создание группы, содержащей спрайты уничтоженных метеоритов
    broken_meteors = pygame.sprite.Group()

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
                if key in [pygame.K_a, pygame.K_d]:
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
                elif event.key == pygame.K_w:
                    starship.is_shoot = False
                starship.is_stop = True
            if event.type == pygame.USEREVENT + 1:
                # Создание метеорита
                Meteorite(meteors)

        # Координаты точки поворота
        pos = (starship.rect.x + starship.rect.width / 2,
               starship.rect.y + starship.rect.height / 2)

        # Поворот направо
        if starship.is_right == 1 and starship.angle != 25:
            starship.angle += 1
            blitRotate(screen, starship.image, pos, (starship.rect.x,
                                                     starship.rect.y), -starship.angle, HEIGHT - 150 / 2)
        # Поворот налево
        elif starship.is_left == 1 and starship.angle != 25:
            starship.angle += 1
            blitRotate(screen, starship.image, pos, (starship.rect.x,
                                                     starship.rect.y), starship.angle, HEIGHT - 150 / 2)
        # Поворот направо при крайних значениях
        elif starship.is_right == 1 and starship.angle == 25:
            blitRotate(screen, starship.image, pos, (starship.rect.x,
                                                     starship.rect.y), -starship.angle, HEIGHT - 150 / 2)
        # Поворот налево при крайних значениях
        elif starship.is_left == 1 and starship.angle == 25:
            blitRotate(screen, starship.image, pos, (starship.rect.x,
                                                     starship.rect.y), starship.angle, HEIGHT - 150 / 2)
        # Состояние покоя
        elif starship.angle == 0:
            blitRotate(screen, starship.image, pos, (starship.rect.x,
                                                     starship.rect.y), starship.angle, HEIGHT - 150 / 2)
        # Возвращение в состояние покоя при повороте направо
        elif starship.is_stop and starship.is_right == 2 and starship.angle != 0:
            starship.angle -= 1
            blitRotate(screen, starship.image, pos, (starship.rect.x,
                                                     starship.rect.y), -starship.angle, HEIGHT - 150 / 2)
        # Возвращение в состояние покоя при повороте налево
        elif starship.is_stop and starship.is_left == 2 and starship.angle != 0:
            starship.angle -= 1
            blitRotate(screen, starship.image, pos, (starship.rect.x,
                                                     starship.rect.y), starship.angle, HEIGHT - 150 / 2)
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
        # Снаряды
        bullets.draw(screen)
        bullets.update()
        # Метеориты
        meteors.update()
        # Уничтоженные метеориты
        broken_meteors.update()

        # Вывод текущего счёта
        setText(screen, f'{SCORE}', pygame.font.get_fonts()
                [9], 50, 'white', 20, 20)

        # Отрисовка кадров
        clock.tick(FPS)
        pygame.display.flip()
