import pygame
import sys
from pygame.locals import *
import time

# Инициализация Pygame
pygame.init()

# Определение размеров окна
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 400

# Определение цветов
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (150, 150, 150)

# Создание игрового окна в полноэкранном режиме
window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.FULLSCREEN)
pygame.display.set_caption('Pong')

clock = pygame.time.Clock()

# Определение параметров платформы
PADDLE_WIDTH = 100
PADDLE_HEIGHT = 5
PADDLE_SPEED = 5

# Создание платформы
paddle = pygame.Rect(WINDOW_WIDTH / 2 - PADDLE_WIDTH / 2, WINDOW_HEIGHT - PADDLE_HEIGHT, PADDLE_WIDTH, PADDLE_HEIGHT)

# Определение параметров мяча
BALL_RADIUS = 10
BALL_SPEED_X = 3
BALL_SPEED_Y = 3

# Создание мяча
ball = pygame.Rect(WINDOW_WIDTH / 2 - BALL_RADIUS / 2, WINDOW_HEIGHT / 2 - BALL_RADIUS / 2, BALL_RADIUS, BALL_RADIUS)
ball_speed_x = BALL_SPEED_X
ball_speed_y = BALL_SPEED_Y

# Состояния кнопок в меню
MENU_START = 0
MENU_ACCELERATE = 1
MENU_TWO_PLAYERS = 2
MENU_EXIT = 3
current_button = MENU_START

game_started = False
game_over = False

# Отрисовка меню
def draw_menu():
    window.fill(BLACK)
    font = pygame.font.Font(None, 36)

    text_start = font.render("Start", True, WHITE if current_button == MENU_START else GRAY)
    text_start_rect = text_start.get_rect(center=(WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2 - 50))
    window.blit(text_start, text_start_rect)

    text_accelerate = font.render("Acceleration", True, WHITE if current_button == MENU_ACCELERATE else GRAY)
    text_accelerate_rect = text_accelerate.get_rect(center=(WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2))
    window.blit(text_accelerate, text_accelerate_rect)

    text_two_players = font.render("Two Players", True, WHITE if current_button == MENU_TWO_PLAYERS else GRAY)
    text_two_players_rect = text_two_players.get_rect(center=(WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2 + 50))
    window.blit(text_two_players, text_two_players_rect)

    text_exit = font.render("Exit", True, WHITE if current_button == MENU_EXIT else GRAY)
    text_exit_rect = text_exit.get_rect(center=(WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2 + 100))
    window.blit(text_exit, text_exit_rect)

# Обновление позиции платформы при изменении размеров окна
def update_paddle_position():
    if pygame.display.get_surface().get_flags() & pygame.FULLSCREEN:
        paddle.x = WINDOW_WIDTH / 2 - PADDLE_WIDTH / 2
    else:
        paddle.x = WINDOW_WIDTH / 2 - PADDLE_WIDTH / 2

    paddle.y = WINDOW_HEIGHT - PADDLE_HEIGHT

# Переменные для отслеживания времени и ускорения мячика
start_time = 0
current_time = 0
BALL_ACCELERATION = 0.05

# Основной игровой цикл
while not game_over:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == KEYDOWN:
            if event.key == K_SPACE:
                if not game_started:
                    if current_button == MENU_START:
                        game_started = True
                    elif current_button == MENU_ACCELERATE:
                        BALL_SPEED_X = 3
                        BALL_SPEED_Y = 3
                        start_time = time.time()
                    elif current_button == MENU_TWO_PLAYERS:
                        pass
                    ball_speed_x = BALL_SPEED_X
                    ball_speed_y = BALL_SPEED_Y
                    ball.x = WINDOW_WIDTH / 2 - BALL_RADIUS / 2
                    ball.y = WINDOW_HEIGHT / 2 - BALL_RADIUS / 2
                    game_over = False

                else:
                    game_started = False
                    current_button = MENU_START
                    game_over = True

            elif event.key == K_UP:
                current_button = (current_button - 1) % 4
            elif event.key == K_DOWN:
                current_button = (current_button + 1) % 4
            elif event.key == K_RETURN:
                if current_button == MENU_EXIT:
                    pygame.quit()
                    sys.exit()

        elif event.type == VIDEORESIZE:
            # Обработка изменения размеров окна
            WINDOW_WIDTH = event.w
            WINDOW_HEIGHT = event.h
            window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.RESIZABLE)
            update_paddle_position()
            ball.x = WINDOW_WIDTH / 2 - BALL_RADIUS / 2
            ball.y = WINDOW_HEIGHT / 2 - BALL_RADIUS / 2

    if not game_started:
        window.fill(BLACK)
        draw_menu()
    else:
        window.fill(BLACK)
        keys = pygame.key.get_pressed()
        if keys[K_LEFT] and paddle.x > 0:
            paddle.x -= PADDLE_SPEED
        if keys[K_RIGHT] and paddle.x < WINDOW_WIDTH - PADDLE_WIDTH:
            paddle.x += PADDLE_SPEED

        ball.x += ball_speed_x
        ball.y += ball_speed_y

        if ball.y <= 0:
            ball_speed_y = -ball_speed_y
        if ball.x <= 0 or ball.x >= WINDOW_WIDTH - BALL_RADIUS:
            ball_speed_x = -ball_speed_x

        if ball.colliderect(paddle):
            ball_speed_y = -ball_speed_y

        if ball.y >= WINDOW_HEIGHT:
            game_started = False
            current_button = MENU_START

        # Увеличение скорости каждые 5 секунд в режиме "Acceleration"
        if current_button == MENU_ACCELERATE:
            current_time = time.time() - start_time
            if current_time >= 5:
                BALL_SPEED_X += BALL_SPEED_X * BALL_ACCELERATION
                BALL_SPEED_Y += BALL_SPEED_Y * BALL_ACCELERATION
                start_time = time.time()

        # Отображение секундомера
        timer_font = pygame.font.Font(None, 24)
        timer_text = timer_font.render(f"Time: {current_time:.2f}", True, WHITE)
        timer_text_rect = timer_text.get_rect(topright=(WINDOW_WIDTH - 10, 10))
        window.blit(timer_text, timer_text_rect)

        pygame.draw.rect(window, WHITE, paddle)
        pygame.draw.ellipse(window, WHITE, ball)

    pygame.display.flip()
    clock.tick(60)

    if game_over:
        game_over = False
        window.fill(BLACK)
        draw_menu()