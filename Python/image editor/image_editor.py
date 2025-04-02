#################################################################
# FILE : image_editor.py
# WRITER : yair mahfud , yairthfc , 207807082
# EXERCISE : intro2cs ex5 2022-2023
# DESCRIPTION: A simple program that edits photos for the user in different ways
# STUDENTS I DISCUSSED THE EXERCISE WITH: no one
# WEB PAGES I USED: https://www.programiz.com/python-programming/methods/built-in/isinstance
# NOTES: 
#################################################################

##############################################################################
#                                   Imports                                  #
##############################################################################
from ex5_helper import *
from typing import Optional
import copy
import sys

##############################################################################
#                                  Functions                                 #
##############################################################################

def create_lists_for_seperation(list: list) -> list:
    """creates a list with lists of lists inside of them for seperation"""
    big_list = []
    for channels in range(len(list[0][0])):
        channel_list = []
        for rows in range(len(list)):
            row_list = []
            channel_list.append(row_list)
        big_list.append(channel_list)
    return big_list

def separate_channels(image: ColoredImage) -> List[SingleChannelImage]:
    """seperates the channels in each 'pixel' into their own color channel, divided by number of rows and columns"""
    SingleChannelImage = create_lists_for_seperation(image)
    for row in range(len(image)):
        for column in range(len(image[0])):
            for channel in range(len(image[0][0])):
                number = image[row][column][channel]
                SingleChannelImage[channel][row].append(number) 
    return SingleChannelImage

def create_lists_for_combination(list: list) -> list:
    """creates list with lists in lists to reverse the seperate action"""
    big_list = []
    for channels in range(len(list[0])):
        channel_list = []
        for rows in range(len(list[0][0])):
            row_list = []
            channel_list.append(row_list)
        big_list.append(channel_list)
    return big_list

def combine_channels(channels: List[SingleChannelImage]) -> ColoredImage:
    """combine the channels from seperated lists into pixels with their respective color spots"""
    ColoredImage = create_lists_for_combination(channels)
    for row in range(len(channels[0])):
        for column in range(len(channels[0][0])):
            for channel in range(len(channels)):
                number = channels[channel][row][column]
                ColoredImage[row][column].append(number)
    return ColoredImage

def turn_channel_gray(color_list: list):
    """takes one channel and turns it into gray"""
    grey_number = (color_list[0] * 0.299) + (color_list[1] * 0.587) + (color_list[2] * 0.114)
    return round(grey_number)

def RGB2grayscale(colored_image: ColoredImage) -> SingleChannelImage:
    """takes a full colored image and turns each channel into gray"""
    SingleChannelImage = []
    for row in range(len(colored_image)):
        row_list = []
        for column in range(len(colored_image[0])):
            row_list.append(turn_channel_gray(colored_image[row][column]))
        SingleChannelImage.append(row_list)
    return SingleChannelImage
            


def blur_kernel(size: int) -> Kernel:
    """takes a rquired kernel size and creates a matrix with the value inside them"""
    Kernel = []
    for x in range(size):
        sub_list = []
        for y in range(size):
            num = 1/(size**2)
            sub_list.append(num)
        Kernel.append(sub_list)
    return Kernel

def calculate(x,y,image,size):
    """calculates one index in the original list value. gets the index numbers,the image and the kernel
    size and check along the index we use what is the sum of the values around him multiplied by the 
    value of the respective kernel index(which are all the same by definition) and returns this total"""
    total = 0
    for i in range(x-(size//2),x+(size//2)+1):
        for j in range(y-(size//2),y+(size//2)+1):
            if (0 <= i <= (len(image)-1)) and (0 <= j <= (len(image[0])-1)):
                total += (image[i][j] * (1/(size**2)))
            else :
                total += (image[x][y] * (1/(size**2)))
    if total < 0:
        return 0
    elif total > 255:
        return 255
    else :
        return round(total)


def apply_kernel(image: SingleChannelImage, kernel: Kernel) -> SingleChannelImage:
    """applys the kernel on each of the indexes of the image to get a blurred image"""
    blured_image = copy.deepcopy(image)
    size = len(kernel)
    for x in range(len(image)):
        for y in range(len(image[0])):
            blured_image[x][y] = calculate(x,y,image,size)
    return blured_image



def determine_index(y: float, x: float):
    """returns the indexes values as a tuple"""
    index = (int(y),int(x))
    return index
            
def determine_indexes_value(image: SingleChannelImage, starting_index: tuple):
    """recieves a starting index and image and calculates the close indexes surrounding him.
    returns the indexes values."""
    a = image[starting_index[0]][starting_index[1]]
    if (len(image)-1) > starting_index[0]:
        b = image[starting_index[0] + 1][starting_index[1]]
    else :
        b = image[starting_index[0]][starting_index[1]]
    if (len(image[0])-1) > starting_index[1]:
        c = image[starting_index[0]][starting_index[1] + 1]
    else :
        c = image[starting_index[0]][starting_index[1]]
    if (len(image[0])-1) > starting_index[1] and (len(image)-1) > starting_index[0]:
        d = image[starting_index[0] + 1][starting_index[1] + 1]
    else :
        d = image[starting_index[0]][starting_index[1]]
    values = [a,b,c,d]
    return values

def calculate_pos_in_mini_square(y: float, x: float):
    """determines the delta x and delta y (distances) from their floor index"""
    distance_y = y - int(y)
    distance_x = x - int(x)
    return [distance_y, distance_x]

def bilinear_interpolation(image: SingleChannelImage, y: float, x: float) -> int:
    """recives an index and image and checkes the value of the index for a new image."""
    index = determine_index(y, x)
    a,b,c,d = determine_indexes_value(image, index)
    delta_y,delta_x = calculate_pos_in_mini_square(y, x)
    new_value = (a*(1-delta_x)*(1-delta_y))+(b*delta_y*(1-delta_x))+(c*delta_x*(1-delta_y))+(d*delta_x*delta_y)
    return round(new_value)

def list_for_new_image(new_height: int, new_width: int):
    """gets new idth and height demands and creates a new matrix according to them"""
    new_list = []
    for x in range(new_height):
        row = []
        for y in range(new_width):
            y = 'e'
            row.append(y)
        new_list.append(row)
    return new_list

def fallen_cordinate(image: list, new_image: list, y: int, x: int):
    """checks the fallen cordinates from the new image onto the origin image"""
    y_relative_block = y/(len(new_image)-1)
    x_relative_block = x/(len(new_image[0])-1)
    fallen_y = (len(image)-1) * y_relative_block
    fallen_x = (len(image[0])-1) * x_relative_block
    return [fallen_y, fallen_x]

def corners_value_transfer(image: list, new_image: list):
    """transfers the corner values from the origin image to the new image"""
    new_image[0][0] = image[0][0]
    new_image[0][len(new_image[0])-1] = image[0][len(image[0])-1]
    new_image[len(new_image)-1][0] = image[len(image)-1][0]
    new_image[len(new_image)-1][len(new_image[0])-1] = image[len(image)-1][len(image[0])-1]

def resize(image: SingleChannelImage, new_height: int, new_width: int) -> SingleChannelImage:
    """takes an origin image and new image height and width paremeters and with each fallen cordinate 
    from the new image to the origin image uses the bilinear interpolation function to get the new image indexes 
    value respectivly"""
    new_image = list_for_new_image(new_height,new_width)
    corners_value_transfer(image, new_image)
    for row in range(len(new_image)):
        for column in range(len(new_image[0])):
            spot = (row,column)
            if spot == ((0,0) or (0,len(new_image[0])-1) or (len(new_image)-1,0) or (len(new_image)-1,len(new_image[0])-1)):
                pass
            else:
                y,x = fallen_cordinate(image, new_image, row, column)
                index_value = bilinear_interpolation(image, y, x)
                new_image[row][column] = index_value
    return new_image

def new_rotated_list(image):
    """creates a new rotated list for turning the photo"""
    rotated_list = []
    for row in range(len(image[0])):
        row =[]
        for column in range(len(image)):
            row.append('e')
        rotated_list.append(row)
    return rotated_list



def rotate_90(image: Image, direction: str) -> Image:
    """rotates the image according to the direction given"""
    rotated_image = new_rotated_list(image)
    if direction == 'R':
        R_list = []
        for column in range(len(image[0])):
            for row in range(len(image)-1,-1,-1):
                R_list.append(image[row][column])
        i = 0
        for x in range(len(rotated_image)):
            for y in range(len(rotated_image[0])):
                rotated_image[x][y] = R_list[i]
                i += 1
    if direction == 'L':
        L_list = []
        for column in range(len(image[0])-1,-1,-1):
            for row in range(len(image)):
                L_list.append(image[row][column])
        i = 0
        for x in range(len(rotated_image)):
            for y in range(len(rotated_image[0])):
                rotated_image[x][y] = L_list[i]
                i += 1

    return rotated_image

def determine_threshold_value(image: SingleChannelImage, block_size: int, c: float,x,y):
    """determines the threshold value for an index given using the indexes around
    him ,averaging them and determines if the average is bigger then the index. if its bigger,
    the return would be black (0) ,and if its smaller the return would be white"""
    total = 0
    for i in range(x-(block_size//2),x+(block_size//2)+1):
        for j in range(y-(block_size//2),y+(block_size//2)+1):
            if (0 <= i <= (len(image)-1)) and (0 <= j <= (len(image[0])-1)):
                total += image[i][j]
            else :
                total += image[x][y]
    total_av = (total/(block_size**2)) -c
    if total_av > image[x][y]:
        return 0
    else:
        return 255

def get_edges(image: SingleChannelImage, blur_size: int, block_size: int, c: float) -> SingleChannelImage:
    """blures the photo according to the blur size and then takes every index in the photo 
    and changes his threshold value using the function for it"""
    blurred_image = copy.deepcopy(apply_kernel(image,blur_kernel(blur_size)))
    for x in range(len(image)):
        for y in range(len(image[0])):
            blurred_image[x][y] = determine_threshold_value(image, block_size, c, x, y)
    return blurred_image


def quantize(image: SingleChannelImage, N: int) -> SingleChannelImage:
    """takes a greyscale image and for every index performs a constant calculation"""
    quantized_image = copy.deepcopy(image)
    for row in range(len(image)):
        for column in range(len(image[0])):
            quantized_image[row][column] = round((int(quantized_image[row][column] * (N/256))) * (255/(N -1)))
    return quantized_image


def quantize_colored_image(image: ColoredImage, N: int) -> ColoredImage:
    """perform the quantize on a colored image on every differnt color channel"""
    quan_colored_image = copy.deepcopy(image)
    quan_colored_image = separate_channels(quan_colored_image)
    for x in range(len(quan_colored_image)):
        quan_colored_image[x] = quantize(quan_colored_image[x],N)
    quan_colored_image = combine_channels(quan_colored_image)
    return quan_colored_image

input_list_message = "1.Change from color to grayscale\n2.Blur photo\n3.change photo size\n4.rotate\n5.Edge your photo\n6.Quantize your photo\n7.Show image\n8.Save and exit"

def get_input():
    """gets input from the user and verifies if its valid input"""
    while True:
        print(input_list_message)
        user_input = input("please enter action number: ")
        options_list = ['1','2','3','4','5','6','7','8']
        if user_input in options_list:
            return user_input
        else:
            print("please enter valid option!")

def is_image_color(image: list):
    """checks if an image is colored or grayscaled"""
    if isinstance(image[0][0], int):
        return GRAYSCALE_CODE
    else:
        return RGB_CODE

def action_1(image: list, color_value: str):
    """performs action 1 according to the color value"""
    if color_value == GRAYSCALE_CODE:
        print("image is already not colored")
    elif color_value == RGB_CODE:
        image = RGB2grayscale(image)
        color_value = GRAYSCALE_CODE
    return image

def action_2(image: list, color_value: str):
    """performs action 2 according to the color value and the user input while validating the input is correct"""
    user_input = input("please enter kernel size: ")
    if (user_input.isdigit()) and (int(user_input) > 0) and (int(user_input)%2 == 1):
        if color_value == GRAYSCALE_CODE:
            image = apply_kernel(image,blur_kernel(int(user_input)))
        elif color_value == RGB_CODE:
            image = separate_channels(image)
            for x in range(len(image)):
                image[x] = apply_kernel(image[x],blur_kernel(int(user_input)))
            image = combine_channels(image)
    else :
        print("input is not valid")
    return image

def action_3(image: list, color_value: str):
    """performs action 3 according to the color value and the user input while validating the input is correct"""
    user_input = input("please insert height and length in the form (x,y): ")
    if "," in  user_input:
        height, width = user_input.split(',')
        if (width.isdigit()) and (height.isdigit()) and (int(width) > 1) and (int(height) > 1):
            width = int(width)
            height = int(height)
            if color_value == GRAYSCALE_CODE:
                image = resize(image, height, width)
            elif color_value == RGB_CODE:
                image = separate_channels(image)
                for x in range(len(image)):
                    image[x] = resize(image[x],height,width)
                image = combine_channels(image)
        else :
            print("input is not valid")
    else :
        print("input is not valid")
    return image
        
def action_4(image: list):
    """performs action 4 according to the user input while validating the input is correct"""
    user_input = input("please insert direction (R or L): ")
    if (len(user_input) == 1) and ((('R') in user_input) or (('L') in user_input)):
        image = rotate_90(image, user_input)
    else :
        print("input is not valid")
    return image

def action_5(image: list, color_value: str):
    """performs action 5 according to the color value and the user input while validating the input is correct"""
    try:
        user_input = input("please insert blur size, block size and c: ")
        blur_size, block_size, c = user_input.split(',')
        if (blur_size.isdigit()) and ((int(blur_size))%2 == 1) and (block_size.isdigit()) and ((int(block_size))%2 == 1):
            if (isinstance(float(c),float)) and (float(c) > 0):
                blur_size = int(blur_size)
                block_size = int(block_size)
                c = float(c)
                if color_value == GRAYSCALE_CODE:
                    image = get_edges(image, blur_size, block_size, c)
                elif color_value == RGB_CODE:
                    image = RGB2grayscale(image)
                    image = get_edges(image, blur_size, block_size, c)
            else:
                print("input is not valid")
        else:
            print("input is not valid")
    except:
        print("input is not valid")
    return image

def action_6(image: list, color_value: str):
    """performs action 6 according to the color value and the user input while validating the input is correct"""
    user_input = input("please enter quantize number: ")
    if (len(user_input) == 1) and (user_input.isdigit()):
        if color_value == GRAYSCALE_CODE:
            image = quantize(image, int(user_input))
        elif color_value == RGB_CODE:
            image = quantize_colored_image(image, int(user_input))
    else:
        print("input is not valid")
    return image

def action_7(image: list):
    """shows image"""
    show_image(image)

def action_8(image: list):
    """saves image according to the user input of name and route"""
    user_input_file_name = input("please choose file name")
    user_input = input("please enter location route to save picture: ")
    save_image(image,user_input_file_name)

if __name__ == '__main__':
    args = sys.argv
    img = copy.deepcopy(load_image(args[1]))
    color_value = is_image_color(img)
    if len(args) == 2:
        while True:
            option = get_input()
            if option == '1':
                img = action_1(img, color_value)
                color_value = GRAYSCALE_CODE
            elif option == '2':
                img = action_2(img, color_value)
            elif option == '3':
                img = action_3(img, color_value)
            elif option == '4':
                img = action_4(img)
            elif option == '5':
                img = action_5(img, color_value)
                color_value = GRAYSCALE_CODE
            elif option == '6':
                img = action_6(img, color_value)
            elif option == '7':
                action_7(img)
            elif option == '8':
                action_8(img)
                break


