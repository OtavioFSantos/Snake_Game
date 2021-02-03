import pygame
import time
import random
from pygame.locals import *

SIZE = 40

class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Snake Game")

        pygame.mixer.init()
        self.play_background_music()

        self.surface = pygame.display.set_mode((600, 600))
        self.snake = Snake(self.surface)
        self.snake.draw()
        self.apple = Apple(self.surface)
        self.apple.draw()
    
    def run(self):
        running = True
        pause = False

        while running:
            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        running = False

                    if event.key == K_RETURN:
                        pause = False
                        self.play_background_music()

                    if not pause:
                        if event.key == K_UP:
                            self.snake.move_up()

                        if event.key == K_DOWN:
                            self.snake.move_down()
                            
                        if event.key == K_LEFT:
                            self.snake.move_left()
                            
                        if event.key == K_RIGHT:
                            self.snake.move_right()
                        
                elif event.type == QUIT:
                    running = False
            
            try:
                if not pause:
                    self.play()
            except Exception as e:
                self.show_game_over()
                pause = True
                self.reset()
            
            time.sleep(0.15)

    def play(self):
        self.render_background()
        self.snake.walk()
        self.apple.draw()
        self.display_score()
        pygame.display.flip()

        if self.collision(self.snake.x[0], self.snake.y[0], self.apple.x, self.apple.y):
            self.play_sound("ding")
            self.snake.increase_length()
            var = True
            while var:
                var = False
                self.apple.move()
                for i in range(1, self.snake.length):
                    if self.collision(self.apple.x, self.apple.y, self.snake.x[i], self.snake.y[i]):
                        var = True

        self.out_of_bounds()

        for i in range(2, self.snake.length):
            if self.collision(self.snake.x[0], self.snake.y[0], self.snake.x[i], self.snake.y[i]):
                self.play_sound('crash')
                raise "Game Over"
        
    def out_of_bounds(self):
        if self.snake.x[0] >= 600:
            self.snake.x[0] = 0

        if self.snake.x[0] < 0:
            self.snake.x[0] = 600

        if self.snake.y[0] >= 600:
            self.snake.y[0] = 0
        
        if self.snake.y[0] < 0:
            self.snake.y[0] = 600
    
    def show_game_over(self):
        self.render_background()
        font = pygame.font.SysFont('arial', 30)
        line1 = font.render(f"Game Over! Your Score: {self.snake.length * 100 - 100}", True, (255, 255, 255))
        self.surface.blit(line1, (80, 220))
        font = pygame.font.SysFont('arial', 20)
        line2 = font.render(f"Press ENTER to play again!", True, (255, 255, 255))
        self.surface.blit(line2, (80, 280))
        pygame.mixer.music.pause()
        pygame.display.flip()

    def collision(self, x1, y1, x2, y2):
        if x1 >= x2 and x1 < x2 + SIZE:
            if y1 >= y2 and y1 < y2 + SIZE:
                return True
        
        return False
    
    def display_score(self):
        points = self.snake.length*100-100
        font = pygame.font.SysFont('arial', 20)
        score = font.render(f"Score: {points}", True, (255, 255, 255))
        self.surface.blit(score, (400, 30))
        
        if points > self.highscore():
            with open('resources/highscore.txt', 'w') as f:
                f.write(str(points))

        font = pygame.font.SysFont('arial', 20)
        hscore = font.render(f"Highest Score: {self.highscore()}", True, (255, 255, 255))
        self.surface.blit(hscore, (400, 10))
        pygame.display.flip()

    def reset(self):
        self.snake = Snake(self.surface)
        self.apple = Apple(self.surface)
    
    def play_background_music(self):
        pygame.mixer.music.load('resources/bg_music.ogg')
        pygame.mixer.music.play(-1, 0)
    
    def play_sound(self, sound_name):
        if sound_name == "crash":
            sound = pygame.mixer.Sound("resources/crash.ogg")
        elif sound_name == 'ding':
            sound = pygame.mixer.Sound("resources/ding.ogg")
        
        pygame.mixer.Sound.play(sound)
    
    def render_background(self):
        bg = pygame.image.load("resources/background.png")
        self.surface.blit(bg, (0, 0))

    def highscore(self):
        with open('resources/highscore.txt', 'r') as f:
            high_score = int(f.read())
        return high_score

class Snake:
    def __init__(self, parent_screen):
        self.length = 1
        self.parent_screen = parent_screen
        self.block = pygame.image.load("resources/block.png").convert()
        self.snake_head = pygame.image.load("resources/snakehead.png").convert()
        self.x = [SIZE]
        self.y = [SIZE]
        self.direction = 'right'

    def increase_length(self):
        self.length += 1
        self.x.append(-1)
        self.y.append(-1)
    
    def draw(self):
        self.parent_screen.blit(self.snake_head, (self.x[0], self.y[0]))
        for i in range(1, self.length):
            self.parent_screen.blit(self.block, (self.x[i], self.y[i]))
        pygame.display.flip()
    
    def move_left(self):
        if self.length == 1:
            self.direction = 'left'

        if not self.direction == 'right':
            self.direction = 'left'

    def move_right(self):
        if self.length == 1:
            self.direction = 'right'

        if not self.direction == 'left':
            self.direction = 'right'
    
    def move_up(self):
        if self.length == 1:
            self.direction = 'up'

        if not self.direction == 'down':
            self.direction = 'up'
    
    def move_down(self):
        if self.length == 1:
            self.direction = 'down'

        if not self.direction == 'up':
            self.direction = 'down'
    
    def walk(self):
        for i in range(self.length-1, 0, -1):
            self.x[i] = self.x[i - 1]
            self.y[i] = self.y[i - 1]

        if self.direction == 'right':
            self.x[0] += SIZE
        if self.direction == 'left':
            self.x[0] -= SIZE
        if self.direction == 'down':
            self.y[0] += SIZE
        if self.direction == 'up':
            self.y[0] -= SIZE
        self.draw()
    
class Apple:
    def __init__(self, parent_screen):
        self.image = pygame.image.load("resources/apple.png").convert_alpha()
        self.parent_screen = parent_screen
        self.x = SIZE*3
        self.y = SIZE*3
        
    def draw(self):
        self.parent_screen.blit(self.image, (self.x, self.y))
        pygame.display.flip()
    
    def move(self):
        self.x = random.randint(0, 12) * SIZE
        self.y = random.randint(0, 12) * SIZE

if __name__ == "__main__":
    game = Game()
    game.run()