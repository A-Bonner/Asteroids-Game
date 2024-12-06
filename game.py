import pygame
import random
from asteroid import Asteroid
from ship import Ship
from bullet import Bullet

running = True
start = True
playing = False
paused = False
done = False

ready1 = False
ready2 = False


pygame.init()

window = pygame.display.set_mode()
dimensions = pygame.display.get_window_size()
score = 0
totalScore = 0
fontSmall = pygame.font.Font(None, 24)
fontMedium = pygame.font.Font(None, 60)
fontBig = pygame.font.Font(None, 96)

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
    for event in pygame.event.get():
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_SPACE:
                if playing:
                    bullets.add(Bullet("Bullet.png", ship.sprite.getPos()[0], ship.sprite.getPos()[1]))
                if start:
                    playing = True
                    start = False
                if paused:
                    playing = True
                    paused = False
                    ready1 = False
                    ready2 = False
            if event.key == pygame.K_ESCAPE:
                if start:
                    running = False
                if playing:
                    paused = True
                    playing = False
                if paused and ready1 and ready2:
                    running = False
                if paused and not ready1:
                    ready1 = True
                if paused and ready1 and not ready2:
                    ready2 = True
                if done:
                    running = False


    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP]:
        if playing:
            move[1] = -2
    if keys[pygame.K_DOWN]:
        if playing:
            move[1] = 2
    if keys[pygame.K_RIGHT]:
        if playing:
            move[0] = 2
    if keys[pygame.K_LEFT]:
        if playing:
            move[0] = -2


    if start:
        startText = fontBig.render("PRESS 'SPACE' TO START", True, 'gray80')
        controlText = fontMedium.render("use ARROW keys to move and 'SPACE' to shoot", True, 'gray80')
        goalText = fontMedium.render("AVOID ASTEROIDS to SURVIVE or DESTROY them to SCORE", True, 'gray80')
        window.blit(startText, (dimensions[0]/2 - startText.get_width()/2, dimensions[1]/2 - startText.get_height()/2))
        window.blit(controlText, (dimensions[0]/2 - controlText.get_width()/2, dimensions[1]/2 + startText.get_height()/2 + 3))
        window.blit(goalText, (dimensions[0]/2 - goalText.get_width()/2, dimensions[1]/2 + startText.get_height()/2 + controlText.get_height() + 3))

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
                        totalScore += rock.size
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

        if score >= 25:
            for rock in asteroids.sprites():
                rock.speedUp(1)
            ship.sprite.health += 1
            score = 0

        scoreText = fontSmall.render(("SCORE: " + str(totalScore)), True, "blue")
        hpText = fontSmall.render(("HP: " + str(ship.sprite.health)), True, "blue")
        window.blit(scoreText, (10, hpText.get_height()+10))
        window.blit(hpText, (10, 10))

        pygame.display.flip()

    if paused:
        pauseText = fontBig.render("PAUSED", True, 'white')
        playText = fontMedium.render("Press 'SPACE' to RESUME", True, 'white')
        exitText = fontMedium.render("Press 'ESCAPE' to EXIT", True, 'white')
        window.fill('black')
        window.blit(pauseText, (dimensions[0]/2 - pauseText.get_width()/2, 100))
        window.blit(playText, (dimensions[0]/2 - playText.get_width()/2, 100 + pauseText.get_height() + 2))
        window.blit(exitText, (dimensions[0]/2 - exitText.get_width()/2, 100 + pauseText.get_height() + playText.get_height()+ 2))

    if done:
        endText = fontBig.render("GAME OVER", True, "red")
        window.blit(endText, (dimensions[0]/2 - endText.get_width()/2, dimensions[1]/2 - endText.get_height()/2))
        finalScoreText = fontMedium.render("SCORE: " + str(totalScore), True, 'blue')
        window.blit(finalScoreText, (dimensions[0]/2 - finalScoreText.get_width()/2, dimensions[1]/2 + endText.get_height()/2 + 3))

    pygame.display.flip()
