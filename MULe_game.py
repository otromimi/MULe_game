"""
Muslimjon Kholjuraev
Guillermo  Leiro Arroyo

Introducing our way to fight corona ;)

"""

import math
import random
import pygame


# Starting pygame  and window
pygame.init()
screen = pygame.display.set_mode((800, 600))

# Background
background = pygame.image.load('vein2.jpg')

# Sound
pygame.mixer.music.load("coffinDance-cut.mp3")
pygame.mixer.music.play(-1)

# Caption and Icon
pygame.display.set_caption("Corona virus attack")
icon = pygame.image.load('but.png')
pygame.display.set_icon(icon)

# white_cell
white_cell_img = pygame.image.load('whiteCell.png')
white_cell_X = 370
white_cell_Y = 480
white_cell_X_change = 0

# Virus
corona_virus = []
virusX = []
virusY = []
virusX_change = []
virusY_change = []
num_of_enemies = 4

for i in range(num_of_enemies):
    corona_virus.append(pygame.image.load('coronaVirus.png'))
    virusX.append(random.randint(0, 736))
    virusY.append(random.randint(50, 150))
    virusX_change.append(4)
    virusY_change.append(40)

# Bullet

# Ready - You can't see the bullet on the screen
# Fire - The bullet is currently moving

bulletImg = pygame.image.load('bullet.png')
bulletX = 0
bulletY = 480
bulletX_change = 0
bulletY_change = 10
bullet_state = "ready"

# Score and best score inicializatioon
try:
    with open('best_score.txt', 'rt') as score_file:
        best_score = int(score_file.read())
except:
    best_score = 0

score_value = 0
font = pygame.font.Font('freesansbold.ttf', 32)

textX = 10
textY = 10

# Game Over
over_font = pygame.font.Font('freesansbold.ttf', 120)


def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg, (x + 16, y + 10))


def isCollision(virusX, virusY, bulletX, bulletY):
    distance = math.sqrt(math.pow(virusX - bulletX, 2) + (math.pow(virusY - bulletY, 2)))
    if distance < 27:
        return True
    else:
        return False


# variable used to maintain the infinite loop at game
mainloop = True

while mainloop:

    # RGB = Red, Green, Blue
    screen.fill((0, 0, 0))
    # Background Image
    screen.blit(background, (0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            # exit the gam by pressing <ESC> or by clicking the 'X' button
            mainloop = False

        # if keystroke is pressed check whether its right or left
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                white_cell_X_change = -5
            if event.key == pygame.K_RIGHT:
                white_cell_X_change = 5
            if event.key == pygame.K_SPACE or event.key == pygame.K_UP:
                if bullet_state == "ready":
                    bulletSound = pygame.mixer.Sound("laser.wav")
                    bulletSound.play()
                    # Get the current x cordinate of the spaceship
                    bulletX = white_cell_X
                    fire_bullet(bulletX, bulletY)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                white_cell_X_change = 0


    white_cell_X += white_cell_X_change
    if white_cell_X <= 0:
        white_cell_X = 0
    elif white_cell_X >= 736:
        white_cell_X = 736

    # virus Movement
    for i in range(num_of_enemies):

        # Game Over
        if virusY[i] > 440:
            for j in range(num_of_enemies):
                virusY[j] = 2000
            over_text = over_font.render("YOU DIE", True, ((255), 255, 255))
            screen.blit(over_text, ((150), 250))
            break

        virusX[i] += virusX_change[i]
        if virusX[i] <= 0:
            virusX_change[i] = 4
            virusY[i] += virusY_change[i]
        elif virusX[i] >= 736:
            virusX_change[i] = -4
            virusY[i] += virusY_change[i]

        # Collision
        collision = isCollision(virusX[i], virusY[i], bulletX, bulletY)
        if collision:
            explosionSound = pygame.mixer.Sound("explosion.wav")
            explosionSound.play()
            bulletY = 480
            bullet_state = "ready"
            score_value += 1
            virusX[i] = random.randint(0, 736)
            virusY[i] = random.randint(50, 150)

        screen.blit(corona_virus[i], (virusX[i], virusY[i]))

    # Bullet Movement
    if bulletY <= 0:
        bulletY = 480
        bullet_state = "ready"

    if bullet_state == "fire":
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change

    # Bliting (adding) cell to the screen    
    screen.blit(white_cell_img, (white_cell_X, white_cell_Y))
    #Adding score to the screen
    score = font.render("Best score : {}  Score : {}".format(best_score, score_value), True, (255, 255, 255))
    screen.blit(score, (textX, textY))
    
    pygame.display.flip()


####################################### END MAIN-LOOP ##############################################

#print(f'{best_score}  {score_value}')

if score_value > best_score:
    with open('best_score.txt', 'w') as f:
        f.write(f'{score_value}')

# Quiting pygame
pygame.quit()