import pygame
from Circle import Circle

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
        self.circles = []
        self.init_circles()

        self.loop()

    def init_circles(self):
        rr = 200
        c = Circle(None, rr, (self.W/2, self.H/2))
        self.circles.append(c)

        for i in range(2, 5):
            c = Circle(self.circles[-1], rr//i+1)
            self.circles.append(c)

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.run = False

    def move(self):
        for c in self.circles:
            c.move(self.time)

        self.time += 0.02

    def refresh_window(self):
        self.WIN.fill(0)

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