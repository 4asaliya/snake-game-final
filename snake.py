import pygame, sys, random
from pygame.math import Vector2

# Добавляем начальный экран
class START_SCREEN:
    def __init__(self):
        # Загружаем и масштабируем фон
        self.background = pygame.image.load('Graphics/background.png').convert()
        self.background = pygame.transform.scale(self.background, (cell_number * cell_size, cell_number * cell_size))

        # Создаем кнопку "Старт"
        self.start_button = pygame.Rect((cell_number * cell_size // 4, cell_number * cell_size // 2), (cell_number * cell_size // 2, 50))

        # Загружаем изображение кнопки "Старт"
        self.start_button_image = pygame.image.load('Graphics/Button.png').convert_alpha()
        self.start_button_image = pygame.transform.scale(self.start_button_image, (self.start_button.width, self.start_button.height))

    def draw(self):
        # Заполняем экран фоном
        screen.blit(self.background, (0, 0))

        # Отображаем кнопку "Старт"
        screen.blit(self.start_button_image, self.start_button.topleft)

    def is_button_clicked(self, mouse_pos):
        if self.start_button.collidepoint(mouse_pos):
            return "start"
        return None

# Экран Game Over
class GAME_OVER_SCREEN:
    def __init__(self):
        # Загружаем и масштабируем фон
        self.background = pygame.image.load('Graphics/background2.png').convert()  # Используем PNG вместо JPG
        self.background = pygame.transform.scale(self.background, (cell_number * cell_size, cell_number * cell_size))

        # Создаем кнопку "Начать заново"
        self.restart_button = pygame.Rect((cell_number * cell_size // 4, cell_number * cell_size // 2), (cell_number * cell_size // 2, 50))

        # Загружаем изображение кнопки "Начать заново"
        self.restart_button_image = pygame.image.load('Graphics/finishbutton.png').convert_alpha()
        self.restart_button_image = pygame.transform.scale(self.restart_button_image, (self.restart_button.width, self.restart_button.height))

    def draw(self):
        # Заполняем экран фоном
        screen.blit(self.background, (0, 0))

        # Отображаем кнопку "Начать заново"
        screen.blit(self.restart_button_image, self.restart_button.topleft)

    def is_button_clicked(self, mouse_pos):
        if self.restart_button.collidepoint(mouse_pos):
            return "restart"
        return None

# Класс змейки
class SNAKE:
    def __init__(self):
        self.body = [Vector2(5, 10), Vector2(4, 10), Vector2(3, 10)]
        self.direction = Vector2(1,0)
        self.new_block = False

        self.head_up = pygame.image.load('Graphics/head.up.png').convert_alpha()
        self.head_down = pygame.image.load('Graphics/head.down.png').convert_alpha()
        self.head_right = pygame.image.load('Graphics/head.right.png').convert_alpha()
        self.head_left = pygame.image.load('Graphics/head.left.png').convert_alpha()

        self.tail_up = pygame.image.load('Graphics/tail.up.png').convert_alpha()
        self.tail_down = pygame.image.load('Graphics/tail.down.png').convert_alpha()
        self.tail_right = pygame.image.load('Graphics/tail.right.png').convert_alpha()
        self.tail_left = pygame.image.load('Graphics/tail.left.png').convert_alpha()

        self.body_vertical = pygame.image.load('Graphics/body_ver.png').convert_alpha()
        self.body_horizontal = pygame.image.load('Graphics/body_hor1.png').convert_alpha()

        self.body_tr = pygame.image.load('Graphics/bl.dleft.png').convert_alpha()
        self.body_tl = pygame.image.load('Graphics/bl.dright.png').convert_alpha()
        self.body_br = pygame.image.load('Graphics/bl.left.png').convert_alpha()
        self.body_bl = pygame.image.load('Graphics/bl.right.png').convert_alpha()
        self.crunch_sound = pygame.mixer.Sound('Sound/eating.mp3')

    def draw_snake(self):
        self.update_head_graphics()
        self.update_tail_graphics()

        for index, block in enumerate(self.body):
            x_pos = int(block.x * cell_size)
            y_pos = int(block.y * cell_size)
            block_rect = pygame.Rect(x_pos, y_pos, cell_size, cell_size)

            if index == 0:
                screen.blit(self.head, block_rect)
            elif index == len(self.body) - 1:
                screen.blit(self.tail, block_rect)
            else:
                previous_block = self.body[index + 1] - block
                next_block = self.body[index - 1] - block
                if previous_block.x == next_block.x:
                    screen.blit(self.body_vertical, block_rect)
                elif previous_block.y == next_block.y:
                    screen.blit(self.body_horizontal, block_rect)
                else:
                    if previous_block.x == -1 and next_block.y == -1 or previous_block.y == -1 and next_block.x == -1:
                        screen.blit(self.body_tl, block_rect)
                    elif previous_block.x == -1 and next_block.y == 1 or previous_block.y == 1 and next_block.x == -1:
                        screen.blit(self.body_bl, block_rect)
                    elif previous_block.x == 1 and next_block.y == -1 or previous_block.y == -1 and next_block.x == 1:
                        screen.blit(self.body_tr, block_rect)
                    elif previous_block.x == 1 and next_block.y == 1 or previous_block.y == 1 and next_block.x == 1:
                        screen.blit(self.body_br, block_rect)

    def update_head_graphics(self):
        head_relation = self.body[1] - self.body[0]
        if head_relation == Vector2(1, 0):
            self.head = self.head_left
        elif head_relation == Vector2(-1, 0):
            self.head = self.head_right
        elif head_relation == Vector2(0, 1):
            self.head = self.head_up
        elif head_relation == Vector2(0, -1):
            self.head = self.head_down

    def update_tail_graphics(self):
        tail_relation = self.body[-2] - self.body[-1]
        if tail_relation == Vector2(1, 0):
            self.tail = self.tail_left
        elif tail_relation == Vector2(-1, 0):
            self.tail = self.tail_right
        elif tail_relation == Vector2(0, 1):
            self.tail = self.tail_up
        elif tail_relation == Vector2(0, -1):
            self.tail = self.tail_down

    def move_snake(self):
        print(f"движение змейки:голова {self.body[0]},направление {self.direction}")
        if self.new_block:
            body_copy = self.body[:]
            body_copy.insert(0, body_copy[0] + self.direction)
            self.body = body_copy[:]
            self.new_block = False
        else:
            body_copy = self.body[:-1]
            body_copy.insert(0, body_copy[0] + self.direction)
            self.body = body_copy[:]

    def add_block(self):
        self.new_block = True

    def play_crunch_sound(self):
        self.crunch_sound.play()

    def reset(self):
        self.body = [Vector2(5, 10), Vector2(4, 10), Vector2(3, 10)]
        self.direction = Vector2(0, 0)

# Класс фрукта
class FRUIT:
    def __init__(self):
        self.randomize()

    def draw_fruit(self):
        fruit_rect = pygame.Rect(int(self.pos.x * cell_size), int(self.pos.y * cell_size), cell_size, cell_size)
        screen.blit(grapes, fruit_rect)

    def randomize(self):
        self.x = random.randint(0, cell_number - 1)
        self.y = random.randint(0, cell_number - 1)
        self.pos = Vector2(self.x, self.y)

# Основной класс игры
class MAIN:
    def __init__(self):
        self.snake = SNAKE()
        self.fruit = FRUIT()
        self.game_over = False

    def update(self):
        if not self.game_over:
            self.snake.move_snake()
            self.check_collision()
            self.check_fail()

    def draw_elements(self):
        self.draw_grass()
        self.fruit.draw_fruit()
        self.snake.draw_snake()
        self.draw_score()

    def check_collision(self):
        if self.fruit.pos == self.snake.body[0]:
            self.fruit.randomize()
            self.snake.add_block()
            self.snake.play_crunch_sound()

        for block in self.snake.body[1:]:
            if block == self.fruit.pos:
                self.fruit.randomize()

    def check_fail(self):
        if not 0 <= self.snake.body[0].x < cell_number or not 0 <= self.snake.body[0].y < cell_number:
            print("змейка вышла из поля")
            self.game_over = True

        for block in self.snake.body[1:]:
            if block == self.snake.body[0]:
                print(f"змейка столкнулась с самой собой:head{self.snake.body[0]},body {block}")
                self.game_over = True

    def reset(self):
        self.snake.reset()
        self.fruit.randomize()
        self.game_over = False

    def draw_grass(self):
        grass_color = (152, 255, 152)
        for row in range(cell_number):
            if row % 2 == 0:
                for col in range(cell_number):
                    if col % 2 == 0:
                        grass_rect = pygame.Rect(col * cell_size, row * cell_size, cell_size, cell_size)
                        pygame.draw.rect(screen, grass_color, grass_rect)
            else:
                for col in range(cell_number):
                    if col % 2 != 0:
                        grass_rect = pygame.Rect(col * cell_size, row * cell_size, cell_size, cell_size)
                        pygame.draw.rect(screen, grass_color, grass_rect)

    def draw_score(self):
        score_text = str(len(self.snake.body) - 3)
        score_surface = game_font.render(score_text, True, (56, 74, 12))
        score_x = int(cell_size * cell_number - 60)
        score_y = int(cell_size * cell_number - 40)
        score_rect = score_surface.get_rect(center=(score_x, score_y))
        apple_rect = grapes.get_rect(midright=(score_rect.left, score_rect.centery))
        bg_rect = pygame.Rect(apple_rect.left, apple_rect.top, apple_rect.width + score_rect.width + 6, apple_rect.height)

        pygame.draw.rect(screen, (167, 209, 61), bg_rect)
        screen.blit(score_surface, score_rect)
        screen.blit(grapes, apple_rect)
        pygame.draw.rect(screen, (56, 74, 12), bg_rect, 2)

# Инициализация Pygame
pygame.mixer.pre_init(44100, -16, 2, 512)
pygame.init()
cell_size = 38
cell_number = 19
screen = pygame.display.set_mode((cell_number * cell_size, cell_number * cell_size))
clock = pygame.time.Clock()
grapes = pygame.image.load('Graphics/grapes.png').convert_alpha()
game_font = pygame.font.Font('Font/PoetsenOne-Regular.ttf', 25)

SCREEN_UPDATE = pygame.USEREVENT
pygame.time.set_timer(SCREEN_UPDATE, 150)

start_screen = START_SCREEN()
game_over_screen = GAME_OVER_SCREEN()
main_game = MAIN()

# Игровой цикл
game_started = False
in_game_over = False

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == SCREEN_UPDATE and not in_game_over:
            print("событие scree_update сработало")
            main_game.update()

        if event.type == pygame.KEYDOWN :
            if event.key == pygame.K_w and main_game.snake.direction.y !=1:
                if main_game.snake.direction.y != 1:
                    main_game.snake.direction = Vector2(0, -1)
            if event.key == pygame.K_d and main_game.snake.direction.y !=1:
                if main_game.snake.direction.x != -1:
                    main_game.snake.direction = Vector2(1, 0)
            if event.key == pygame.K_s and main_game.snake.direction.y !=1:
                if main_game.snake.direction.y != -1:
                    main_game.snake.direction = Vector2(0, 1)
            if event.key == pygame.K_a and main_game.snake.direction.y !=1:
                if main_game.snake.direction.x != 1:
                    main_game.snake.direction = Vector2(-1, 0)

        if event.type == pygame.MOUSEBUTTONDOWN:
            if not game_started:
                mouse_pos = pygame.mouse.get_pos()
                button_clicked = start_screen.is_button_clicked(mouse_pos)

                if button_clicked == "start":
                    print("кнопка старт нажата")
                    game_started = True 
                if not game_started:
                    start_screen.draw()
                elif main_game.game_over:
                    in_game_over = True
                    game_over_screen.draw()
                else:
                    print("игровое поле отрисовывается")
                    screen.fill((85, 107, 47))
                    main_game.draw_elements()

            elif in_game_over:
                mouse_pos = pygame.mouse.get_pos()
                button_clicked = game_over_screen.is_button_clicked(mouse_pos)

                if button_clicked == "restart":
                    main_game.reset()
                    in_game_over = False
                    game_started = True

    pygame.display.update()
    clock.tick(60)