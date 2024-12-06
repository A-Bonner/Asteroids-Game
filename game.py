import pygame
import random
from asteroid import Asteroid
from ship import Ship
from bullet import Bullet

pygame.init()
window = pygame.display.set_mode()
dimensions = pygame.display.get_window_size()
score = 0
fontSmall = pygame.font.Font(None, 24)
fontBig = pygame.font.Font(None, 96)

running = True
start = True
playing = False
paused = False
done = False

stars = []
for i in range(0, 200):
    star = [(random.randint(0, dimensions[0]), random.randint(0, dimensions[1])), random.randint(2, 5)]
    stars.append(star)

pressed = []

asteroids = pygame.sprite.Group()
for i in range(0, 10):
    size = random.randint(1, 4)
    if size == 1:
        asteroids.add(Asteroid(1, "Asteroid (small).png", random.randint(0, dimensions[0]), random.randint(-750, -49)))
    if size == 2:
        asteroids.add(Asteroid(2, "Asteroid (medium).png", random.randint(0, dimensions[0]), random.randint(-750, -49)))
    if size == 3:
        asteroids.add(Asteroid(3, "Asteroid (large).png", random.randint(0, dimensions[0]), random.randint(-750, -49)))

ship = pygame.sprite.GroupSingle()
bullets = pygame.sprite.Group()
ship.add(Ship("Ship.png", 10, dimensions[0]/2, dimensions[1]/2))
move = [0, 0]

while running:
    if start:
        startText = fontBig.render("PRESS 'SPACE' TO START", True, 'gray91')
        window.blit(startText, (dimensions[0]/2 - startText.get_width()/2, dimensions[1]/2 - startText.get_height()/2))
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            print('o_O')
            if pygame.K_SPACE not in pressed:
                print('UwU')
                pressed.append(pygame.K_SPACE)
        else:
            print('-_-')
            if pygame.K_SPACE in pressed:
                print('OwO')
                pressed.remove(pygame.K_SPACE)
                playing = True
                start = False
        pygame.display.flip()

    if playing:
        window.fill('black')
        for i in stars:
            pygame.draw.circle(window, 'white', i[0], i[1])
        ship.draw(window)
        ship.update(move, dimensions)
        move = [0, 0]

        bullets.draw(window)
        bullets.update()
        for bullet in bullets.sprites():
            for rock in asteroids.sprites():
                if pygame.sprite.collide_mask(bullet, rock) != None:
                    rock.update(True)
                    if rock.health == 0:
                        rock.destroy(random.randint(0, dimensions[0]), random.randint(-1000, -49))
                        score += rock.size
                    bullet.kill()

        asteroids.update(False)
        asteroids.draw(window)
        for rock in asteroids.sprites():
            rock.offscreen(dimensions[1], random.randint(0, dimensions[0]), random.randint(-1000, -49))
            if pygame.sprite.collide_mask(rock, ship.sprite) != None:
                rock.relocate(random.randint(0, dimensions[0]), random.randint(-1000, -49))
                remaining = ship.sprite.hit()
                if remaining == 0:
                    done = True
                    playing = False

        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP]:
            move[1] = -2
        if keys[pygame.K_DOWN]:
            move[1] = 2
        if keys[pygame.K_RIGHT]:
            move[0] = 2
        if keys[pygame.K_LEFT]:
            move[0] = -2

        if keys[pygame.K_SPACE]:
            if pygame.K_SPACE not in pressed:
                pressed.append(pygame.K_SPACE)
        else:
            if pygame.K_SPACE in pressed:
                pressed.remove(pygame.K_SPACE)
                bullets.add(Bullet("Bullet.png", ship.sprite.getPos()[0], ship.sprite.getPos()[1]))

        if keys[pygame.K_ESCAPE]:
            done = True
            playing = False

        if score >= 50:
            for rock in asteroids.sprites():
                rock.speedUp(1)
            ship.sprite.health += 1
            score = 0

        hpText = fontSmall.render(("HP: " + str(ship.sprite.health)), True, "white")
        window.blit(hpText, (10, 10))

        pygame.display.flip()

    if done:
        done = False
        running = False
