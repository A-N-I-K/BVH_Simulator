'''
Created on Apr 15, 2019

@author: Anik
'''

import contextlib
import time
from _overlapped import NULL
with contextlib.redirect_stdout(None):
    import pygame
from pygame.locals import *
from PIL import Image
from math import ceil, sqrt

FILENAME = "obstacleMask.png"
IMG = Image.open(FILENAME)

WINSIZE = IMG.size
PIXELS = IMG.load()
CENTER = [WINSIZE[0] / 2, WINSIZE[1] / 2]
INFINITY = WINSIZE[0] * WINSIZE[1]

GRID = 15
DIAG = ceil(sqrt(2 * GRID * GRID))

UP = (172, 258)
MID = (293, 365)

BLACK = 0, 0, 0
WHITE = 255, 255, 255
RED = 255, 0, 0
YELLOW = 255, 255, 0
GREEN = 0, 255, 0

# Initialize screen
pygame.init()
# screen = pygame.display.set_mode([WINSIZE[0] * 2, WINSIZE[1]])
screen = pygame.display.set_mode(WINSIZE)
#screen.blit(pygame.image.load(FILENAME), (0, 0))
pygame.display.set_caption("BVH Simulator - Anik, 2019")
pygame.display.update()

# time.sleep(1)


def generateVertex():
    vertexList = []
    
    for i in range(0, WINSIZE[0], GRID):
        for j in range (0, WINSIZE[1] - 1):
            if PIXELS[i, j] != PIXELS[i, j + 1]:
                # print((i,j), PIXELS[i, j])
                vertexList.append((i, j))
    
    for j in range(0, WINSIZE[1], GRID):
        for i in range (0, WINSIZE[0] - 1):
            if PIXELS[i, j] != PIXELS[i + 1, j]:
                # print((i,j), PIXELS[i, j])
                vertexList.append((i, j))
                
    # print(vertexList)
    return vertexList


def clusterizeVertex(vertexList):
    clusterList = []
    # tempList = []
    # print(len(vertexList))
    # start = vertexList.pop(0)
    # tempList.append(start)
    # print(start, len(vertexList))
    # minDist = WINSIZE[0] * WINSIZE[1]
    # minIndex = -1
    while(len(vertexList) != 0):
        tempList = []
        start = vertexList.pop(0)
        
        while(True):
            # start = vertexList.pop(0)
            tempList.append(start)
            minDist = INFINITY
            minIndex = -1
            for i in range(0, len(vertexList)):
                if pointDist(start, vertexList[i]) < minDist:
                    minDist = pointDist(start, vertexList[i])
                    minIndex = i
                    
            if minDist > DIAG:
                tempList.append(tempList[0])
                clusterList.append(tempList)
                break
            else:
                print([minIndex], vertexList[minIndex])
                # tempList.append(vertexList[minIndex])
                start = vertexList.pop(minIndex)
                
                # minDist = WINSIZE[0] * WINSIZE[1]
                # minIndex = -1
    return clusterList


def displayVertex(clusterList):
    for vertexList in clusterList:
        screen.fill(RED, ((vertexList), (2, 2)))
        pygame.display.update()
        time.sleep(0.05)
    #pauseStuff()

    # time.sleep(10)


def pointDist(p1, p2):
    return sqrt((p1[0] - p2[0]) * (p1[0] - p2[0]) + (p1[1] - p2[1]) * (p1[1] - p2[1]))


def drawPoly(clusterList):
    for vertexList in clusterList:
        pygame.draw.lines(screen, RED, False, vertexList, 2)
        pygame.display.update()
        time.sleep(0.05)

        
def bvhCircle(clusterList):
    for vertexList in clusterList:
        longestPair = ((0, 0), (0, 0))
        
        for i in vertexList:
            for j in vertexList:
                if pointDist(i, j) > pointDist(longestPair[0], longestPair[1]):
                    longestPair = (i, j)
        
        center = (int((longestPair[0][0] + longestPair[1][0]) / 2), int((longestPair[0][1] + longestPair[1][1]) / 2))
        radius = int(pointDist(longestPair[0], longestPair[1]) / 2)
        drawCircle(center, radius)


def drawCircle(center, radius):
    pygame.draw.circle(screen, YELLOW, center, radius, 2)
    pygame.display.update()
    

def bvhAABB(clusterList):
    for vertexList in clusterList:
        left = INFINITY
        up = INFINITY
        right = -1
        down = -1
        
        for vertex in vertexList:
            if vertex[0] < left:
                left = vertex[0]
            if vertex[1] < up:
                up = vertex[1]
            if vertex[0] > right:
                right = vertex[0]
            if vertex[1] > down:
                down = vertex[1]
        
        shape = []
        shape.append((left, up))
        shape.append((right, up))
        shape.append((right, down))
        shape.append((left, down))
        shape.append((left, up))
        
        drawRectangle(shape)

        
def drawRectangle(shape):
    pygame.draw.lines(screen, GREEN, False, shape, 2)
    pygame.display.update()
    
    
def bvhOBB(vertexList):
    left = (INFINITY, 0)
    up = (0, INFINITY)
    right = (-1, 0)
    down = (0, -1)
        
    for vertex in vertexList:
        if vertex[0] < left[0]:
            left = vertex
        if vertex[1] < up[1]:
            up = vertex
        if vertex[0] > right[0]:
            right = vertex
        if vertex[1] > down[1]:
            down = vertex
    
    shape = []
    shape.append(left)
    shape.append(UP)
    shape.append(right)
    shape.append(down)
    shape.append(left)
    
    drawRectangle(shape)
    
    
def bvhHull(vertexList):
    left = (INFINITY, 0)
    up = (0, INFINITY)
    right = (-1, 0)
    down = (0, -1)
        
    for vertex in vertexList:
        if vertex[0] < left[0]:
            left = vertex
        if vertex[1] < up[1]:
            up = vertex
        if vertex[0] > right[0]:
            right = vertex
        if vertex[1] > down[1]:
            down = vertex
    
    shape = []
    shape.append(left)
    shape.append(MID)
    shape.append(up)
    shape.append(right)
    shape.append(down)
    shape.append(left)
    
    drawRectangle(shape)
    
    
def pauseStuff():
    print("\nSimulation paused..\n")
    done = 0
    while not done:
        for e in pygame.event.get():
            if e.type == QUIT or (e.type == KEYUP and e.key == K_ESCAPE):
                print("\nSimulation resuming..\n")
                done = 1
                break
        
    
def main():
    vertexList = generateVertex()
    displayVertex(vertexList)
    time.sleep(2)
    clusterList = clusterizeVertex(vertexList)
    drawPoly(clusterList)
    time.sleep(2)
    bvhCircle(clusterList)
    time.sleep(2)
    bvhAABB(clusterList)
    time.sleep(2)
    bvhOBB(clusterList[1])
    time.sleep(2)
    bvhHull(clusterList[2])
    time.sleep(6000)
    
    # print (vertexList)
    # print (pointDist((10,10), (20,20)))


if __name__ == '__main__':
    main()
    pass
