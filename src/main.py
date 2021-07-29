import pygame
from Circle import Circle
from DFT import discrete_fourier_transform
import math
import numpy as np
from pygameZoom import PygameZoom
from PIL import Image, ImageOps
from image_to_path import image_to_path
pygame.init()


class Window:
    def __init__(self, img_path):
        self.W = 1000
        self.H = 800
        self.WIN = pygame.display.set_mode((self.W, self.H))
        self.CLOCK = pygame.time.Clock()
        self.FPS = 30
        self.run = True
        self.pgZ = PygameZoom(self.W, self.H)
        self.pgZ.allow_zooming(False)
        self.pgZ.allow_dragging(False)

        print("Reading image...")
        img = Image.open(img_path)
        mode = img.mode
        size = img.size
        data = img.tobytes()
        self.image = pygame.image.fromstring(data, size, mode)
        img = ImageOps.grayscale(img)
        print("Converting image to path...")
        path, self.dists = image_to_path(np.array(img))
        self.signal = [complex(p[0] - img.size[0]/2, p[1] - img.size[1]/2) for p in path]

        print("Calculating fourier transform for generated path...")
        self.epicycles = discrete_fourier_transform(self.signal)
        self.speed = 2 * math.pi / len(self.epicycles)
        self.time = 0
        self.current_circle_position_index = 0
        self.path = []
        self.disapear_ratio = 200 / len(self.signal)
        self.circles = []
        self.one_full_cycle = False
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
            c = Circle(parent, epicycle['amplitude'], epicycle['phase'], epicycle['frequency'], coords)
            self.circles.append(c)

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.run = False

    def move(self):
        for c in self.circles:
            c.move(self.time)

        # Make path less visible over time
        for i, p in enumerate(self.path):
            p[2] = [abs(x - self.disapear_ratio) for x in p[2]]
            if i == self.current_circle_position_index:
                p[2] = (255, 0, 0)

        if not self.one_full_cycle:
            self.path.append([self.circles[-1].x, self.circles[-1].y, (255, 0, 0)])

        if self.time > math.pi * 2:
            self.time = 0
            self.one_full_cycle = True
            self.current_circle_position_index = 0

        self.time += self.speed
        self.current_circle_position_index += 1

    def refresh_window(self):
        self.WIN.fill(0)

        #self.pgZ.blit(self.image, (self.W//2 - self.image.get_width() // 2, self.H//2 - self.image.get_height() // 2))

        for i in range(1, len(self.path) - 2):
            if self.dists[i] < 10:
                self.pgZ.draw_line(self.path[i][2], self.path[i - 1][0], self.path[i - 1][1], self.path[i][0],
                                   self.path[i][1], 3)

        # self.pgZ.follow_point(self.circles[-1].x, self.circles[-1].y, 5)
        for c in self.circles:
            c.draw(self.pgZ)

        self.pgZ.render(self.WIN, (0, 0))
        pygame.display.update()

    def loop(self):
        while self.run:
            self.events()
            self.move()
            self.refresh_window()
            self.CLOCK.tick(self.FPS)


Window('face.jpeg')
