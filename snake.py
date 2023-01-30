# importing libraries
import pygame
import time
import random


class DisplayParams:
    def __init__(self):
        # Window size
        self.window_x = 720
        self.window_y = 480

        # defining colors
        self.black = pygame.Color(0, 0, 0)
        self.white = pygame.Color(255, 255, 255)
        self.red = pygame.Color(255, 0, 0)
        self.green = pygame.Color(0, 255, 0)
        self.blue = pygame.Color(0, 0, 255)

        # Initialise game window
        pygame.display.set_caption('Snake Game')
        self.game_window = pygame.display.set_mode((self.window_x, self.window_y))

        # FPS (frames per second) controller
        self.fps = pygame.time.Clock()


class Snake:
    def __init__(self, display_params):
        self.display_params = display_params
        self.speed = 15

        # defining snake default position
        self.position = [100, 50]

        # defining first 4 blocks of snake body
        # Notice that the snake's head is at body[0]. The tail is at body[-1]
        self.body = [[100, 50], [90, 50], [80, 50], [70, 50]]

        # setting default snake direction towards right
        self.direction = 'RIGHT'

    def add_to_head(self):
        self.body.insert(0, list(self.position))

    def trim_tail(self):
        self.body.pop()

    def draw(self):
        for pos in self.body:
            pygame.draw.rect(self.display_params.game_window, self.display_params.green,
                             pygame.Rect(pos[0], pos[1], 10, 10))


class Fruit:
    def __init__(self, display_params):
        self.display_params = display_params
        self.spawn = True
        self.position = None
        self.set_random_position()

    def set_random_position(self):
        self.position = [random.randrange(1, (self.display_params.window_x // 10)) * 10,
                         random.randrange(1, (self.display_params.window_y // 10)) * 10]

    def draw(self):
        pygame.draw.rect(self.display_params.game_window, self.display_params.white, pygame.Rect(
            self.position[0], self.position[1], 10, 10))


class Game:
    def __init__(self, display_params, snake, fruit):
        self.display_params = display_params
        self.snake = snake
        self.fruit = fruit

        self.score = 0

        self.change_to = self.snake.direction

    def game_over(self):
        # creating font object my_font
        my_font = pygame.font.SysFont('times new roman', 50)

        # creating a text surface on which text
        # will be drawn
        game_over_surface = my_font.render(
            'Your Score is : ' + str(self.score), True, self.display_params.red)

        # create a rectangular object for the text
        # surface object
        game_over_rect = game_over_surface.get_rect()

        # setting position of the text
        game_over_rect.midtop = (self.display_params.window_x / 2, self.display_params.window_y / 4)

        # blit will draw the text on screen
        self.display_params.game_window.blit(game_over_surface, game_over_rect)
        pygame.display.flip()

        # after 2 seconds we will quit the program
        time.sleep(2)

        # deactivating pygame library
        pygame.quit()

        # quit the program
        quit()

    # displaying Score function
    def show_score(self, color, font, size):
        # creating font object score_font
        score_font = pygame.font.SysFont(font, size)

        # create the display surface object
        # score_surface
        score_surface = score_font.render('Score : ' + str(self.score), True, color)

        # create a rectangular object for the text
        # surface object
        score_rect = score_surface.get_rect()

        # displaying text
        self.display_params.game_window.blit(score_surface, score_rect)

    def handle_key_event(self):
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.change_to = 'UP'
                if event.key == pygame.K_DOWN:
                    self.change_to = 'DOWN'
                if event.key == pygame.K_LEFT:
                    self.change_to = 'LEFT'
                if event.key == pygame.K_RIGHT:
                    self.change_to = 'RIGHT'

        # If two keys pressed simultaneously
        # we don't want snake to move into two
        # directions simultaneously
        if self.change_to == 'UP' and self.snake.direction != 'DOWN':
            self.snake.direction = 'UP'
        if self.change_to == 'DOWN' and self.snake.direction != 'UP':
            self.snake.direction = 'DOWN'
        if self.change_to == 'LEFT' and self.snake.direction != 'RIGHT':
            self.snake.direction = 'LEFT'
        if self.change_to == 'RIGHT' and self.snake.direction != 'LEFT':
            self.snake.direction = 'RIGHT'

    def move_snake(self):
        # Moving the snake
        if self.snake.direction == 'UP':
            self.snake.position[1] -= 10
        if self.snake.direction == 'DOWN':
            self.snake.position[1] += 10
        if self.snake.direction == 'LEFT':
            self.snake.position[0] -= 10
        if self.snake.direction == 'RIGHT':
            self.snake.position[0] += 10

    def do_snake_fruit_collide(self):
        rv = self.snake.position[0] == self.fruit.position[0] and \
            self.snake.position[1] == self.fruit.position[1]

        if rv:
            self.fruit.set_random_position()
            self.snake.speed += 1

        return rv

    def draw(self):
        self.display_params.game_window.fill(self.display_params.black)
        self.snake.draw()
        self.fruit.draw()

    def check_end_game(self):
        # Game Over conditions
        if self.snake.position[0] < 0 or self.snake.position[0] > self.display_params.window_x - 10:
            self.game_over()
        if self.snake.position[1] < 0 or self.snake.position[1] > self.display_params.window_y - 10:
            self.game_over()

        # Check if the snake's head (body[0] touches the snake body
        for block in self.snake.body[1:]:
            if self.snake.position[0] == block[0] and self.snake.position[1] == block[1]:
                self.game_over()

    def play(self):
        # Main Function
        while True:
            # handling key events
            self.handle_key_event()

            self.move_snake()

            # Snake body growing mechanism
            self.snake.add_to_head()

            # if fruits and snakes collide then scores
            # will be incremented by 10
            if self.do_snake_fruit_collide():
                self.score += 10
            else:
                self.snake.trim_tail()

            self.draw()
            self.check_end_game()

            # displaying score continuously
            self.show_score(self.display_params.white, 'times new roman', 20)

            # Refresh game screen
            pygame.display.update()

            # Frame Per Second /Refresh Rate
            self.display_params.fps.tick(self.snake.speed)


def main():
    pygame.init()

    display_params = DisplayParams()
    snake = Snake(display_params)
    fruit = Fruit(display_params)
    game = Game(display_params, snake, fruit)
    game.play()


main()
