import pygame
from window_files.Circle import Circle
import helper
import math
import numpy as np
import cv2
from pygameZoom import PygameZoom
from PIL import Image, ImageOps
from functions.image_to_path import image_to_path
from functions.ImageVisibility import ImageVisibility
import time

class Window:
    def __init__(self, img_path, image_visibility, static_path, reset_path, hide_circles, save_as_video):
        start = time.time()
        img = Image.open(img_path)
        mode = img.mode
        size = img.size
        data = img.tobytes()
        self.image = pygame.image.fromstring(data, size, mode)
        img = ImageOps.grayscale(img)

        path, self.dists = image_to_path(np.array(img))
        skip = round(len(path) / 7500) if len(path) > 7500 else 1
        self.signal = np.array([complex(path[i][0] - img.size[0] / 2, path[i][1] - img.size[1] / 2) for i in range(0, len(path), skip)], dtype=np.complex128)
        start1 = time.time()
        self.epicycles = helper.discrete_fourier_transform(self.signal)
        end1 = time.time()
        print(f"CALCULATING FOURIER: {round(end1-start1, 3)} sec")
        end = time.time()
        print(f"ALL CALCULATIONS: {round(end-start, 3)} sec")

        pygame.init()
        self.W = size[0] + 100
        self.H = size[1] + 100
        self.WIN = pygame.display.set_mode((self.W, self.H))
        self.CLOCK = pygame.time.Clock()
        self.FPS = 60
        self.run = True
        self.pgZ = PygameZoom(self.W, self.H)
        self.pgZ.allow_zooming(False)
        self.pgZ.allow_dragging(False)

        #Parse args
        self.image_visibility = image_visibility
        self.static_path = static_path
        self.reset_path = reset_path
        self.hide_circles = hide_circles
        self.save_as_video = save_as_video

        self.speed = 2 * math.pi / len(self.epicycles)
        self.time = 0
        self.current_circle_position_index = 0
        self.path = []
        self.disappear_ratio = 120 / len(self.signal)
        self.circles = []
        self.one_full_cycle = False
        self.init_circles()

        if self.save_as_video:
            self.codec = cv2.VideoWriter_fourcc(*'mp4v')
            self.video_name = f"ImageToFourier-{time.time()}.mp4"
            self.out = cv2.VideoWriter(self.video_name, self.codec, 200, (self.W, self.H))

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
            c = Circle(parent, epicycle[1], epicycle[2], epicycle[0], coords)
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

        if not self.hide_circles:
            for c in self.circles:
                c.draw(self.pgZ)

        for i in range(1, len(self.path) - 2):
            if self.dists[i] < 10:
                self.pgZ.draw_line(self.path[i][2], self.path[i - 1][0], self.path[i - 1][1], self.path[i][0],
                                   self.path[i][1], 3)

        surface = self.pgZ.generate_surface()
        if self.save_as_video:
            img = pygame.surfarray.array3d(surface).swapaxes(0,1)
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            self.out.write(img)
        self.WIN.blit(surface, (0, 0))
        pygame.display.update()

    def loop(self):
        while self.run:
            self.events()
            self.move()
            self.refresh_window()
            self.CLOCK.tick(self.FPS)
