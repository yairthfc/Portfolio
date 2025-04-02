class Car:
    """
    Add class description here
    """
    def __init__(self, name, length, location, orientation):
        """
        A constructor for a Car object
        :param name: A string representing the car's name
        :param length: A positive int representing the car's length.
        :param location: A tuple representing the car's head (row, col) location
        :param orientation: One of either 0 (VERTICAL) or 1 (HORIZONTAL)
        """
        # Note that this function is required in your Car implementation.
        # implement your code and erase the "pass"
        self.__name = name
        self.__length = length
        self.__location = location
        self.__orientation = orientation
    def car_coordinates(self):
        """
        :return: A list of coordinates the car is in
        """
        cordinates = []
        x,y = self.__location
        if self.__orientation == 0:
            for i in range(self.__length):
                cordinates.append((x + i, y))
        elif self.__orientation == 1:
            for i in range(self.__length):
                cordinates.append((x, y + i))
        return cordinates

    def possible_moves(self):
        """
        :return: A dictionary of strings describing possible movements permitted by this car.
        """
        # For this car type, keys are from 'udrl'
        # The keys for vertical cars are 'u' and 'd'.
        # The keys for horizontal cars are 'l' and 'r'.
        # You may choose appropriate strings.
        # implement your code and erase the "pass"
        # The dictionary returned should look something like this:
        # result = {'f': "cause the car to fly and reach the Moon",
        #          'd': "cause the car to dig and reach the core of Earth",
        #          'a': "another unknown action"}
        # A car returning this dictionary supports the commands 'f','d','a'.
        # implement your code and erase the "pass"
        pos_moves = {}
        if self.__orientation == 0:
            pos_moves["u"] = "cause the car to go up"
            pos_moves["d"] = "cause the car to go down"
        elif self.__orientation == 1:
            pos_moves["r"] = "cause the car to go right"
            pos_moves["l"] = "cause the car to go left"
        return pos_moves

    def movement_requirements(self, move_key):
        """ 
        :param move_key: A string representing the key of the required move.
        :return: A list of cell locations which must be empty in order for this move to be legal.
        """
        # For example, a car in locations [(1,2),(2,2)] requires [(3,2)] to
        # be empty in order to move down (with a key 'd').
        # implement your code and erase the "pass"
        listo = []
        cordinates = self.car_coordinates()
        first_cor = cordinates[0]
        last_cor = cordinates[-1]
        first_row, first_col = first_cor
        last_row, last_col = last_cor
        if self.__orientation == 0:
            if move_key == 'u':
                listo.append((first_row - 1, first_col))
            elif move_key == 'd':
                listo.append((last_row + 1, last_col))
        elif self.__orientation == 1:
            if move_key == 'l':
                listo.append((first_row, first_col - 1))
            elif move_key == 'r':
                listo.append((last_row, last_col + 1))
        return listo



    def move(self, move_key):
        """ 
        :param move_key: A string representing the key of the required move.
        :return: True upon success, False otherwise
        """
        # implement your code and erase the "pass"
        if move_key in self.possible_moves():
            row, col = self.__location
            if move_key == 'u':
                self.__location = (row - 1, col)
            elif move_key == 'd':
                self.__location = (row + 1, col)
            elif move_key == 'l':
                self.__location = (row, col -1)
            elif move_key == 'r':
                self.__location = (row, col + 1)
            return True
        else:
            return False
    
    def get_name(self):
        """
        :return: The name of this car.
        """
        # implement your code and erase the "pass"
        return self.__name