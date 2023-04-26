import pygame
import sys
import random
from access_dict_by_dot import AccessDictByDot
from pygame.math import Vector2

cell_size = 15
cell_number = 20
start_direction = 'right'
colors = {
    "red": (255, 0, 0),
    'green': (0, 180, 0),
    'blue': (0, 0, 250)
}
colors = AccessDictByDot.load(colors)


class fruit:
    def __init__(self):
        self.x = random.randint(0, cell_number - 1)
        self.y = random.randint(0, cell_number - 1)
        self.pos = Vector2(self.x, self.y)

    def draw_fruit(self):
        fruit_rect = pygame.Rect(int(self.pos.x * cell_size), int(self.pos.y * cell_size), cell_size, cell_size)
        screen.blit(apple, fruit_rect)
        # pygame.draw.rect(screen, colors.red, fruit_rect)

    def randomize(self):
        self.x = random.randint(0, cell_number - 1)
        self.y = random.randint(0, cell_number - 1)
        while (self.x, self.y) in snake.body:
            self.x = random.randint(0, cell_number - 1)
            self.y = random.randint(0, cell_number - 1)
        self.pos = Vector2(self.x, self.y)


class snake:
    def __init__(self):
        self.new_block = False
        self.body = [Vector2(3, 9), Vector2(2, 9), Vector2(1, 9)]
        self.direction = Vector2(1, 0)

    def draw_snake(self):
        for x, y in self.body:
            snake_rect = pygame.Rect(int(x * cell_size), int(y * cell_size), cell_size, cell_size)
            pygame.draw.rect(screen, colors.blue, snake_rect)

            for i in range(4):
                pygame.draw.rect(screen, (0, 0, 0), (x * cell_size - i, y * cell_size - i, cell_size, cell_size), 1)

    def move_snake(self):
        global direction
        # print(self.new_block)
        if self.new_block is not True:
            body_copy = self.body[:-1]
            body_copy.insert(0, body_copy[0] + self.direction)
            self.body = body_copy

        elif self.new_block is True:
            # self.body.insert(0, self.body[0] + self.direction)
            # print(self.new_block)
            body_copy = self.body
            body_copy.insert(0, body_copy[0] + self.direction)
            self.body = body_copy
            self.new_block = False

        # change snake current pos
        if snake.direction == [0, -1]:
            direction = 'up'
        elif snake.direction == [0, 1]:
            direction = 'down'
        elif snake.direction == [-1, 0]:
            direction = 'left'
        elif snake.direction == [1, 0]:
            direction = 'right'

    def add_block(self):
        self.new_block = True


class MAIN:
    def __init__(self):
        self.snake = snake
        self.fruit = fruit
        self.score = 0

    def update(self):
        self.snake.move_snake()
        self.check_collide()
        self.check_fail()

    def draw_elements(self):
        self.fruit.draw_fruit()
        self.snake.draw_snake()

    def check_collide(self):
        if self.fruit.pos == self.snake.body[0]:
            self.fruit.randomize()
            self.snake.new_block = True
            self.score += 1

    def check_fail(self):
        x_pos = self.snake.body[0].x
        y_pos = self.snake.body[0].y
        if x_pos < 0 or x_pos > cell_number - 1 or y_pos < 0 or y_pos > cell_number - 1:
            self.game_over()
        if self.snake.body[0] in self.snake.body[1:]:
            self.game_over()

    def game_over(self):
        pygame.quit()
        input(f"Score: {self.score}")
        sys.exit()


def display_update():
    pygame.display.update()
    screen.fill(colors.green)


def lost():
    global has_lost
    # if has_lost is True:
    #     pygame.quit()
    has_lost = True


if __name__ == "__main__":
    pygame.init()

    screen = pygame.display.set_mode((cell_size * cell_number, cell_size * cell_number))
    apple = pygame.image.load('apple.png').convert_alpha()

    pygame.display.set_caption('Snake Game')
    pygame.display.set_icon(apple)

    clock = pygame.time.Clock()
    direction = start_direction
    fruit = fruit()
    snake = snake()
    main = MAIN()

    SCREEN_UPDATE = pygame.USEREVENT
    pygame.time.set_timer(SCREEN_UPDATE, 150)

    # print(snake.body[0])
    # for loop
    while True:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == SCREEN_UPDATE:
                # move snake with direction every x seconds
                main.update()
            if event.type == pygame.KEYDOWN:
                # check directions
                if event.key == pygame.K_UP or event.key == pygame.K_w and direction != 'down':
                    snake.direction = Vector2(0, -1)  # move up
                elif event.key == pygame.K_DOWN or event.key == pygame.K_s and direction != 'up':
                    snake.direction = Vector2(0, 1)
                elif event.key == pygame.K_LEFT or event.key == pygame.K_a and direction != 'right':
                    snake.direction = Vector2(-1, 0)
                elif event.key == pygame.K_RIGHT or event.key == pygame.K_d and direction != 'left':
                    snake.direction = Vector2(1, 0)
                # print(direction.upper())

        main.draw_elements()
        display_update()
