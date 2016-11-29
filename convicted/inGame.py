import pygame
import Character
import floorCollision
import movement
import sys

pygame.init()


#Height and width of the screen
Width = 1200
Height = 500

#Direction of the character. For x 1 is right and -1 is left, 0 is no movement.
charXDirection = 0
charYDirection = 1
#Sets the starting position for the character.
charXpos = 50
charYPos = 0
#Sets the starting position for the floor.
floorXPos = 100
floorYPos = 900
#Used to check if the character has jumped and therefore if they are able to jump.
jumped = False

WHITE = (255,255,255)
TRANSPARENT = (255,255,255,0)
BLACK = (0,0,0)
Purple = (146,32,164)
Grey = (128,128,128)
BLUE = (0,0,255)
counter = 0
counterIncrease = True

window = pygame.display.set_mode((Width, Height),0, 32)
font = pygame.font.SysFont(None,48)
text = font.render("  ",True, WHITE,WHITE)
character = text.get_rect()
onFloor = False
isSliding = False
characterImage = pygame.image.load('8bitDude.png')
characterImage2 = pygame.image.load('8bitDude.jpg')
skipImage = pygame.image.load('skipSmallSize.jpg')
binImage = pygame.image.load('binSmallSize.jpg')
characterImageSlide = pygame.image.load('8bitDudeSlide.jpg')
bikeRackImage = pygame.image.load('BikeRack.jpg')
wall = pygame.image.load('wall.png')
wall = pygame.transform.scale(wall,(30,100))

firstFloor = (0, Height-20, Width, 20)
skip1 = (450,Height-77,132,57)
bin1 = (300,Height-51,22,31)
bikeRack = (900,Height - 64,87,44)
wallObject = (700,Height-120,30,100)


while True:
                                                                                                                        #Checks if the player is pressing any key. Listener.
    pressed = pygame.key.get_pressed()
    charYDirection += 0.1

    if pressed[pygame.K_SPACE] and onFloor == True:
        jumped = True
        charYDirection, charYPos = movement.jump(charYPos)
    elif pressed[pygame.K_s] or pressed[pygame.K_DOWN]:
        isSliding = True
    else:
        isSliding = False

    if pressed[pygame.K_a] or pressed[pygame.K_LEFT]:
        charXDirection = movement.moveLeft(charXDirection)
    elif pressed[pygame.K_d] or pressed[pygame.K_RIGHT]:
        charXDirection = movement.moveRight(charXDirection)
    else:
        charXDirection = 0


                                                                                                                        #Checks if the players position is less than the position of the floor. If it is then it brings the player back up one space.
    if character.colliderect(firstFloor) == True:
        if charYPos >= firstFloor[1]+20:
            charYDirection = 1
        else:
            onFloor = True
    else:
        onFloor = False

    if onFloor == True:
        charYDirection = 0
        jumped = False
                                                                                                                        #Checks if the player is pressing the right or d arrow keys. If they are the character moves to the right.

    onBin = character.colliderect(bin1)
    onSkip = character.colliderect(skip1)
    onBikeRack = character.colliderect(bikeRack)
    onWall = character.colliderect(wallObject)

    if character.colliderect(bin1) == True:
        onBin = True
    elif character.colliderect(skip1) == True:
        onSkip = True
    elif character.colliderect(bikeRack) == True:
        onBikeRack = True
    elif character.colliderect(wallObject) == True:
        onWall = True
    else:
        onBin = False
        onSkip = False
        onBikeRack = False



    #Position checkers to see if the player is at the boundry of the screen.
    charXpos = floorCollision.outOfBounds(charXpos,Width)

    if onBin == True:
        onBin = False
        if charXpos >= bin1[0]+bin1[2]:
            if pressed[pygame.K_RIGHT] or pressed[pygame.K_d]:
                charXDirection = 1
            else:
                charXDirection = 0
        elif charXpos <= bin1[0]:
            if pressed[pygame.K_LEFT] or pressed[pygame.K_a]:
                charXDirection = -1
            else:
                charXDirection = 0
        elif charYPos <= bin1[1]:
            charYDirection = 0
        if pressed[pygame.K_SPACE]:
            charYDirection = -4
    if onSkip == True:
        onSkip = False
        if charXpos >= skip1[0] + skip1[2]:
            if pressed[pygame.K_RIGHT] or pressed[pygame.K_d]:
                charXDirection = 1
            else:
                charXDirection = 0
        elif charXpos <= skip1[0]:
            if pressed[pygame.K_LEFT] or pressed[pygame.K_a]:
                charXDirection = -1
            else:
                charXDirection = 0
        elif charYPos <= skip1[1]:
            charYDirection = 0
            if pressed[pygame.K_SPACE]:
                charYDirection = -4
    if onBikeRack == True:
        onBikeRack = False
        if charXpos >= bikeRack[0]+bikeRack[2] and isSliding == False:
            if pressed[pygame.K_RIGHT] or pressed[pygame.K_d]:
                charXDirection = 1
            else:
                charXDirection = 0
        elif charXpos <= bikeRack[0] and isSliding == False:
            if pressed[pygame.K_LEFT] or pressed[pygame.K_a]:
                charXDirection = -1
            else:
                charXDirection = 0
        elif charYPos <= bikeRack[1]:
            charYDirection=0
            if pressed[pygame.K_SPACE]:
                charYDirection = -4
    if onWall == True:
        onWall = False
        if charXpos >= wallObject[0] + wallObject[2]:
            if pressed[pygame.K_RIGHT] or pressed[pygame.K_d]:
                charXDirection = 1
            else:
                charXDirection = 0
        elif charXpos <= wallObject[0]:
            if pressed[pygame.K_LEFT] or pressed[pygame.K_a]:
                charXDirection = -1
            else:
                charXDirection = 0
        elif charYPos <= wallObject[1]:
            charYDirection = 0
            if pressed[pygame.K_SPACE]:
                charYDirection = -4


    charXpos = charXpos + charXDirection
    charYPos = charYPos + charYDirection
    character.centerx = charXpos
    character.centery = charYPos

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    if pressed[pygame.K_ESCAPE]:
        pygame.quit()
        sys.exit()

    window.fill(WHITE)


    window.blit(text,character)
    if isSliding == True:
        window.blit(characterImageSlide, (charXpos - 9, charYPos - 6))
        charSlidingRect = (charXpos,charYPos,40,20)
        charXDirection = movement.slide(charXDirection)
        if charXDirection > 0:
            charXDirection -= 0.1
        elif charXDirection < 0 :
            charXDirection += 0.1


    elif counterIncrease == True:
        pygame.draw.rect(window, WHITE, character)
        counter +=1
        window.blit(characterImage, (charXpos - 10, charYPos - 23))
        if(counter >= 25):
            counterIncrease = False
    else:
        pygame.draw.rect(window, WHITE, character)
        counter-=1
        window.blit(characterImage2,(charXpos - 10, charYPos - 23))
        if(counter <=0):
            counterIncrease = True


    pygame.draw.rect(window,Grey, firstFloor)

    pygame.draw.rect(window, BLUE,bin1)
    pygame.draw.rect(window, BLUE,skip1)
    pygame.draw.rect(window, TRANSPARENT,bikeRack)
    pygame.draw.rect(window,TRANSPARENT,wallObject)

    window.blit(binImage,(bin1[0],bin1[1]))
    window.blit(skipImage,(skip1[0],skip1[1]))
    window.blit(bikeRackImage,(bikeRack[0],bikeRack[1]))
    window.blit(wall,(wallObject[0],wallObject[1]))



    clock = pygame.time.Clock()
    clock.tick(300)
    pygame.display.update()