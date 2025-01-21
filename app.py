import pygame
from pygame.math import Vector2
from random import randint, uniform
import colorsys

HEIGHT = 700
WIDTH = 700

class Ball:
    def __init__(self, screen: pygame.Surface, 
                 coords: tuple[int, int],
                 radius: int,
                 velocity: tuple[int, int] = (0, 5),
                 hue: int = 250) -> None:
        self.screen = screen
        self.velocity = Vector2(velocity)
        self.velocity.rotate_ip(randint(-20, 20))
        self.coords = Vector2(coords)
        self.radius = radius
        self.color = tuple(x * 255 for x in colorsys.hsv_to_rgb(hue / 1000, uniform(0.5, 0.75), 1))

    def move(self, gravity: Vector2) -> None:
        self.coords += self.velocity
        self.velocity += gravity
        # self.velocity *= 0.999
        pygame.draw.circle(self.screen, self.color, self.coords, self.radius)

class App:

    def __init__(self):
        self.RADIUS = 300
        self.BALL_RADIUS = 2
        self.LIMIT = 10000
        self.hue = 250
        self.MID = Vector2(WIDTH // 2, HEIGHT // 2)
        pygame.init()
        self.display = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Ball multiplication")
        self.balls: list[Ball] = [Ball(self.display, (WIDTH // 2 + 50, HEIGHT // 2 + 50), self.BALL_RADIUS)]
        self.bg = pygame.Surface((WIDTH, HEIGHT))
        self.bg.fill((0, 0, 0))
        pygame.draw.circle(self.bg, (100, 0, 200), self.MID, self.RADIUS + self.BALL_RADIUS + 2, width=4)
        self.running = True
        self.clock = pygame.time.Clock()
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    self.balls = self.balls[0:1]
            self.display.blit(self.bg, (0, 0))
            temp_balls: list[Ball] = []
            for ball in self.balls:
                if (ball.coords.x - self.MID.x) ** 2 + (ball.coords.y - self.MID.y) ** 2 > self.RADIUS ** 2:
                    self.hue = self.hue + 1 if self.hue < 750 else 250
                    ball.velocity *= -0.99
                    ball.coords += Vector2(self.MID.x - ball.coords.x, 
                                                       self.MID.y - ball.coords.y).normalize() * ball.velocity.length() 
                    temp_balls.append(Ball(self.display, 
                                           ball.coords.copy(), 
                                           randint(2, 4),
                                           ball.velocity.copy(),
                                           self.hue))
                ball.move(self.__get__velocity(1, ball))
            self.balls.extend(temp_balls)
            if len(self.balls) > self.LIMIT:
                self.balls = self.balls[-self.LIMIT:]
            print(len(self.balls))
            pygame.display.flip()
            self.clock.tick(90)
            
    def __get__velocity(self, mode: int, ball: Ball) -> Vector2:
        match mode:
            case 1:
                v = Vector2(self.MID.x - ball.coords.x, self.MID.x - ball.coords.y)
            case _:
                v = Vector2(0, 1)
        return v.normalize() * 0.0981 * 0.95

if __name__ == "__main__":
    app = App()

 