import pygame
from functions import terminate, setText

FPS = 50
WIDTH, HEIGHT = 800, 900
clock = pygame.time.Clock()


def game_killer(screen, score):
    # Заголовок окна
    pygame.display.set_caption('end window')
    # Загрузка текста
    # text = pygame.transform.scale(load_image('text.png'), (600, 120))
    image = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA, 32)
    image = image.convert_alpha()
    transparency = 0
    pygame.time.set_timer(pygame.USEREVENT, 500)
    font_size = 30



    while True:
        # внутри игрового цикла ещё один цикл
        # приема и обработки сообщений
        for event in pygame.event.get():
            # при закрытии окна
            if event.type == pygame.QUIT:
                # Выход из приложения
                terminate()
            if event.type == pygame.USEREVENT and transparency != 255:
                transparency += 1
                

        # Отрисовка текста
        setText(screen, f'Your score: {score}', pygame.font.get_fonts()
                [9], font_size, 'black', 20, 380, True)
        if font_size != 80:
            font_size += 1

        # Отрисовка поверхности
        if transparency != 255:
            image = pygame.Surface((WIDTH, HEIGHT))
            image = image.convert_alpha()
            image.fill((255, 255, 255, transparency))
            screen.blit(image, (0, 0))
        
        # Отрисовка кадров
        clock.tick(FPS)
        pygame.display.flip()
