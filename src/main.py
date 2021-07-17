import pygame
from Circle import Circle
from DFT import discrete_fourier_transform
import math

pygame.init()


class Window:
    def __init__(self):
        self.W = 1000
        self.H = 800
        self.WIN = pygame.display.set_mode((self.W, self.H))
        self.CLOCK = pygame.time.Clock()
        self.FPS = 30
        self.run = True

        self.time = 0
        self.signal = [100, 100, 100, -100, -100, -100, 100, 100, 100, -100, -100, -100]
        self.path = []
        self.epicycles = discrete_fourier_transform(self.signal)
        self.speed = (2 * math.pi) / len(self.epicycles)
        self.circles = []
        self.init_circles()

        self.loop()

    def init_circles(self):
        for i in range(len(self.epicycles)):
            if i == 0:
                parent = None
                coords = (self.W / 2, self.H / 2)
            else:
                parent = self.circles[i - 1]
                coords = None

            epicycle = self.epicycles[i]
            print(epicycle)
            c = Circle(parent, epicycle['amplitude'], epicycle['phase'], epicycle['frequency'], coords)
            self.circles.append(c)

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.run = False

    def move(self):
        for c in self.circles:
            c.move(self.time)

        if len(self.path) > 300:
            self.path.pop(0)

        for point in self.path:
            point[0] += 1
        self.path.append([700, self.circles[-1].y])

        if self.time > math.pi * 2:
            self.time = 0

        self.time += self.speed

    def refresh_window(self):
        self.WIN.fill(0)

        pygame.draw.line(self.WIN, (255, 0, 0), (self.circles[-1].x, self.circles[-1].y), (700, self.circles[-1].y))

        for i in range(1, len(self.path)):
            pygame.draw.line(self.WIN, (255, 0, 0), self.path[i - 1], self.path[i])

        for c in self.circles:
            c.draw(self.WIN)

        pygame.display.update()

    def loop(self):
        while self.run:
            self.events()
            self.move()
            self.refresh_window()
            self.CLOCK.tick(self.FPS)


Window()
