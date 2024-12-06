import pygame


class Ship(pygame.sprite.Sprite):

    def __init__(self, model, health, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(model)
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()  # it MUST be self.rect for sprites
        self.rect.center = (x, y)
        self.health = health

    def update(self, move, bounds):
        x, y = self.rect.center
        if move[0] > 0 and self.rect.right < bounds[0]:
            x += move[0]
        if move[0] < 0 and self.rect.left > 0:
            x += move[0]
        if move[1] > 0 and self.rect.bottom < bounds[1]:
            y += move[1]
        if move[1] < 0 and self.rect.top > 0:
            y += move[1]
        self.rect.center = (x, y)

    def hit(self) -> int:
        self.health -= 1
        return self.health

    def getPos(self):
        return self.rect.center
