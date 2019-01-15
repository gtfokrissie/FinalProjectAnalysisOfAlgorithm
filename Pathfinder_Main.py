import os
import pygame
from pygame.locals import *
from random import randint

import Graph
import Graphics
import Entity
from Pathfinder import Pathfinder

pathfinderAlgo = 'A*'
displayGraphOverlay = False

overlayMap_width = 1675
overlayMap_height = 862

mapNodes = None
overlayMap = None
overlayMapRect = None
clickCounter = 0

car = None
pathIndex = 0
pathfinder = None

nodeGeneratorMode = False
clickCounter = 90

forceUpdate = False

# PATHFINDER HELPER FUNCTIONS
def nodeIndexer (node) :
    return 'x:' + str(node['x']) + '-y:'+str(node['y'])

def getNodeNeighbor (node) :
    neighbors = []

    for links in node['linkTo'] :
        neighbors.append(mapNodes[links])

    return neighbors

def manhattanDistance (a, b) :
    return ( abs(a['x'] - b['x']) + abs(a['y'] - b['y']) )

def isGoal (a, b) :
    return manhattanDistance(a, b) == 0
    # ((a['x'] == b['x']) and a['y'] == b['y'])
# END OF PATHFINDER HELPER FUNCTIONS

def getNearestNode (x, y) :
    dist = overlayMap_width * overlayMap_height
    node = None

    for currentNode in mapNodes:
        currentDist = manhattanDistance({
            'x': x,
            'y': y
        }, currentNode)
        if dist > currentDist:
            dist = currentDist
            node = currentNode

    return node

def mouseDown (event) :
    global clickCounter
    global car
    global pathfinder
    global pathIndex
    global forceUpdate

    if nodeGeneratorMode == False :
        carStartingNode = getNearestNode(car.posX, car.posY)
        carEndNode = getNearestNode(event[0], event[1])

        pathfinder = Pathfinder(pathfinderAlgo, carStartingNode, carEndNode, manhattanDistance)

        pathfinder.nodeIndexer = nodeIndexer
        pathfinder.getNodeNeighbor = getNodeNeighbor
        pathfinder.isGoal = isGoal

        pathfinder.computePath()

        pathIndex = -1
        forceUpdate = True
    else :
        # Spawn new entity on mouse click, or move entity on second click
        Entity.newEntity(event[0], event[1])

        print("{'x': "+str(event[0])+", 'y': "+str(event[1])+", 'linkTo': ["+ str(clickCounter - 1)+","+ str(clickCounter + 1)+"]}, #" + str(clickCounter) + " " + str(clickCounter + 1))
        clickCounter += 1

def update (renderEngine) :
    #entities = Entity.getEntities()

    #for entity in entities:
    #    entity.update()
    # Make the car follow a path
    global pathIndex
    global car
    global pathfinder
    global forceUpdate

    if car == None:
        return

    carToNodeDistance = abs(car.posX - car.targetX) + abs(car.posY - car.targetY)

    if (forceUpdate or (carToNodeDistance <= 0.6 and pathfinder != None)) :
        forceUpdate = False
        if pathIndex < len(pathfinder.paths) - 1:
            pathIndex += 1

        car.changeTarget(pathfinder.paths[pathIndex]['x'], pathfinder.paths[pathIndex]['y'])

    car.update()


def draw (renderEngine) :
    global pathfinder

    entities = Entity.getEntities()
    renderEngine._display_surf.fill(Graphics.WHITE)
    renderEngine._display_surf.blit(overlayMap, overlayMapRect)

    if displayGraphOverlay:
        for node in mapNodes:
            posX = node['x']
            posY = node['y']

            for link in node['linkTo']:
                currentLinkNode = mapNodes[link]
                link_posX = currentLinkNode['x']
                link_posY = currentLinkNode['y']

                pygame.draw.line(renderEngine._display_surf, Graphics.BLACK, [posX, posY], [link_posX, link_posY], 5)

            pygame.draw.circle(renderEngine._display_surf, Graphics.RED, [posX, posY], 5)

    if pathfinder != None :
        pathIterator = 0

        while pathIterator < len(pathfinder.paths) - 1 :
            current = pathfinder.paths[pathIterator]
            next = pathfinder.paths[pathIterator + 1]

            curX = current['x']
            curY = current['y']

            nextX = next['x']
            nextY = next['y']

            pygame.draw.line(renderEngine._display_surf, Graphics.BLUE, [curX, curY], [nextX, nextY], 5)

            pathIterator += 1


    for entity in entities:
        pygame.draw.circle(renderEngine._display_surf, Graphics.GREEN, [round(entity.posX), round(entity.posY)], 5)

def changeAlgorithm (button) :
    global pathfinderAlgo
    
    if pathfinderAlgo == 'A*':
        pathfinderAlgo = 'Floodfill'
        button['label'] = 'Use A*'
        print('Search algorithm switched to floodfill')
    else:
        pathfinderAlgo = 'A*'
        button['label'] = 'Use Floodfill'
        print('Search algorithm switched to A*')

# Program entry point
if __name__ == "__main__":
    pathfinderAlgo = 'A*' 

    mapNodes = Graph.getNodes()

    # Create car object

    # carStartingNode = mapNodes[randint(0, len(mapNodes))] # Uncomment for random staring point
    carStartingNode = mapNodes[153] 

    car = Entity.newEntity(carStartingNode['x'], carStartingNode['y'])
    car.moveSpeed = 5
    car.timeSpeedup = 4

    
    renderEngine = Graphics.Init(overlayMap_width, overlayMap_height)
    renderEngine.on_loop   = update
    renderEngine.on_render = draw
    renderEngine.on_mouseDown = mouseDown

    overlayMap = pygame.image.load('sample_map.png')
    overlayMapRect = overlayMap.get_rect()

    renderEngine.button(20, 20, 135, 35, "Use Floodfill", changeAlgorithm)

    renderEngine.on_execute()
