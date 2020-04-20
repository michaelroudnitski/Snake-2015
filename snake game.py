#########################################
# Programmer: Michael Roudnitski
# Date: 21/09/2012
# File Name: snake_template.py
# Description: This program is a template for Snake Game.
#               It demonstrates how to move and lengthen the snake. 
#########################################

import time
from random import randint

import pygame

pygame.init()

intro = True
inPlay = False

HEIGHT = 600
WIDTH = 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
WHITE = (255, 255, 255)
BLACK = (40, 40, 4)
RED = (231, 76, 60)
GREEN = (0, 255, 0)
BLUE = (44, 62, 80)
ORANGE = (241, 196, 15)
outline = 0
score = 1
appleEaten = True
difficulty = 50
font = pygame.font.SysFont("Myriad", 60)
introFont = pygame.font.SysFont("Myriad", 36)
appleTimer = 5000
gameTimer = 10000
#---------------------------------------#
# snake's properties                    #
#---------------------------------------#
BODY_SIZE = 15
APPLE_SIZE = 15
HSPEED = 20
VSPEED = 20

enemyCLR = (155, 89, 182)
enemyXspeed = 20
enemyX = WIDTH/2 - 15
enemyYspeed = 0
gravity =0.98
enemyY = 300
speedX = 0
speedY = -VSPEED
segx = [int(WIDTH/2.)]*3
segy = [HEIGHT, HEIGHT+VSPEED, HEIGHT+2*VSPEED]

timerColor = WHITE
appleX = [WIDTH]
appleY = [HEIGHT]
#---------------------------------------#
# function that redraws all objects     #
#---------------------------------------#
def redraw_screen():
    screen.fill(BLUE)
# Score Text
    scoreText = font.render(str(score - 1), 1, WHITE)
    screen.blit(scoreText, (10, 10))
    #Timer Text
    timerText = font.render(str(int(gameTimer/1000)), 1, timerColor)
    screen.blit(timerText, (750, 10))

    for i in range(len(segx)):                                                              #draw snake
        pygame.draw.rect(screen, ORANGE, (segx[i], segy[i], BODY_SIZE, BODY_SIZE))          #head
        pygame.draw.rect(screen, RED, (segx[0], segy[0], BODY_SIZE, BODY_SIZE))             #body

    for i in range(len(appleX)):                                                            #draw apples
        if appleEaten is False:
            pygame.draw.rect(screen, GREEN, (appleX[i], appleY[i], APPLE_SIZE, APPLE_SIZE))

    pygame.display.update()
#---------------------------------------#
# the main program begins here          #
#---------------------------------------#
FPS = 120
appleSound = pygame.mixer.Sound('PickupCoin.wav')
appleSound.set_volume(8)

introScreen = pygame.image.load("introScreen.jpg")

startButton = pygame.image.load("start.jpg")
startButtonHover = pygame.image.load("startHover.jpg")

exitButton = pygame.image.load("exit.jpg")
exitButtonHover = pygame.image.load("exitHover.jpg")

print("Use the arrow keys.")
print("You have 10 seconds to collect an apple")
print("Hit ESC to end the program.")
enemyW = 30
enemyH = 30
exitButtonX = 500
startButtonX = 0
buttonY = HEIGHT - 250
startClicked = False
exitClicked = False
while intro:
    pygame.event.get()
    (mouseX, mouseY) = pygame.mouse.get_pos()
    keys = pygame.key.get_pressed()

    screen.blit(introScreen, (0, 0))
    screen.blit(startButton, (startButtonX, buttonY))
    screen.blit(exitButton, (exitButtonX, buttonY))

    # move enemy

    if enemyY >= HEIGHT:
        enemyYspeed *= -0.95
    if enemyY >= HEIGHT + 30:
        enemyYspeed = 0
        enemyY = -10
    if enemyYspeed > 20:
        enemyH += 1
        enemyY -= 1
        enemyW -= 1
        enemyX += 1
    elif enemyH > 30 and enemyYspeed < 10:
        enemyH -= 2
        enemyY += 2
    elif enemyW < 30 and enemyYspeed < 10:
        enemyW += 2
        enemyX -= 2
    enemyYspeed += gravity
    enemyY += enemyYspeed

    pygame.draw.rect(screen, GREEN, (enemyX, enemyY, enemyW, enemyH))                            #draw enemy

    if mouseX > 0 and mouseX < 300 and mouseY > HEIGHT - 250 and mouseY < HEIGHT - 200:
        screen.blit(startButtonHover, (startButtonX, buttonY))
        if pygame.mouse.get_pressed()[0]:
            startButtonX += 20
            startClicked = True
    if startClicked is True:
        startButtonX -= 15
        if startButtonX <= -300:
            intro = False
            inPlay = True
            clock = pygame.time.Clock()

    if mouseX > 500 and mouseX < WIDTH and mouseY > HEIGHT - 250 and mouseY < HEIGHT - 200:
        screen.blit(exitButtonHover, (exitButtonX, buttonY))
        if pygame.mouse.get_pressed()[0]:
            exitClicked = True
            exitButtonX -= 20
    if exitClicked is True:
        exitButtonX += 15
        if exitButtonX >= WIDTH:
            intro = False

    if keys[pygame.K_ESCAPE]:
        intro = False

    if keys[pygame.K_SPACE]:
        intro = False
        inPlay = True
        clock = pygame.time.Clock()

    pygame.display.update()

while inPlay:
    clock.tick(FPS)
# check for events
    pygame.event.get()
    keys = pygame.key.get_pressed()
    if segx[0] <= 0:
        inPlay = False
    elif segx[0] >= WIDTH:
        inPlay = False
    elif segy[0] <= 0:
        inPlay = False
    elif segy[0] >= (HEIGHT + 1):
        inPlay = False
# act upon key events
    if keys[pygame.K_ESCAPE]:
        inPlay = False
    if keys[pygame.K_LEFT] and speedX != HSPEED:
        speedX = -HSPEED
        speedY = 0
    if keys[pygame.K_RIGHT] and speedX != -HSPEED:
        speedX = HSPEED
        speedY = 0
    if keys[pygame.K_UP] and speedY != VSPEED:
        speedX = 0
        speedY = -VSPEED
    if keys[pygame.K_DOWN]and speedY != -VSPEED:
        speedX = 0
        speedY = VSPEED

# move all segments
    for i in range(len(segx)-1, 0, -1):   # start from the tail, and go backwards:
        segx[i] = segx[i-1]               # every segment takes the coordinates
        segy[i] = segy[i-1]               # of the previous one
# move the head
    segx[0] += speedX
    segy[0] += speedY

# detect if the snake eats itself
    for i in range(len(segx)-1, 0, -1):
        if segx[0] == segx[i] and segy[0] == segy[i]:
            inPlay = False

# apple timer
    appleTimer -= clock.get_time()
    if appleTimer <= 0:
        appleEaten = True
        appleTimer = 5000

# apple position generator
    for i in range(len(appleX)):
        if appleEaten is True:
            appleXGrid = (randint(1, 38))
            appleX.append(HSPEED*appleXGrid)
            appleYGrid = (randint(1, 28))
            appleY.append(VSPEED*appleYGrid)
            appleEaten = False
        # detect if snake eats apple
        if segx[0] == appleX[i] and segy[0] == appleY[i]:
            appleSound.play()
            appleX[i] = (HSPEED*randint(1, 38))
            appleY[i] = (HSPEED*randint(1, 28))
            segx.append(segx[-1])
            segy.append(segy[-1])
            score += 1
            gameTimer = 10000
            difficultyTF = True
            timerColor = WHITE

# game timer
    gameTimer -= clock.get_time()
    if gameTimer <= 4000:               # changes timer color to red if there are 3 seconds left
        timerColor = RED
    if gameTimer <= 1000:
        inPlay = False

# increase difficulty
    if score % 3 == 0 and difficultyTF is True:
        difficulty -= 2
        difficultyTF = False
# update the screen
    redraw_screen()
    pygame.time.delay(difficulty)
    
print("Your score was", score - 1)
pygame.quit()                           # always quit pygame when done!
