import pygame
import math

pygame.init()
ScreenResolution = (1500, 600)
TimeStep = 10
SlopeAngle = 10.0
Screen = pygame.display.set_mode(ScreenResolution)

def slopeDraw(SlopeAngle, ScreenResolution):
    pygame.draw.line(Screen, 0x26a32c, (0, ScreenResolution[1]), (ScreenResolution[0] * math.tan((90.0 - SlopeAngle) * math.pi / 180), 0), 5)

class MovingObject:
    def __init__(self, StartX, StartY, TimeStep_ms, SlopeAngle, ScreenResolution):
        self.ScreenResolution = ScreenResolution
        self.Angle = SlopeAngle
        self.TimeStep = TimeStep_ms / 1000.0
        self.X = float(StartX)
        self.Y = float(StartY)
        self.vX = 0.0
        self.vY = 0.0
        self.aX = 0.0
        self.aY = 981.0
        self.ClashBlock = False
    
    def stepMove(self):
        self.vX += self.aX * self.TimeStep
        self.vY += self.aY * self.TimeStep
        self.X += self.vX * self.TimeStep
        self.Y += self.vY * self.TimeStep

    def clashDetection(self):
        A = math.tan(self.Angle * math.pi / 180.0)
        B = 1.0
        C = -self.ScreenResolution[1]
        Distance = abs(A * self.X + B * self.Y + C) / math.sqrt(A ** 2 + B ** 2)
        print(Distance)

        if Distance < 5 and not self.ClashBlock:
            self.ClashBlock = True
            self.bounceOffSurface()
            return True
        elif Distance > 5:
            self.ClashBlock = False
            return False
    
    def bounceOffSurface(self):
        vX_Old = self.vX
        vY_Old = self.vY
        self.vX = -(vY_Old * math.cos((90.0 - 2* self.Angle) * math.pi / 180.0) + vX_Old * math.cos((self.Angle * 2) * math.pi / 180.0))
        self.vY = -(vY_Old * math.sin((90.0 - 2* self.Angle) * math.pi / 180.0) - vX_Old * math.sin((self.Angle * 2) * math.pi / 180.0))

    def __del__(self):
        pass
    

pygame.display.set_caption("Bouncing ball simulation")

BallImg = pygame.image.load('ball.png')

NextMove = pygame.time.get_ticks() + TimeStep
Screen.fill((0, 30, 94))
ball = MovingObject(ScreenResolution[0]-50, 100, TimeStep, SlopeAngle, ScreenResolution)
pygame.display.update()

GameRunning = True
while GameRunning:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            GameRunning = False

    CurrentTime = pygame.time.get_ticks()

    if CurrentTime >= NextMove:
        Screen.fill((0, 30, 94))
        slopeDraw(SlopeAngle, ScreenResolution)
        ball.stepMove()
        ball.clashDetection()
        #print(ball.X)
        #print(ball.Y)
        Screen.blit(BallImg, (ball.X, ball.Y))
        pygame.display.update()
        NextMove = pygame.time.get_ticks() + TimeStep