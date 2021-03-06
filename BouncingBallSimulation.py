import pygame
import math
from pygame import mixer

pygame.init()
ScreenResolution = (1500, 600)
BallStartingPos = (ScreenResolution[0] - 50, 200 )
TimeStep = 10
SlopeAngle = 10.0
Screen = pygame.display.set_mode(ScreenResolution)
font = pygame.font.Font('freesansbold.ttf', 32)

def slopeDraw(SlopeAngle, ScreenResolution):
    pygame.draw.line(Screen, 0x26a32c, (0, ScreenResolution[1]), (ScreenResolution[0], math.tan(-SlopeAngle * math.pi / 180.0) * ScreenResolution[0] + ScreenResolution[1]), 5)

class MovingObject:
    def __init__(self, StartX, StartY, TimeStep_ms, SlopeAngle, ScreenResolution):
        self.ScreenResolution = ScreenResolution
        self.SlopeAngle = SlopeAngle
        self.TimeStep = TimeStep_ms / 1000.0
        self.X = float(StartX)
        self.Y = float(StartY)
        self.vX = 0.0
        self.vY = 0.0
        self.aX = 0.0
        self.aY = 981.0
        self.A = math.tan(self.SlopeAngle * math.pi / 180.0)
        self.B = 1.0
        self.C = -self.ScreenResolution[1]
        self.PrevDistance = abs(self.A * StartX + self.B * StartY + self.C) / math.sqrt(self.A ** 2 + self.B ** 2)
        self.MoveDownDirection = True
        self.No = 0
        self.NoOfBounces = font.render("Bounce no: " + str(self.No), True, (255, 255, 255))
        self.MaxHeight = font.render("Max height: " + str(int(self.PrevDistance)), True, (255, 255, 255))
        self.Range = font.render("Range: " + str(0), True, (255, 255, 255))        
    
    def stepMove(self):
        self.vX += self.aX * self.TimeStep
        self.vY += self.aY * self.TimeStep
        self.X += self.vX * self.TimeStep
        self.Y += self.vY * self.TimeStep
    
    def bounceOffSurface(self):
        vX_Old = self.vX
        vY_Old = -self.vY
        self.vX = vY_Old * math.cos((90.0 - 2 * self.SlopeAngle) * math.pi / 180.0) + vX_Old * math.cos((-2 * self.SlopeAngle) * math.pi / 180.0)
        self.vY = vY_Old * math.sin((90.0 - 2 * self.SlopeAngle) * math.pi / 180.0) + vX_Old * math.sin((-2 * self.SlopeAngle) * math.pi / 180.0)
        
        #try:
        #    VeloAngle = math.atan(vY_Old / vX_Old)
        #except ZeroDivisionError:
        #    VeloAngle = math.pi/2
        #self.vX = -math.sqrt(vX_Old ** 2 + vY_Old ** 2) * math.cos(VeloAngle - 2 * self.Angle * math.pi / 180.0)
        #self.vY = -math.sqrt(vX_Old ** 2 + vY_Old ** 2) * math.sin(VeloAngle - 2 * self.Angle * math.pi / 180.0)

    def clashDetection(self):
        Distance = abs(self.A * self.X + self.B * self.Y + self.C) / math.sqrt(self.A ** 2 + self.B ** 2)
        #print(Distance)

        DistanceDelta = Distance - self.PrevDistance
        print(DistanceDelta)
        if DistanceDelta > 0 and self.MoveDownDirection is True:
            self.MoveDownDirection = False
            self.bounceOffSurface()
            BounceSound = mixer.Sound("laser.wav")
            BounceSound.play()
            self.No += 1
            self.NoOfBounces = font.render("Bounce no: " + str(self.No), True, (255, 255, 255))
            self.Range = font.render("Range: " + str( int(abs(BallStartingPos[0] - self.X)) ), True, (255, 255, 255))
        elif DistanceDelta < 0.1 and DistanceDelta > -0.1 and self.MoveDownDirection is False: # Maximum height of a single bounce, height over slope
            self.MaxHeight = font.render("Max height: " + str(int(Distance)), True, (255, 255, 255))
            self.MoveDownDirection = True
        
        self.PrevDistance = Distance
        return Distance

    def __del__(self):
        pass
    

pygame.display.set_caption("Bouncing ball simulation")
BallImg = pygame.image.load('ball.png')

NextMove = pygame.time.get_ticks() + TimeStep
Screen.fill((0, 30, 94))
ball = MovingObject(BallStartingPos[0], BallStartingPos[1], TimeStep, SlopeAngle, ScreenResolution)
pygame.display.update()

GameRunning = True
while GameRunning:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            GameRunning = False
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                SpacePressed = True
                while SpacePressed:
                    for event2 in pygame.event.get():
                        if event2.type == pygame.KEYDOWN:
                            if event2.key == pygame.K_SPACE:
                                SpacePressed = False

    CurrentTime = pygame.time.get_ticks()

    if CurrentTime >= NextMove:
        Screen.fill((0, 30, 94))
        slopeDraw(SlopeAngle, ScreenResolution)
        ball.stepMove()
        ball.clashDetection()
        Screen.blit(ball.NoOfBounces, (50, 20))
        Screen.blit(ball.MaxHeight, (50, 60))
        Screen.blit(ball.Range, (50, 100))
        #print(ball.X)
        #print(ball.Y)
        Screen.blit(BallImg, (ball.X, ball.Y))
        pygame.display.update()
        NextMove = pygame.time.get_ticks() + TimeStep