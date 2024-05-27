import math
import random
import pygame
from pygame import mixer

# Intialize the pygame
pygame.init()

# create the screen
screen = pygame.display.set_mode((800, 500))

# Background
background = pygame.image.load('background.png')

# Sound
mixer.music.load("background.wav")
mixer.music.play(-1)

# Caption and Icon
pygame.display.set_caption("Space Invader")
icon = pygame.image.load('ufo.png')
pygame.display.set_icon(icon)

# Player
playerImg = pygame.image.load('player.png')
playerX = 370
playerY = 380
playerX_change = 0
 
# Enemy
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemies = 10

#possible coords
xlist = [0,50,100,150,200,250,300,350,400,450,500,550,600,650,700]
ylist = [50, 100, 150]

for i in range(num_of_enemies):
	enemyImg.append(pygame.image.load("invader"+ str(random.randint(1,5)) +".png"))
	enemyX.append(random.choice(xlist))
	enemyY.append(random.choice(ylist))
	enemyX_change.append(10)
	enemyY_change.append(20)

# Bullet
bulletImg = pygame.image.load('bullet.png')
bulletX = 0
bulletY = 380
bulletX_change = 0
bulletY_change = 10
bullet_state = "ready"

# Score
score_value = 0
font = pygame.font.Font('freesansbold.ttf', 32)
textX = 10
testY = 10

# Game Over
over_font = pygame.font.Font('freesansbold.ttf', 64)
 

def show_score(x, y):
	score = font.render("Score : " + str(score_value), True, (255, 255, 255))
	screen.blit(score, (x, y))

def game_over_text():
	over_text = over_font.render("GAME OVER", True, (255, 255, 255))
	screen.blit(over_text, (200, 250))

def player(x, y):
	screen.blit(playerImg, (x, y))

def enemy(x, y, i):
	screen.blit(enemyImg[i], (x, y))

def fire_bullet(x, y):
	global bullet_state
	bullet_state = "fire"
	screen.blit(bulletImg, (x + 16, y + 10))

def isCollision(enemyX, enemyY, bulletX, bulletY):
	distance = math.sqrt(math.pow(enemyX - bulletX, 2) + (math.pow(enemyY - bulletY, 2)))
	if distance < 27:
		return True
	else:
		return False

# Game Loop
running = True
while running:

	# RGB = Red, Green, Blue
	screen.fill((0, 0, 0))

	# Background Image
	screen.blit(background, (0, 0))

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False

		# if keystroke is pressed check whether its right or left
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_LEFT:
				playerX_change = -10
				playerX += playerX_change
				if playerX <= 0:
					playerX = 0
			if event.key == pygame.K_RIGHT:
				playerX_change = 10
				playerX += playerX_change
				if playerX >= 736:
					playerX = 736
			if event.key == pygame.K_SPACE:
				if bullet_state == "ready":
					bulletSound = mixer.Sound("laser.wav")
					bulletSound.play()
					# Get the current x cordinate of the spaceship
					bulletX = playerX
					fire_bullet(bulletX, bulletY)

		 

	# Enemy Movement
	for i in range(num_of_enemies):

		if enemyY[i] > 10:
			enemyX[i] += enemyX_change[i]
			if enemyX[i] <= 0:
				enemyX_change[i] = 2
				enemyY[i] += enemyY_change[i]
			elif enemyX[i] >= 736:
				enemyX_change[i] = -2
				enemyY[i] += enemyY_change[i]

			# Game Over
			if enemyY[i] >= 340:
				game_over_text()
				num_of_enemies = 0;
				
		# Collision
		collision = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)
		if collision:
			explosionSound = mixer.Sound("explosion.wav")
			explosionSound.play()
			bulletY = 380
			bullet_state = "ready"
			score_value += 1
			enemyX[i] = random.randint(0, 736)
			enemyY[i] = random.randint(50, 150)
		enemy(enemyX[i], enemyY[i], i)

		# Bullet Movement
		if bulletY <= 0:
			bulletY = 380
			bullet_state = "ready"
		if bullet_state == "fire":
			fire_bullet(bulletX, bulletY)
			bulletY -= bulletY_change

		player(playerX, playerY)
		show_score(textX, testY)
		pygame.display.update()