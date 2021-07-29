import pygame
import math


class Circle:
    def __init__(self, parent, amplitude, phase, frequency, coords=(None, None)):
        self.r = amplitude
        self.phase = phase
        self.frequency = frequency
        self.parent = parent
        if parent is None:
            self.x = coords[0]
            self.y = coords[1]
        self.ending_x = 0
        self.ending_y = 0

    def move(self, time):
        if self.parent is not None:
            self.x = self.parent.ending_x
            self.y = self.parent.ending_y
        self.ending_x = self.x + self.r * math.cos(self.frequency * time + self.phase)
        self.ending_y = self.y + self.r * math.sin(self.frequency * time + self.phase)

    def draw(self, pgZ):
        pgZ.draw_circle((100, 100, 100), self.x, self.y, self.r, 1)
        pgZ.draw_line((100, 100, 100), self.x, self.y, self.ending_x, self.ending_y)
