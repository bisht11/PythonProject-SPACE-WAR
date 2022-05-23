import pygame
import random
import math
from pygame import mixer

# initializing pygame libraries
pygame.init()

# create a game window
screen = pygame.display.set_mode((800, 600))
# Background
background = pygame.image.load('background.jpg')
# Background Sound
mixer.music.load('backgroundpg.mp3')
mixer.music.play(-1)

# changing the caption and image
pygame.display.set_caption("HIT OR QUIT")
# load icon and set it to the game window
image = pygame.image.load('ufo.png')
pygame.display.set_icon(image)

# Player(image and coordinates)
playerImg = pygame.image.load('spaceship.png')
playerX = 370
playerY = 480
# change in coordinate when the keystroke is pressed(movement towards x-axis)
playerX_change = 0

# Enemy
# multiple enemy setup
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemies = 6

for i in range(num_of_enemies):
    enemyImg.append(pygame.image.load('alien.png'))
    enemyX.append(random.randint(0, 735))
    enemyY.append(random.randint(50, 150))
    enemyX_change.append(1)
    enemyY_change.append(20)

# Laser

# ready- you can not see the bullet on the screen
# fire- the bullet is currently moving across the screen
laserImg = pygame.image.load('laser.png')
laserX = 0
laserY = 480
laserX_change = 0
laserY_change = 5
laser_state = "ready"

# Building up score and font
score = 0
font = pygame.font.Font("freesansbold.ttf", 30)
fontX = 10
fontY = 10

# Game Over
over = pygame.font.Font("freesansbold.ttf", 65)


# draw player image over the screen
def player(x, y):
    screen.blit(playerImg, (x, y))


# draw enemy over the screen
def enemy(x, y, i):
    screen.blit(enemyImg[i], (x, y))


# function to fire the laser
def fire_laser(x, y):
    global laser_state  # made the laser_state global
    laser_state = "fire"
    screen.blit(laserImg, (x + 16, y + 10))  # laser appears on the middle of spaceship


def isColiision(enemyX, enemyY, laserX, laserY):
    distance = math.sqrt((math.pow(enemyX - laserX, 2))) + (math.pow(enemyY - laserY, 2))
    if distance < 27:
        return True
    else:
        return False


def showScore(x, y):
    # render then blit
    score_value = font.render("SCORE :" + str(score), True, (255, 0, 0))
    screen.blit(score_value, (x, y))


def gameOver():
    game_over_value = over.render("GAME OVER", True, (0, 255, 0))
    screen.blit(game_over_value, (250, 250))


# Game Loop
running = True
while running:
    # RGB-Red Green Blue- from 0 to 255 only
    screen.fill((0, 0, 0))
    # background image
    screen.blit(background, (0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # keystroke detection(KEYDOWN)
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change -= 4
            if event.key == pygame.K_RIGHT:
                playerX_change += 4
            if event.key == pygame.K_SPACE:
                if laser_state == "ready":
                    laserSound = mixer.Sound('shootingpg.wav')
                    laserSound.play()
                    # gets the current x coordinate of the spaceship and log into laserX
                    laserX = playerX
                    fire_laser(playerX, laserY)

        # keystroke detection(KEYUP)
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_RIGHT or event.key == pygame.K_LEFT:
                playerX_change = 0

    # controlling the movement speed of our spaceship
    playerX += playerX_change

    # checking boundaries for spaceship
    if playerX <= 0:
        playerX = 0
    elif playerX >= 736:
        playerX = 736

    # synchronising the enemy position with the changing value of i
    for i in range(num_of_enemies):
        # Game over
        if enemyY[i] > 440:
            for j in range(num_of_enemies):
                enemyY[j] = 2000
            gameOver()
            break
        # controlling movement of our enemy
        enemyX[i] += enemyX_change[i]
        # checking boundaries for enemy
        if enemyX[i] <= 0:
            enemyX_change[i] = 2
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >= 736:
            enemyX_change[i] = -2
            enemyY[i] += enemyY_change[i]

        # collision
        collision = isColiision(enemyX[i], enemyY[i], laserX, laserY)
        if collision:
            explosionSound = mixer.Sound('explosionpg.wav')
            explosionSound.play()
            laserY = 480
            laser_state = "ready"
            score += 1
            enemyX[i] = random.randint(0, 735)
            enemyY[i] = random.randint(50, 150)
        enemy(enemyX[i], enemyY[i], i)
    # laser movement
    # reset the bullet everytime in order to shoot the bullet as many times as we want
    if laserY <= 0:
        laserY = 480
        laser_state = "ready"
    # laser movement
    if laser_state == "fire":
        fire_laser(laserX, laserY)
        laserY -= laserY_change

    # blit enemy and player throughout the game loop
    player(playerX, playerY)
    showScore(fontX, fontY)
    # updating the game window to apply all the changes
    pygame.display.update()