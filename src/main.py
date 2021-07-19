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
        self.current_circle_position_index = 0
        self.signal = []
        self.path = []
        self.epicycles = []
        self.speed = 0
        self.circles = []
        self.one_full_cycle = False
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
                    self.disapear_ratio = 255 / len(self.signal) * 0.9
                    self.init_circles()
            elif event.type == pygame.MOUSEMOTION:
                if self.status == "USER" and pygame.mouse.get_pressed()[0]:
                    pos = list(pygame.mouse.get_pos())
                    pos.append((255, 0, 0))
                    self.signal.append(complex(pos[0] - self.W/2, pos[1] - self.H/2))
                    self.path.append(pos)
                    self.one_full_cycle = False

    def move(self):
        for c in self.circles:
            c.move(self.time)

        if self.status == "FOURIER":
            #Make path less visible over time
            for i, p in enumerate(self.path):
                p[2] = [abs(x-self.disapear_ratio) for x in p[2]]
                if i == self.current_circle_position_index:
                    p[2] = (255, 0, 0)


        if not self.one_full_cycle:
            self.path.append([self.circles[-1].x, self.circles[-1].y, (255, 0, 0)])

        if self.time > math.pi * 2:
            self.time = 0
            self.one_full_cycle = True
            self.current_circle_position_index = 0

        self.time += self.speed
        self.current_circle_position_index += 1 if self.status == "FOURIER" else 0

    def refresh_window(self):
        self.WIN.fill(0)

        for i in range(1, len(self.path)-2):
            self.pgZ.draw_line(self.path[i][2], self.path[i - 1][0], self.path[i-1][1], self.path[i][0], self.path[i][1],3)

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
