import pygame
import math
import time
from copy import deepcopy
from operator import itemgetter
#import logging

from Map import Map

class Options:
    """
\t--help                   (to show this help and exit)
\t--width                  <number of cells wide the map is>
\t--height                 <number of cells tall the map is>
\t--cell_size              <number of pixels square each cell is>
    """
    def __init__(self):
        self.width         = 64 #: integer cell count
        self.height        = 64 #: integer cell count
        self.cell_size     = 25 #: integer cell size

    def parse_args(self, args):
        argind = 1
        while argind < len(args):
            if args[argind] == '--width':
                self.width = int(args[argind+1])
                argind += 1
            elif args[argind] == '--height':
                self.height = int(args[argind+1])
                argind += 1
            elif args[argind] == '--cell_size':
                self.cell_size = int(args[argind+1])
                argind += 1
            elif args[argind] == "--help":
                self.print_usage(args[0])
                return -1
            argind += 1
        return 0

    def print_usage(self, name):
        print """Usage:\n{}{}""".format(name, self.__doc__)

def main( argv ):
    options = Options()
    if options.parse_args(argv):
        return -1

    # general map stats
    map_width = options.width
    map_height = options.height
    tile_size = options.cell_size


    center_location = (math.floor(map_width/2)-1, math.floor(map_height/2)-1)
    #center_location = (6,2)
    obstacle_list = []

        
    cellMap = Map(width=map_width,
                  height=map_height,
                  center_location=center_location,
                  obstacles=obstacle_list)
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


if __name__ == "__main__":
    import sys
    main(sys.argv)

