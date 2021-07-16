import pygame
import math


class Circle:
    def __init__(self, parent, r, coords=(None, None)):
        self.r = r
        self.parent = parent
        if parent is None:
            self.x = coords[0]
            self.y = coords[1]
        else:
            self.x = parent.ending_x
            self.y = parent.ending_y
        self.ending_x = self.x + self.r
        self.ending_y = self.y

    def move(self, time):
        if self.parent is not None:
            self.x = self.parent.ending_x
            self.y = self.parent.ending_y
        self.ending_x = self.x + self.r * math.sin(time)
        self.ending_y = self.y + self.r * math.cos(time)

    def draw(self, surface):
        pygame.draw.circle(surface, (255, 255, 255), (self.x, self.y), self.r, 1)
        pygame.draw.line(surface, (255, 255, 255), (self.x, self.y), (self.ending_x, self.ending_y))
