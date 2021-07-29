import pygame
from window_files.Circle import Circle
from functions.DFT import discrete_fourier_transform
import math
import numpy as np
from pygameZoom import PygameZoom
from PIL import Image, ImageOps
from functions.image_to_path import image_to_path
from functions.ImageVisibility import ImageVisibility


class Window:
    def __init__(self, img_path, image_visibility, static_path, reset_path):
        img = Image.open(img_path)
        mode = img.mode
        size = img.size
        data = img.tobytes()
        self.image = pygame.image.fromstring(data, size, mode)
        img = ImageOps.grayscale(img)

        path, self.dists = image_to_path(np.array(img))
        self.signal = [complex(p[0] - img.size[0] / 2, p[1] - img.size[1] / 2) for p in path]

        self.epicycles = discrete_fourier_transform(self.signal)

        pygame.init()
        self.W = size[0] + 100
        self.H = size[1] + 100
        self.WIN = pygame.display.set_mode((self.W, self.H))
        self.CLOCK = pygame.time.Clock()
        self.FPS = 30
        self.run = True
        self.pgZ = PygameZoom(self.W, self.H)
        self.pgZ.allow_zooming(False)
        self.pgZ.allow_dragging(False)

        #Parse args
        self.image_visibility = image_visibility
        self.static_path = static_path
        self.reset_path = reset_path

        self.speed = 2 * math.pi / len(self.epicycles)
        self.time = 0
        self.current_circle_position_index = 0
        self.path = []
        self.disappear_ratio = 120 / len(self.signal)
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
        if not self.static_path:
            for i, p in enumerate(self.path):
                p[2] = [abs(x - self.disappear_ratio) for x in p[2]]
                if i == self.current_circle_position_index:
                    p[2] = (255, 0, 0)

        if not self.one_full_cycle:
            self.path.append([self.circles[-1].x, self.circles[-1].y, (255, 0, 0)])

        if self.time > math.pi * 2:
            self.time = 0
            if self.reset_path:
                self.path = []
            else:
                self.one_full_cycle = True
            self.current_circle_position_index = 0

        self.time += self.speed
        self.current_circle_position_index += 1

    def refresh_window(self):
        self.WIN.fill(0)

        if self.image_visibility == ImageVisibility.VISIBLE:
            self.pgZ.blit(self.image, (self.W//2 - self.image.get_width() // 2, self.H//2 - self.image.get_height() // 2))

        # self.pgZ.follow_point(self.circles[-1].x, self.circles[-1].y, 5)
        for c in self.circles:
            c.draw(self.pgZ)

        for i in range(1, len(self.path) - 2):
            if self.dists[i] < 10:
                self.pgZ.draw_line(self.path[i][2], self.path[i - 1][0], self.path[i - 1][1], self.path[i][0],
                                   self.path[i][1], 3)

        self.pgZ.render(self.WIN, (0, 0))
        pygame.display.update()

    def loop(self):
        while self.run:
            self.events()
            self.move()
            self.refresh_window()
            self.CLOCK.tick(self.FPS)
