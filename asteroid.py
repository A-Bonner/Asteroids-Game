import pygame
import random


class Asteroid(pygame.sprite.Sprite):

    def __init__(self, size, model, x, y):
        pygame.sprite.Sprite.__init__(self)
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(model)
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.size = size
        if self.size == 3:
            self.health = 5
        if self.size == 2:
            self.health = 3
        if self.size == 1:
            self.health = 1
        self.speed = 1


    def update(self, hit):
        y = self.rect.centery
        y += self.speed
        self.rect.centery = y
        if hit:
            self.health -= 1

    def relocate(self, newX, newY):
        self.rect.center = (newX, newY)

    def offscreen(self, bound, newX, newY):
        if self.rect.top > bound:
            self.relocate(newX, newY)

    def speedUp(self, newSpeed):
        self.speed += newSpeed

    def destroy(self, newX, newY):
        self.relocate(newX, newY)
        if self.size == 3:
            self.health = 5
        if self.size == 2:
            self.health = 3
        if self.size == 1:
            self.health = 1
