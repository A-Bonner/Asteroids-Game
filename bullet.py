import pygame


class Bullet(pygame.sprite.Sprite):

    def __init__(self, model, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(model)
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()  # it MUST be self.rect for sprites
        self.rect.center = (x, y)

    def update(self):
        self.rect.centery -= 5
        if self.rect.bottom < 0:
            self.kill()
