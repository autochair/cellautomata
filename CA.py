import pygame
import math
import time
from copy import deepcopy
from operator import itemgetter
#import logging


class MapGrid():

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

   

    def __init__(self, map_width, map_height, center_location, obstacle_list):

        # set map values
        self.map_width = map_width
        self.map_height = map_height
        self.center_location = center_location
        self.obstacle_list = obstacle_list

        # generate outside rooms
        self.map = self._generate_map(self.map_width, self.map_height, self.center_location, self.obstacle_list)
        #self.map = self._generate_empty_noise_grid(map_width, map_height)

    def _generate_center_only_grid(self, map_width, map_height, center_location):

        new_map_grid = []
        cx = center_location[0] 
        cy = center_location[1] 

        '''
        print(map_width)
        print(map_height)
        for x in range(map_height):
            new_map_grid.append([]) # add our columns to the array
            for y in range(map_width):
                new_map_grid[x].append(y)
                print((x,y))
        print(new_map_grid)
        '''
        for x in range(map_height):
            new_map_grid.append([]) # add our rows to the array
            for y in range(map_width):
                
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

    def _place_obstacles(self, map_grid, obstacle_list):

        for ob in obstacle_list:
            map_grid[ob[0]][ob[1]] = self.obstacle
        return map_grid

    
    def _generate_map(self, map_width, map_height, center_location, obstacle_list):
        '''
        creates a grid
        '''

        #create a grid with center tile and all others pointing towards it
        self.clean_map = self._generate_center_only_grid(map_width, map_height, center_location)

        new_map_grid = self._place_obstacles(deepcopy(self.clean_map), obstacle_list)

        return new_map_grid

    def _toggle_obstacle(self,ob):
        x = ob[1]
        y = ob[0]
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
            if neighborCoordx >= 0 and neighborCoordy >= 0 and neighborCoordx < self.map_height and neighborCoordy < self.map_width and grid[neighborCoordx][neighborCoordy] != self.obstacle:
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
        


                    
if __name__ == '__main__':


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
    '''
    northeast_color = (0,0,0)
    northwest_color = (0,0,0)
    southeast_color = (0,0,0)
    southwest_color = (0,0,0)
    '''
    center_color = (135,64,8)


    # general map stats
    map_width = 64
    map_height = 64
    tile_size = 25

    center_location = (math.floor(map_width/2)-1, math.floor(map_height/2)-1)
    #center_location = (6,2)
    obstacle_list = []

        
    map_grid = MapGrid(map_width, map_height, center_location, obstacle_list)
    #print map_grid.map

    pygame.init()

    screen = pygame.display.set_mode((map_width * tile_size,map_height * tile_size))
    
    obstacle_tile = pygame.Surface((tile_size,tile_size))
    obstacle_tile.fill(obstacle_color)

    target_tile = pygame.Surface((tile_size, tile_size))
    target_tile.fill(target_color)
    
    north_tile = pygame.Surface((tile_size, tile_size))
    north_tile.fill(north_color)
    
    south_tile = pygame.Surface((tile_size, tile_size))
    south_tile.fill(south_color)
    
    east_tile = pygame.Surface((tile_size, tile_size))
    east_tile.fill(east_color)
    
    west_tile = pygame.Surface((tile_size, tile_size))
    west_tile.fill(west_color)
    
    northeast_tile = pygame.Surface((tile_size, tile_size))
    northeast_tile.fill(northeast_color)
    
    northwest_tile = pygame.Surface((tile_size, tile_size))
    northwest_tile.fill(northwest_color)
    
    southeast_tile = pygame.Surface((tile_size, tile_size))
    southeast_tile.fill(southeast_color)
    
    southwest_tile = pygame.Surface((tile_size, tile_size))
    southwest_tile.fill(southwest_color)
    
    center_tile = pygame.Surface((tile_size, tile_size))
    center_tile.fill(center_color)
    
    colors = {0: obstacle_tile,
             1: target_tile,
             2: northwest_tile,
             3: north_tile,
             4: northeast_tile,
             5: west_tile,
             6: east_tile,
             7: southwest_tile,
             8: south_tile,
             9: southeast_tile,
             10: center_tile}

    background = pygame.Surface((map_width * tile_size,map_height * tile_size))

    clock = pygame.time.Clock()

    idle = True
    i = 0
    currentCell = (0,0)
    running = True
    while running == True:
        #clock.tick(3)
        pygame.display.set_caption('Cell: ' + str(currentCell) + " Generations: " + str(i))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                ob = tuple(math.floor(ti/tile_size) for ti in event.pos)
                print(ob)
                map_grid._toggle_obstacle(ob)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE or pygame.K_RIGHT:
                    idle = False
            if event.type == pygame.MOUSEMOTION:
                currentCell = tuple(math.floor(ti/tile_size) for ti in reversed(event.pos)) 

        if idle:
            themap = map_grid.map
        else:
            themap = map_grid._update_map(themap, 1)
            idle = True
            i+=1

        for column_index, column in enumerate(themap):
            for tile_index, tile in enumerate(column):
                screen.blit(colors[tile], (tile_index * tile_size, column_index * tile_size))

        pygame.display.flip()

       
    pygame.quit()
