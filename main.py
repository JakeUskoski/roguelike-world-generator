import random
import math
import pygame

MINIMUM_ROOM_SIZE = 8
MAXIMUM_ROOM_SIZE = MINIMUM_ROOM_SIZE * 6

ITERATIONS = 10
BLOCK = 800

TOTAL_TEMPLATES = 1
TEMPLATE_X_DIMENSION = 14
TEMPLATE_Y_DIMENSION = 8
RANDOM_MIN = 8
RANDOM_MAX = 20

SECTION_BOX = 0
SECTION_HAT = 1
SECTION_BUCKET = 2
SECTION_CAP = 3
SECTION_END = 4
SECTION_TL_CORNER = 5
SECTION_TR_CORNER = 6
SECTION_BL_CORNER = 7
SECTION_BR_CORNER = 8
SECTION_COLUMN = 9
SECTION_CORRIDOR = 10
SECTION_T_EDGE = 11
SECTION_B_EDGE = 12
SECTION_L_EDGE = 13
SECTION_R_EDGE = 14
SECTION_MIDDLE = 15

SIDE_LEFT = 0
SIDE_RIGHT = 1


class Rectangle(object):
    def __init__(self, x, y, x_size, y_size):
        self.x = x
        self.y = y
        self.x_size = x_size
        self.y_size = y_size
        self.connections = []
        self.room = None

    def divide(self):
        if self.x_size >= self.y_size:
            # vertical cut
            newXSize = random.randint(math.floor(self.x_size*0.25), math.floor(self.x_size*0.75))
            newX = self.x + self.x_size - newXSize
            self.x_size -= newXSize
            newYSize = self.y_size
            newY = self.y
        else:
            # horizontal cut
            newXSize = self.x_size
            newYSize = random.randint(math.floor(self.y_size*0.25), math.floor(self.y_size*0.75))
            newY = self.y + self.y_size - newYSize
            self.y_size -= newYSize
            newX = self.x

        return Rectangle(newX, newY, newXSize, newYSize)

    def get_values(self):
        return [self.x, self.y, self.x_size, self.y_size]

    def get_connections(self):
        return self.connections

    def get_left_connections(self):
        list = []
        for i in range(self.count_connections()):
            if self.connections[i].x < self.x:
                list.append(self.connections[i])
        return list

    def get_right_connections(self):
        list = []
        for i in range(self.count_connections()):
            if self.connections[i].x > self.x:
                list.append(self.connections[i])
        return list

    def count_connections(self):
        return len(self.connections)

    def add_connection(self, rect):
        self.connections.append(rect)

    def remove_connection(self, rect):
        self.connections.remove(rect)

    def find_rects(self, rects):
        size = len(rects)
        connectedRects = []
        for i in range(size):
            if rects[i].y_size >= MINIMUM_ROOM_SIZE and rects[i].x_size >= MINIMUM_ROOM_SIZE:
                if rects[i].x + rects[i].x_size == self.x or rects[i].x == self.x + self.x_size:
                    if (rects[i].y < self.y and self.y - rects[i].y_size + MINIMUM_ROOM_SIZE <= rects[i].y) or\
                            (rects[i].y >= self.y and rects[i].y + MINIMUM_ROOM_SIZE <= self.y + self.y_size):
                        if rects[i] not in self.connections:
                            connectedRects.append(rects[i])

        size = len(connectedRects)
        if size == 0:
            return
        for i in range(size):
            self.add_connection(connectedRects[i])
            connectedRects[i].add_connection(self)
        for i in range(size):
            connectedRects[i].find_rects(rects)

    def build_room(self):
        self.room = Room(self.x_size, self.y_size, self)


class Room(object):
    def __init__(self, x_size, y_size, parent):
        x_size = x_size // MINIMUM_ROOM_SIZE
        y_size = y_size // MINIMUM_ROOM_SIZE
        self.x_size = x_size * TEMPLATE_X_DIMENSION
        self.y_size = y_size * TEMPLATE_Y_DIMENSION
        self.parent = parent
        self.templates = []
        self.blocks = []
        self.doors = []

        self.__outline_room(x_size, y_size)
        self.__stitch_room(x_size, y_size)
        self.__fetch_doors()

    def __outline_room(self, x_size, y_size):
        connectionsMade = []
        if x_size == 1 and y_size == 1:
            self.templates.append([])
            self.templates[0].append(Section(0, 0, self, SECTION_HAT, connectionsMade))
        elif x_size == 1:
            for i in range(y_size):
                self.templates.append([])
                if i == 0:
                    self.templates[i].append(Section(0, i, self, SECTION_HAT, connectionsMade))
                    print("hat")
                elif i == y_size - 1:
                    self.templates[i].append(Section(0, i, self, SECTION_BUCKET, connectionsMade))
                    print("bucket")
                else:
                    self.templates[i].append(Section(0, i, self, SECTION_COLUMN, connectionsMade))
                    print("column")
        elif y_size == 1:
            self.templates.append([])
            for i in range(x_size):
                if i == 0:
                    self.templates[0].append(Section(i, 0, self, SECTION_CAP, connectionsMade))
                    print("cap")
                elif i == x_size - 1:
                    self.templates[0].append(Section(i, 0, self, SECTION_END, connectionsMade))
                    print("end")
                else:
                    self.templates[0].append(Section(i, 0, self, SECTION_CORRIDOR, connectionsMade))
                    print("corridor")
        else:
            for i in range(y_size):
                self.templates.append([])
                for j in range(x_size):
                    if i == 0:
                        if j == 0:
                            self.templates[i].append(Section(j, i, self, SECTION_TL_CORNER, connectionsMade))
                            print("tl corner")
                        elif j == x_size - 1:
                              self.templates[i].append(Section(j, i, self, SECTION_TR_CORNER, connectionsMade))
                              print("tr corner")
                        else:
                            self.templates[i].append(Section(j, i, self, SECTION_T_EDGE, connectionsMade))
                            print("t edge")
                    elif i == y_size - 1:
                        if j == 0:
                            self.templates[i].append(Section(j, i, self, SECTION_BL_CORNER, connectionsMade))
                            print("bl corner")
                        elif j == x_size - 1:
                            self.templates[i].append(Section(j, i, self, SECTION_BR_CORNER, connectionsMade))
                            print("br corner")
                        else:
                            self.templates[i].append(Section(j, i, self, SECTION_B_EDGE, connectionsMade))
                            print("b edge")
                    else:
                        if j == 0:
                            self.templates[i].append(Section(j, i, self, SECTION_L_EDGE, connectionsMade))
                            print("l edge")
                        elif j == x_size - 1:
                            self.templates[i].append(Section(j, i, self, SECTION_R_EDGE, connectionsMade))
                            print("r edge")
                        else:
                            self.templates[i].append(Section(j, i, self, SECTION_MIDDLE, connectionsMade))
                            print("middle")

    def __stitch_room(self, x_size, y_size):
        print("put room blocks together")
        for i in range(x_size):
            for j in range(y_size):
                set = self.templates[j][i]
                for k in range(j * TEMPLATE_Y_DIMENSION, (j + 1) * TEMPLATE_Y_DIMENSION):
                    if len(self.blocks) <= k:
                        self.blocks.append([])
                    for l in range(i * TEMPLATE_X_DIMENSION, (i + 1) * TEMPLATE_X_DIMENSION):
                        self.blocks[k].append(set.blocks[k - j * TEMPLATE_Y_DIMENSION][l - i * TEMPLATE_X_DIMENSION])

    def __fetch_doors(self):
        for list in self.templates:
            for template in list:
                for door in template.get_doors():
                    self.doors.append(door)


class Section(object):
    def __init__(self, x, y, room, template, connections_made):
        self.x = x
        self.y = y
        self.parent = room
        self.template = template
        self.doors = []
        self.blocks = []

        self.__build_template(connections_made)
        self.__randomize()

    def get_doors(self):
        return self.doors

    def __build_template(self, connections_made):
        name = "templates/" + str(self.template)

        if self.x == 0:
            for rect in self.parent.parent.get_left_connections():
                if self.y == 0 and self.parent.y_size == TEMPLATE_Y_DIMENSION:
                    if self.__add_door(Door(self.parent.parent, rect, SIDE_LEFT), connections_made):
                        name += "_L"
                        break
                elif self.y == 0:
                    if rect.y + rect.y_size / 2 < self.parent.parent.y + TEMPLATE_Y_DIMENSION:
                        if self.__add_door(Door(self.parent.parent, rect, SIDE_LEFT), connections_made):
                            name += "_L"
                            break
                elif self.y == self.parent.y_size / TEMPLATE_Y_DIMENSION - 1:
                    if rect.y + rect.y_size / 2 >= self.parent.parent.y + self.y * TEMPLATE_Y_DIMENSION:
                        if self.__add_door(Door(self.parent.parent, rect, SIDE_LEFT), connections_made):
                            name += "_L"
                            break
                else:
                    if rect.y + rect.y_size / 2 >= self.parent.parent.y + self.y * TEMPLATE_Y_DIMENSION:
                        if rect.y + rect.y_size / 2 < self.parent.parent.y + (self.y + 1) * TEMPLATE_Y_DIMENSION:
                            if self.__add_door(Door(self.parent.parent, rect, SIDE_LEFT), connections_made):
                                name += "_L"
                                break

        if self.x == self.parent.x_size / TEMPLATE_X_DIMENSION - 1:
            for rect in self.parent.parent.get_right_connections():
                if self.y == 0 and self.parent.y_size == TEMPLATE_Y_DIMENSION:
                    if self.__add_door(Door(self.parent.parent, rect, SIDE_RIGHT), connections_made):
                        name += "_R"
                        break
                elif self.y == 0:
                    if rect.y + rect.y_size / 2 < self.parent.parent.y + TEMPLATE_Y_DIMENSION:
                        if self.__add_door(Door(self.parent.parent, rect, SIDE_RIGHT), connections_made):
                            name += "_R"
                            break
                elif self.y == self.parent.y_size / TEMPLATE_Y_DIMENSION - 1:
                    if rect.y + rect.y_size / 2 >= self.parent.parent.y + self.y * TEMPLATE_Y_DIMENSION:
                        if self.__add_door(Door(self.parent.parent, rect, SIDE_RIGHT), connections_made):
                            name += "_R"
                            break
                else:
                    if rect.y + rect.y_size / 2 >= self.parent.parent.y + self.y * TEMPLATE_Y_DIMENSION:
                        if rect.y + rect.y_size / 2 < self.parent.parent.y + (self.y + 1) * TEMPLATE_Y_DIMENSION:
                            if self.__add_door(Door(self.parent.parent, rect, SIDE_RIGHT), connections_made):
                                name += "_R"
                                break

        rnd = random.randint(0, TOTAL_TEMPLATES - 1)
        if rnd < 10:
            num = "0" + str(rnd)
        else:
            num = str(rnd)
        name += "/" + num + ".txt"
        file = open(name)

        for i in range(TEMPLATE_Y_DIMENSION):
            string = file.readline()
            if i >= len(self.blocks):
                self.blocks.append([])
            for j in range(TEMPLATE_X_DIMENSION):
                self.blocks[i].append(int(string[j]))
                if self.blocks[i][j] == 3 and i > 0:
                    if self.blocks[i-1][j] == 3:
                        if j == 0:
                            self.__get_left_door().set_xy(j, i)
                        else:
                            self.__get_right_door().set_xy(j, i)

    def __get_left_door(self):
        for door in self.doors:
            if door.side == SIDE_LEFT:
                return door

    def __get_right_door(self):
        for door in self.doors:
            if door.side == SIDE_RIGHT:
                return door

    def __add_door(self, door, connections_made):
        for connection in connections_made:
            if connection is door.connection:
                return False
        self.doors.append(door)
        connections_made.append(door.connection)
        return True

    def __randomize(self):
        iterations = random.randint(RANDOM_MIN, RANDOM_MAX)
        for i in range(iterations):
            ready = False
            while not ready:
                ready = True
                x = random.randint(0, TEMPLATE_X_DIMENSION - 1)
                y = random.randint(0, TEMPLATE_Y_DIMENSION - 1)
                if self.blocks[y][x] == 9 or self.blocks[y][x] == 8 or self.blocks[y][x] == 3:
                    ready = False
                else:
                    attempt = True
                    while attempt:
                        rnd = random.randint(0, 2)
                        if rnd == 0:
                            if self.blocks[y][x] != 2:
                                self.blocks[y][x] = 0
                                attempt = False
                        elif rnd == 1:
                            self.blocks[y][x] = 1
                            attempt = False
                        else:
                            if y != TEMPLATE_Y_DIMENSION - 1 and self.blocks[y+1][x] != 1 and self.blocks[y+1][x] != 2 and self.blocks[y+1][x] != 9:
                                if (x != 0 and (self.blocks[y][x-1] == 1 or self.blocks[y][x-1] == 2)) or\
                                        (x != TEMPLATE_X_DIMENSION - 1 and (self.blocks[y][x+1] == 1 or self.blocks[y][x+1] == 2)):
                                    self.blocks[y][x] = 2


class Door(object):
    def __init__(self, rect, connect, side):
        self.parent = rect
        self.side = side
        self.connection = connect
        self.x = 0
        self.y = 0

    def set_x(self, x):
        self.x = x

    def set_y(self, y):
        self.y = y

    def set_xy(self, x, y):
        self.x = x
        self.y = y


if __name__ == '__main__':
    mcNum = 0
    rectList = []
    ready = False
    div = True
    while not ready:
        largestX = 0
        largestY = 0
        averageX = 0
        averageY = 0
        largestVolume = 0
        mostConnections = 0
        rectList.clear()
        rectList.append(Rectangle(0, 0, BLOCK, BLOCK))
        i = 0
        div = True
        while div:
            div = False
            if i < ITERATIONS:
                div = True
            size = len(rectList)
            for j in range(size):
                if rectList[j].x_size >= MINIMUM_ROOM_SIZE * 2 and rectList[j].y_size >= MINIMUM_ROOM_SIZE * 2:
                    if i < ITERATIONS or (rectList[j].x_size >= MAXIMUM_ROOM_SIZE and rectList[j].y_size >= MAXIMUM_ROOM_SIZE):
                        rectList.append(rectList[j].divide())
                        div = True
            print(str(i))
            i += 1
        for i in range(len(rectList)):
            if rectList[i].x == 0 and rectList[i].y == 0:
                rectList[i].find_rects(rectList)

        connected = []
        count = 0
        for i in range(len(rectList)):
            if rectList[i].count_connections() > 0:
                count += 1
                connected.append(rectList[i])

            if rectList[i].x_size * rectList[i].y_size > largestVolume:
                largestVolume = rectList[i].x_size * rectList[i].y_size
                largestX = rectList[i].x_size
                largestY = rectList[i].y_size
            if rectList[i].count_connections() > mostConnections:
                mostConnections = rectList[i].count_connections()
                mcNum = i
            averageX += rectList[i].x_size
            averageY += rectList[i].y_size

        volume = 0
        for i in range(len(connected)):
            volume += connected[i].x_size * connected[i].y_size

        total = len(rectList)

        print("Accessible Rooms: " + str(count) + ", Total rooms: " + str(total))

        if volume >= BLOCK * BLOCK * 0.75:
            ready = True
            templates = (largestX // MINIMUM_ROOM_SIZE) * (largestY // MINIMUM_ROOM_SIZE)
            averageX /= total
            averageY /= total
            averageTemplates = (averageX // MINIMUM_ROOM_SIZE) * (averageY // MINIMUM_ROOM_SIZE)
            print("Largest room's volume: " + str(largestVolume))
            print("Largest room's X size: " + str(largestX))
            print("Largest room's Y size: " + str(largestY))
            print("Largest room's templates: " + str(templates))
            print("Most connections: " + str(mostConnections))
            print("Average room's X size: " + str(averageX))
            print("Average room's Y size: " + str(averageY))
            print("Average room's templates:" + str(averageTemplates))
            rectList[mcNum].build_room()
            print("Connections to room: " + str(rectList[mcNum].count_connections()))
            print("Doors: " + str(len(rectList[mcNum].room.doors)))
            print("Room y size: " + str(rectList[mcNum].y_size))
        else:
            print("Not Enough Rooms")


    """
     Pygame base template for opening a window

     Sample Python/Pygame Programs
     Simpson College Computer Science
     http://programarcadegames.com/
     http://simpson.edu/computer-science/

     Explanation video: http://youtu.be/vRB_983kUMc
    """

    # Define some colors
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    BLUE = (0, 0, 255)
    GREEN = (0, 255, 0)
    RED = (255, 0, 0)
    TEAL = (0, 255, 255)
    PURPLE = (255, 0, 255)
    YELLOW = (255, 255, 0)

    pygame.init()

    # Set the width and height of the screen [width, height]
    size = (1400, 800)
    screen = pygame.display.set_mode(size)

    pygame.display.set_caption("My Game")

    # Loop until the user clicks the close button.
    done = False

    # Used to manage how fast the screen updates
    clock = pygame.time.Clock()

    # -------- Main Program Loop -----------
    while not done:
        # --- Main event loop
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True

        # --- Game logic should go here

        # --- Screen-clearing code goes here

        # Here, we clear the screen to white. Don't put other drawing commands
        # above this, or they will be erased with this command.

        # If you want a background image, replace this clear with blit'ing the
        # background image.
        screen.fill(WHITE)

        """
        # --- Drawing code should go here
        size = len(rectList)
        for i in range(size):
            if rectList[i].count_connections() > 0:
                decrease2 = 0
                decrease = rectList[i].count_connections() * 50
                if(decrease >= 250):
                    decrease2 = decrease - 250
                    decrease -= decrease2
                c = pygame.Color(250 - decrease, 200, 250 - decrease2, 255)
                pygame.draw.rect(screen, c, rectList[i].get_values(), 0)
                pygame.draw.rect(screen, BLACK, rectList[i].get_values(), 1)
        """
        room = rectList[mcNum].room
        if len(room.blocks[0]) * 10 > size[0] or len(room.blocks) * 10 > size[1]:
            if len(room.blocks[0]) * 8 > size[0] or len(room.blocks) * 8 > size[1]:
                NUM = 6
            else:
                NUM = 8
        else:
            NUM = 10
        for i in range(len(room.blocks)):
            for j in range(len(room.blocks[i])):
                if room.blocks[i][j] == 0:
                    pygame.draw.rect(screen, WHITE, (j * NUM, i * NUM, NUM, NUM), 0)
                    pygame.draw.rect(screen, BLACK, (j * NUM, i * NUM, NUM, NUM), 1)
                elif room.blocks[i][j] == 1:
                    pygame.draw.rect(screen, BLACK, (j * NUM, i * NUM, NUM, NUM), 0)
                    pygame.draw.rect(screen, BLACK, (j * NUM, i * NUM, NUM, NUM), 1)
                elif room.blocks[i][j] == 2:
                    pygame.draw.rect(screen, GREEN, (j * NUM, i * NUM, NUM, NUM/2), 0)
                    pygame.draw.rect(screen, BLACK, (j * NUM, i * NUM, NUM, NUM), 1)
                elif room.blocks[i][j] == 3:
                    pygame.draw.rect(screen, RED, (j * NUM, i * NUM, NUM, NUM), 0)
                    pygame.draw.rect(screen, BLACK, (j * NUM, i * NUM, NUM, NUM), 1)
                elif room.blocks[i][j] == 8:
                    pygame.draw.rect(screen, PURPLE, (j * NUM, i * NUM, NUM, NUM), 0)
                    pygame.draw.rect(screen, BLACK, (j * NUM, i * NUM, NUM, NUM), 1)
                elif room.blocks[i][j] == 9:
                    pygame.draw.rect(screen, BLUE, (j * NUM, i * NUM, NUM, NUM), 0)
                    pygame.draw.rect(screen, BLACK, (j * NUM, i * NUM, NUM, NUM), 1)
                else:
                    pygame.draw.rect(screen, TEAL, (j * NUM, i * NUM, NUM, NUM), 0)
                    pygame.draw.rect(screen, BLACK, (j * NUM, i * NUM, NUM, NUM), 1)

        # --- Go ahead and update the screen with what we've drawn.
        pygame.display.flip()

        # --- Limit to 60 frames per second
        clock.tick(60)

    # Close the window and quit.
    pygame.quit()