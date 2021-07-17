import pygame
from Circle import Circle
from DFT import discrete_fourier_transform
import math
from pygameZoom import PygameZoom

pygame.init()


class Window:
    def __init__(self):
        self.W = 1000
        self.H = 800
        self.WIN = pygame.display.set_mode((self.W, self.H))
        self.CLOCK = pygame.time.Clock()
        self.FPS = 30
        self.run = True
        self.pgZ = PygameZoom(self.W, self.H)
        self.pgZ.allow_zooming(False)
        self.pgZ.allow_dragging(False)

        self.time = 0
        self.signal = []
        self.path = []
        self.epicycles = []
        self.speed = 0
        self.circles = []
        self.init_circles()

        self.status = "USER"

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
            c = Circle(parent, epicycle['amplitude'], epicycle['phase'], epicycle['frequency'], coords)
            self.circles.append(c)

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.run = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    self.status = "USER"
                    self.signal = []
                    self.path = []
                    self.circles = []
                    self.time = 0
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    self.status = "FOURIER"
                    self.path = []
                    self.epicycles = discrete_fourier_transform(self.signal)
                    self.speed = (2 * math.pi) / len(self.epicycles)
                    self.init_circles()
            elif event.type == pygame.MOUSEMOTION:
                if self.status == "USER" and pygame.mouse.get_pressed()[0]:
                    pos = pygame.mouse.get_pos()
                    self.signal.append(complex(pos[0], pos[1]))
                    self.path.append(pos)

    def move(self):
        for c in self.circles:
            c.move(self.time)

        self.path.append([self.circles[-1].x, self.circles[-1].y])

        if self.time > math.pi * 2:
            self.time = 0
            self.path = []

        self.time += self.speed

    def refresh_window(self):
        self.WIN.fill(0)

        for i in range(1, len(self.path)):
            self.pgZ.draw_line((255, 0, 0), self.path[i - 1][0], self.path[i-1][1], self.path[i][0], self.path[i][1])

        if self.status == "FOURIER":
            #self.pgZ.follow_point(self.circles[-1].x, self.circles[-1].y, 5)
            for c in self.circles:
                c.draw(self.pgZ)

        self.pgZ.render(self.WIN, (0, 0))
        pygame.display.update()

    def loop(self):
        while self.run:
            self.events()
            if self.status == "FOURIER":
                self.move()
            self.refresh_window()
            self.CLOCK.tick(self.FPS)


Window()
