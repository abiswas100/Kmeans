import os
from pathlib import Path

import csv
import json
import cv2
from skimage import draw
import numpy as np
import re
not_working = []
'''
Functions used for different calculations on the objects. 
1. Calcualting all coordinates within a polygon given the edge coordinates
2. Calculate v_values from the generated coordinates
3. Calculating the mean of all u_values calculated within an object (polygon)
'''
def polygon_area_calculation(x_inputs, y_inputs):
    '''
    Function generate a list of all coordinates that are found within the polygon object.
    Generates a list of x and y coordinates of the same length (they are pairs). In order to
    access the coordinates, step through each list (x_coordiantes, y_coordinates) at the same rate
    ie. one for loop with len(x_coordinates)
    :param x_inputs: list of x coordinates from the annotated json file
    :param y_inputs: list of y coordinates from the annotated json file
    :return: x_coordinates, y_coordinates which hold the x and y, respectively, coordinates of the polygon.
    '''
    r = np.array(x_inputs)
    c = np.array(y_inputs)
    x_coordinates, y_coordinates = draw.polygon(r, c)
    return x_coordinates, y_coordinates


# image_list = []
def start_parsing(image_list,filenames): #json_files , project_name
    #changing into the json directory in data folder

    temp_images,new_coords = [],[]

    path = os.getcwd()
    parent_path = Path(path).parent
    os.chdir(parent_path)    
    os.chdir('json')

    for i in range(len(image_list)):

        choice = int("Enter the object 1. Windows 2. Facade 3.Roof")
        filename = filenames[i]

        if choice  == 1: classtitle,classtitle1 = 'Windows','Window'
        elif choice == 2 : classtitle,classtitle1 = 'Facades','Facades'
        elif choice == 3 : classtitle,classtitle1 = 'Roofs','Roof' 

        x_coordinates, y_coordinates = [0],[0]
        img = image_list[i]
        json_filename = filename[:-4] + '.jpg.json'  

        with open(json_filename) as json_content:
                json_data = json.load(json_content)

                for entry in json_data['objects']:
                    if (entry['classTitle'] == classtitle or entry['classTitle'] == classtitle1):
                        
                        x_values = []
                        y_values = []
                        points = entry['points']
                        exterior = points['exterior']

                        for k, coordinates in enumerate(exterior):
                            x_values.append(exterior[k][0])
                            y_values.append(exterior[k][1])
                        if (len(x_values) < 4):
                            print("ERROR: LESS THAN 4 POINTS ANNOTATED FOR WINDOW. NUMBER OF POINTS: {}".format(len(x_values)),filename)
                            x_coordinates, y_coordinates = 0,0
                        else:
                            x_coordinates, y_coordinates = polygon_area_calculation(x_values, y_values)
        
                            new_coord = []      
                            for i in range(len(x_coordinates)):
                                    x = x_coordinates[i].item()
                                    y = y_coordinates[i].item()
                                    new_coord.append([x,y])
                            new_coords.append(new_coord)       # apppending new_coord of 1 image to new_coords of all images        
                                
                            #print("x: {} y: {} z: {}".format(x_coordinates[0], y_coordinates[1], len(new_coord)))        
                            # except UnboundLocalError: print(filename)

                            try:    
                                temp_image = []        
                                for j in new_coord:
                                    r ,g,b = img[j[1],j[0]]
                                    temp_image.append(list([r,g,b]))    

                            except UnboundLocalError : 
                                print("Annotation not working",filename)
                                print("")
                            temp_images.append(temp_image)    # apppending temp_image of 1 image to temp_images of all images
                    else:
                        image_list = image_list.remobe(img)
                        filenames = filename.remove(filename)

    return temp_images, new_coords,image_list,filenames
     

