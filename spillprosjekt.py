# -*- coding: utf-8 -*-
"""
Created on Wed Nov 27 15:22:45 2019

@author: Joakim
"""

import pygame, sys, random
from pygame.locals import *

FPS = 30
playerSpeed = 5
windowWidth = 400
windowHeight = 600
divisorForText = 5
divisorForText2 = 3
textColor = (192, 192, 192)
bulletWidth = 10
bulletHeight = 20
bulletSpeed = 4
bakgrunn = (0, 0, 64)
main = (0, 0, 0)
addNewBulletRate = 0 #mindre tall = flere bullets
powerUpStop = False
cooldown = 0


def end():
    pygame.quit()
    sys.exit()

def waitForPlayerToPress():
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                end()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    end()
                if event.key == K_SPACE:
                    return

def collision(playerRect, bullets):
    for b in bullets:
        if playerRect.colliderect(b['rect']):
            return True
    return False

def drawText(text, font, surface, x, y):
    textObj = font.render(text, 1, textColor)
    textRect = textObj.get_rect()
    textRect.topleft = (x, y)
    surface.blit(textObj, textRect)
    
def drawScreen():
    #fill background with color
    windowSurface.fill(bakgrunn)
    pygame.draw.polygon(windowSurface, (64, 64, 128), ((146 + 64, 0 + 30), (236 + 64, 277 + 30), (0 + 64, 106 + 30), (291 + 64, 106 + 30), (56 + 64, 277 + 30)))
    #draw score and top score
    drawText('Score: %s' % (score), font, windowSurface, 10, 0)
    drawText('Best: %s' % (bestRun), font, windowSurface, 10, 40)
    drawText('Lives: %s' % (playerHealth), font, windowSurface, 10, 80)
    #drawText('Cooldown: %s' % (cooldown), font, windowSurface, 10, windowHeight - 40)
    drawText('Freeze: %s' % (freeze), font, windowSurface, windowWidth - 200, 40)
    drawText('Bombs: %s' % (powerUpBomb), font, windowSurface, windowWidth - 150, 0)

pygame.init()
clock = pygame.time.Clock()

windowSurface = pygame.display.set_mode((windowWidth, windowHeight), 0, 32)
pygame.display.set_caption('budget toohoo')
pygame.mouse.set_visible(False)
font = pygame.font.SysFont(None, 48)

#notes: do sounds last
gameOverSound = pygame.mixer.Sound('aaaAAA.wav')
pygame.mixer.music.load('toad sings christmas.mp3')

#sets up images
playerHitbox = pygame.image.load('hitbox.png')
playerImage = pygame.image.load('exarch1Hello.png')
playerHit = pygame.image.load('playerHit.png')
#playerBomb = pygame.image.load('hitbox.png')
playerSize = pygame.transform.scale(playerImage, (40, 40))
#playerBombSize = pygame.transform.scale(playerBomb, (100, 100))
playerRectSize = playerSize.get_rect()
playerRect = playerHitbox.get_rect()
#playerRectBomb = playerBombSize.get_rect()
#note: draw bullet myself
bulletImage = pygame.image.load('bullet.png')

bestRun = 0
#run the game loop
while True:
    #show start screen
    windowSurface.fill(main)
    drawText('budget toohoo', font, windowSurface, (windowWidth / divisorForText), (windowHeight / divisorForText))
    drawText('press space to play!', font, windowSurface, (windowWidth / divisorForText) - 30, (windowHeight / divisorForText) + 50)
    drawText('use wasd to move', font, windowSurface, (windowWidth / divisorForText) - 20, (windowHeight / divisorForText) + 100)
    drawText('i: freeze', font, windowSurface, (windowWidth / divisorForText) + 60, (windowHeight / divisorForText) + 150)
    drawText('o: bomb', font, windowSurface, (windowWidth / divisorForText) + 60, (windowHeight / divisorForText) + 200)
    pygame.display.update()
    waitForPlayerToPress()
    
    bullets = []
    score = 0
    timerScore = 0
    timerCheck = 0
    playerHealth = 3
    playerRectSize.topleft = (windowWidth / 2, windowHeight * 2 / 3)
    playerRect.topleft = (windowWidth / 2 + 20 - 5, windowHeight * 2 / 3 + 20 - 5)
    moveLeft = moveRight = moveUp = moveDown = False
    powerUpStop = False
    freeze = "OFF"
    powerUpBomb = 3
    bombBoolean = False
    cooldown = 0
    invisTimer = 0
    invisFrames = False
    bulletAddCounter = 0
    pygame.mixer.music.play(-1, 0.0)
    while True:
        timerScore += 1
        if timerScore == FPS:
            score += 1
            timerScore = 0
        for event in pygame.event.get():
            if event.type == QUIT:
                end()
            if event.type == KEYDOWN:
                if event.key == ord('a'):
                    moveRight = False
                    moveLeft = True
                if event.key == ord('d'):
                    moveLeft = False
                    moveRight = True
                if event.key == ord('w'):
                    moveDown = False
                    moveUp = True
                if event.key == ord('s'):
                    moveUp = False
                    moveDown = True
            if event.type == KEYUP:
                if event.key == K_ESCAPE:
                    end()
                if event.key == ord('i'):
                    if score >= 5 and powerUpStop == False:
                        powerUpStop = True
                        freeze = "ON"
                        score -= 5
                if event.key == ord('o'):
                    if powerUpBomb > 0:
                        bombBoolean = True
                        powerUpBomb -= 1
                if event.key == ord('a'):
                    moveLeft = False
                if event.key == ord('d'):
                    moveRight = False
                if event.key == ord('w'):
                    moveUp = False
                if event.key == ord('s'):
                    moveDown = False
        if powerUpStop == True:
                bulletAddCounter = -1
        if powerUpStop == False:
                bulletAddCounter += 1
        if bulletAddCounter >= addNewBulletRate:
            bulletAddCounter = 0
            newBullet = {'rect': pygame.Rect(random.randint(0, windowWidth - bulletWidth), 0 - bulletHeight, bulletWidth, bulletHeight),
                         'speed':bulletSpeed, 'surface':pygame.transform.scale(bulletImage, (bulletWidth, bulletHeight)),
                         }
            bullets.append(newBullet)
        if moveLeft and playerRect.left > 0:
            playerRect.move_ip(-1 * playerSpeed, 0)
            playerRectSize.move_ip(-1 * playerSpeed, 0)
        if moveRight and playerRect.right < windowWidth:
            playerRect.move_ip(playerSpeed, 0)
            playerRectSize.move_ip(playerSpeed, 0)
        if moveUp and playerRect.top > 0:
            playerRect.move_ip(0, -1 * playerSpeed)
            playerRectSize.move_ip(0, -1 * playerSpeed)
        if moveDown and playerRect.bottom < windowHeight:
            playerRect.move_ip(0, playerSpeed)
            playerRectSize.move_ip(0, playerSpeed)
        if bombBoolean == True:
            timerCheck += 1
            if cooldown == 0:
                for b in bullets:
                    if b['rect'].top < windowHeight:
                        bullets.remove(b)
            if timerCheck == 14:
                cooldown += 1
                timerCheck = 0
            if cooldown == 1:
                bombBoolean = False
                cooldown = 0
        if powerUpStop == True:
            for b in bullets:
                b['rect'].move_ip(0, 0)
            if timerScore == 0:
                cooldown += 1
                score -= 1
            if cooldown == 5:
                powerUpStop = False
                freeze = "OFF"
                cooldown = 0
        else:
            for b in bullets:
                b['rect'].move_ip(0, b['speed'])
        for b in bullets[:]:
            if b['rect'].top > windowHeight:
                bullets.remove(b)
                
        drawScreen()
        #check collision
        if invisFrames == False:
            if collision(playerRect, bullets):
                playerHealth -= 1
                invisFrames = True
                if playerHealth <= 0:
                    if score > bestRun:
                        bestRun = score
                    for b in bullets:
                        windowSurface.blit(b['surface'], b['rect'])
                    pygame.display.update()
                    break
            #draw player and hitbox
            windowSurface.blit(playerSize, playerRectSize)
            windowSurface.blit(playerHitbox, playerRect)
        if invisFrames == True:
            if timerScore == 0:
                invisTimer += 1
            if timerScore % 4:
                windowSurface.blit(playerHit, playerRectSize)
                windowSurface.blit(playerHit, playerRect)
            if (timerScore + 2) % 4:
                windowSurface.blit(playerSize, playerRectSize)
                windowSurface.blit(playerHitbox, playerRect)
            if invisTimer == 2:
                invisFrames = False
                invisTimer = 0
        #draw bullets
        for b in bullets:
            windowSurface.blit(b['surface'], b['rect'])
        #draw window to screen
        pygame.display.update()
        clock.tick(FPS)
    #stop game and show "game over" screen
    pygame.mixer.music.stop()
    gameOverSound.play()
    #death animation
    for i in range(0, 40, 2):
        drawScreen()
        playerDeath = pygame.transform.scale(playerImage, (40 - i, 40 - i))
        playerRectSize.move_ip(1, 0)
        playerRectSize.move_ip(0, 1)
        windowSurface.blit(playerDeath, playerRectSize)
        windowSurface.blit(playerHitbox, playerRect)
        for b in bullets:
            windowSurface.blit(b['surface'], b['rect'])
        pygame.display.update()
        #kode runs FPS times a second
        clock.tick(FPS)
    drawText('game over', font, windowSurface, (windowWidth / divisorForText2) - 20, (windowHeight / divisorForText2))
    drawText('press space to restart', font, windowSurface, (windowWidth / divisorForText2) - 100, (windowHeight / divisorForText2) + 40)
    pygame.display.update()
    waitForPlayerToPress()
    gameOverSound.stop()