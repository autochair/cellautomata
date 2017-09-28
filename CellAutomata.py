import pygame
import math
import time
from copy import deepcopy
from operator import itemgetter
#import logging


class CellAutomata:

    """

    This class implements cellular atomata for determining paths to a
    goal in a map with obstacles.

    """

    #define colors
    obstacle_color = (0,0,0)
    target_color = (255,255,255)
    north_color = (255,0,0)
    south_color = (0,255,0)
    east_color = (255,125,0)
    west_color = (0,0,255)
    
    northeast_color = (255,80,0)
    northwest_color = (255,0,255)
    southeast_color = (160,200,0)
    southwest_color = (0,125,255)
    center_color = (135,64,8)

    # define tile types and positions
    obstacle = 0
    target = 1
    northwest = 2
    north = 3
    northeast = 4
    west = 5
    east = 6
    southwest = 7
    south = 8
    southeast = 9
    center = 10

   

    def __init__(self, width, height, center_location, obstacles):

        # set map values
        self.width = width
        self.height = height
        self.center_location = (math.floor(width/2)-1, math.floor(height/2)-1)
        self.obstacles = obstacles

        # generate outside rooms
        self.map = self._generate_map(
            self.width,
            self.height,
            self.center_location,
            self.obstacles)
        #self.map = self._generate_empty_noise_grid(width, height)

    def _generate_center_only_grid(self, width, height, center_location):

        new_map_grid = []
        cx = center_location[0] 
        cy = center_location[1] 

        '''
        print(width)
        print(height)
        for x in range(height):
            new_map_grid.append([]) # add our columns to the array
            for y in range(width):
                new_map_grid[x].append(y)
                print((x,y))
        print(new_map_grid)
        '''
        for x in range(height):
            new_map_grid.append([]) # add our rows to the array
            for y in range(width):
                
                dx = cx - x
                dy = cy - y
                

                
                if dx == 0 and dy == 0:
                    new_map_grid[x].append(self.target)
                elif math.fabs(dx) == math.fabs(dy):
                    if dx > 0 and dy > 0:
                        new_map_grid[x].append(self.southeast)
                    elif dx > 0 and dy < 0:
                        new_map_grid[x].append(self.southwest)
                    elif dx < 0 and dy > 0:
                        new_map_grid[x].append(self.northeast)
                    elif dx < 0 and dy < 0:
                        new_map_grid[x].append(self.northwest)
                elif math.fabs(dx) > math.fabs(dy):
                    if dx > 0:
                        new_map_grid[x].append(self.south)
                    else:
                        new_map_grid[x].append(self.north)
                else:
                    if dy > 0:
                        new_map_grid[x].append(self.east)
                    else:
                        new_map_grid[x].append(self.west)

                #print((x,y,dx,dy))
                        
                        

        return new_map_grid

    def _place_obstacles(self, map_grid, obstacles):

        for ob in obstacles:
            map_grid[ob[0]][ob[1]] = self.obstacle
        return map_grid

    
    def _generate_map(self, width, height, center_location, obstacles):
        '''
        creates a grid
        '''

        #create a grid with center tile and all others pointing towards it
        self.clean_map = self._generate_center_only_grid(width, height, center_location)

        new_map_grid = self._place_obstacles(deepcopy(self.clean_map), obstacles)

        return new_map_grid

    def _toggle_obstacle(self,ob):
        x = int(ob[1])
        y = int(ob[0])
        print((x,y))
        print(self.map[x][y])
        print(self.clean_map[x][y])
        if self.map[x][y] == self.obstacle:
            self.map[x][y] = self.clean_map[x][y]
        else:
            self.map[x][y] = self.obstacle
        print(self.map[x][y])
        print(self.clean_map[x][y])

    def _update_map(self, map, jumpLevel):
        
        grid = map
        next_grid = []
        for x, row in enumerate(grid):
            next_row = []
            next_grid.append(next_row)
            for y, tile in enumerate(row):

                
                center = grid[x][y]

                nextCoord = self.getNextCoord((x,y),center) #coordinate of next

                #if(not self.isValid(grid, (x,y), nextCoord)):
                if center != self.obstacle and center != self.target:
                    neighborCoords = self.getPrioritizedNeighbors(grid,(x,y))
                    
                    allInvalid = True
                    lastChoice = (x,y)
                    for neighborCoord in neighborCoords:
                        if(self.isValid(grid, (x,y), neighborCoord)):
                            grid[x][y] = self.pointAt((x,y), neighborCoord)
                            allInvalid = False
                            break
                    if allInvalid:  #if all are invalid, pick the best one for now
                        for neighborCoord in neighborCoords:
                            if neighborCoord != nextCoord:
                                lastChoice = neighborCoord
                                break
                        grid[x][y] = self.pointAt((x,y), lastChoice)
                        #grid[x][y] = self.center

                #next_column.append(next_cell)
        grid = next_grid
                   
        return next_grid

    def getNextCoord(self,currentCoord, direction):
        offset = self.getOffsetFromDirection(direction)
        newX = currentCoord[0] + offset[0]
        newY = currentCoord[1] + offset[1]
        return (newX,newY)

    def getOffsetFromDirection(self, nextDirection):
        if nextDirection == self.northwest:
            return (-1,-1)
        if nextDirection == self.north:
            return (-1,0)
        if nextDirection == self.northeast:
            return (-1,1)
        if nextDirection == self.west:
            return (0,-1)
        if nextDirection == self.center:
            return (0,0)
        if nextDirection == self.east:
            return (0,1)
        if nextDirection == self.southwest:
            return (1,-1)
        if nextDirection == self.south:
            return (1,0)
        if nextDirection == self.southeast:
            return (1,1)
        return (0,0)

    def getDirectionFromOffset(self, offset):
        if offset == (-1,-1):
            return self.northwest
        if offset == (-1,0):
            return self.north
        if offset == (-1,1):
            return self.northeast
        if offset == (0,-1):
            return self.west
        if offset == (0,0):
            return self.center
        if offset == (0,1):
            return self.east
        if offset == (1,-1):
            return self.southwest
        if offset == (1,0):
            return self.south
        if offset == (1,1):
            return self.southeast
        return self.center

    def isValid(self, map, currentCoord, nextCoord):
        curX = currentCoord[0]
        curY = currentCoord[1]
        nextX = nextCoord[0]
        nextY = nextCoord[1]
        nextDirection = map[nextX][nextY]
        nextDestCoord = self.getNextCoord(nextCoord, nextDirection)
        nextDestX = nextDestCoord[0]
        nextDestY = nextDestCoord[1]

        #isObstacle = map[curX][curY] == self.obstacle  
        isObstacle = False   #obstacles are returned from getPrioritizedNeighbors

        isNextAtTarget = nextDirection == self.target

        if isObstacle or isNextAtTarget:
            return True

        isNextObstacle = nextDirection == self.obstacle
        
        isNextPointingAtObstacle =  not isNextObstacle and map[nextDestX][nextDestY] == self.obstacle

        isPointingAtNeighbor = math.sqrt(math.pow(curX - nextDestX, 2) + math.pow(curY - nextDestY, 2)) < 1.42



        return not isNextObstacle and (isNextPointingAtObstacle or not isPointingAtNeighbor)

    def getPrioritizedNeighbors(self, grid, currentCoord):
        #first generate a list of all neighbor coordinates and distance from center 
        neighborTuples = []
        cx = self.center_location[0] 
        cy = self.center_location[1] 

        for x, y in [(-1,-1),(-1,0),(-1,1),(0,-1),(0,1),(1,-1),(1,0),(1,1)]:
            neighborCoordx = currentCoord[0] + x
            neighborCoordy = currentCoord[1] + y
            distance = math.sqrt(math.pow(neighborCoordx - cx, 2) + math.pow(neighborCoordy - cy, 2))
            if neighborCoordx >= 0 and neighborCoordy >= 0 and neighborCoordx < self.height and neighborCoordy < self.width and grid[neighborCoordx][neighborCoordy] != self.obstacle:
                neighborTuples.append((neighborCoordx, neighborCoordy, distance))

        #sort by distance and make new list
        sortedTuples = sorted(neighborTuples, key=itemgetter(2))

        returnTuples = []
        for x,y,z in sortedTuples:
            returnTuples.append((x,y))
        if not returnTuples:
            returnTuples.append((0,0))  #put self at very end
        return returnTuples

    def pointAt(self, currentCoord, nextCoord):
        offsetx = nextCoord[0] - currentCoord[0]
        offsety = nextCoord[1] - currentCoord[1]

        return self.getDirectionFromOffset((offsetx,offsety))
