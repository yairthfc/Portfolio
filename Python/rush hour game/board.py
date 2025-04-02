class Board:
    """
    Add a class description here.
    Write briefly about the purpose of the class
    """

    def __init__(self):
        # implement your code and erase the "pass"
        # Note that this function is required in your Board implementation.
        # implement your code and erase the "pass"
        board = []
        for x in range(7):
            line = []
            for y in range(7):
                 line.append("_")
                 if (x,y) == (3,6):
                    line.append('E')
            board.append(line)
        self.__cars = {}
        self.__board = board

    def __str__(self):
        """
        This function is called when a board object is to be printed.
        :return: A string of the current status of the board
        """
        # The game may assume this function returns a reasonable representation
        # of the board for printing, but may not assume details about it.
        # implement your code and erase the "pass"
        string = "\n"
        for line in range(len(self.__board)):
            for spot in self.__board[line]:
                string = string + " " + str(spot)
            string = string + "\n"
        return string

    def get_car_dict(self):
        return self.__cars

    def cell_list(self):
        """ This function returns the coordinates of cells in this board
        :return: list of coordinates
        """
        # In this board, returns a list containing the cells in the square
        # from (0,0) to (6,6) and the target cell (3,7)
        # implement your code and erase the "pass"
        list_of_cells = []
        for x in range(len(self.__board)):
            for y in range(len(self.__board[0])):
                list_of_cells.append((x,y))
                if (x,y) == (3,6):
                    list_of_cells.append((3,7))
        return list_of_cells
        

    def possible_moves(self):
        """ This function returns the legal moves of all cars in this board
        :return: list of tuples of the form (name,move_key,description) 
                 representing legal moves
        """
        # From the provided example car_config.json file, the return value could be
        # [('O','d',"some description"),('R','r',"some description"),('O','u',"some description")]
        # implement your code and erase the "pass"
        list_of_moves = []
        for x in self.__cars.values():
            cord = x.car_coordinates()
            pos_moves = x.possible_moves()
            if 'u' in pos_moves and cord[0][0] > 0:
                list_of_moves.append((x.get_name(),'u',"can go up"))
            if 'd' in pos_moves and cord[-1][0] < 6:
                list_of_moves.append((x.get_name(),'d',"can go down"))
            if 'l' in pos_moves and cord[0][1] > 0:
                list_of_moves.append((x.get_name(),'l',"can go left"))
            if 'r' in pos_moves and ((cord[-1][1] < 6) or (cord[-1] == (3,6))):
                list_of_moves.append((x.get_name(),'r',"can go right"))
        return list_of_moves

    def target_location(self):
        """
        This function returns the coordinates of the location which is to be filled for victory.
        :return: (row,col) of goal location
        """
        # In this board, returns (3,7)
        # implement your code and erase the "pass"
        return (3,7)

    def cell_content(self, coordinate):
        """
        Checks if the given coordinates are empty.
        :param coordinate: tuple of (row,col) of the coordinate to check
        :return: The name if the car in coordinate, None if empty
        """
        # implement your code and erase the "pass"
        if self.__board[coordinate[0]][coordinate[1]] in '_E':
            return None
        else:
            return self.__board[coordinate[0]][coordinate[1]]

    def add_car(self, car):
        """
        Adds a car to the game.
        :param car: car object of car to add
        :return: True upon success. False if failed
        """
        # Remember to consider all the reasons adding a car can fail.
        # You may assume the car is a legal car object following the API.
        # implement your code and erase the "pass"
        cord = car.car_coordinates()
        if car.get_name() in self.__cars:
            return False
        for x in cord:
            if (x not in self.cell_list()) or (self.cell_content(x) != None):
                return False
            else: 
                continue
        for x in cord:
            self.__board[x[0]][x[1]] = car.get_name()
        self.__cars[car.get_name()] = car
        return True


    def move_car(self, name, move_key):
        """
        moves car one step in given direction.
        :param name: name of the car to move
        :param move_key: Key of move in car to activate
        :return: True upon success, False otherwise
        """
        # implement your code and erase the "pass"
        if name in self.__cars:
            car = self.__cars[name]
            cord = car.car_coordinates()
            if move_key == 'u':
                desc = "can go up"
            elif move_key == 'd':
                desc = "can go down"
            elif move_key == 'l':
                desc = "can go left"
            else:
                desc = "can go right"
            if (name,move_key,desc) in self.possible_moves():
                move_tbd = car.movement_requirements(move_key)[0]
                if self.cell_content(move_tbd) == None:
                    if car.move(move_key):
                        if move_key == 'u':
                            self.__board[move_tbd[0]][move_tbd[1]] = name
                            self.__board[cord[-1][0]][cord[-1][1]] = '_'
                        if move_key == 'd':
                            self.__board[move_tbd[0]][move_tbd[1]] = name
                            self.__board[cord[0][0]][cord[0][1]] = '_'
                        if move_key == 'l':
                            self.__board[move_tbd[0]][move_tbd[1]] = name
                            self.__board[cord[-1][0]][cord[-1][1]] = '_'
                        if move_key == 'r':
                            self.__board[move_tbd[0]][move_tbd[1]] = name
                            self.__board[cord[0][0]][cord[0][1]] = '_'
                        return True
                    else:
                        return False
                else:
                    return False
            else:
                return False
        else:
            return False