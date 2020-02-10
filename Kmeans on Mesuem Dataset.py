#!/usr/bin/env python
# coding: utf-8
import cv2
import numpy as np
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
import os
import time

#Storing the images from File to an array named image_list
image_list = []
filename = []
for files in os.listdir():
    if(files.endswith('.jpg')):
        img = cv2.imread(str(files))
        image_list.append(img)
        filename.append(files)

#to see an image 
#plt.imshow(cv2.cvtColor(image_list[1], cv2.COLOR_BGR2RGB))

# # Running 6 clusters on each image of Museum 

start = time.time()
clustered_images_list = []
for image in image_list:
    # reshape the image to a 2D array of pixels and 3 color values (RGB)
    pixel_values = image.reshape((-1, 3))
    # convert to float for kmeans to understand
    pixel_values = np.float32(pixel_values)
    #Criteria for Stopping the clustering
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 100, 0.01)
    #KMEANS 
    clusters = 6
    compactness, labels, centers = cv2.kmeans(pixel_values, clusters, None,criteria, 10, cv2.KMEANS_PP_CENTERS)
    # convert back to 8 bit values
    centers = np.uint8(centers)
    # flatten the labels array
    labels = labels.flatten()
    #Reconstructing the Clustered Image
    segmented_image = centers[labels]
    segmented_image = segmented_image.reshape(image.shape)
    clustered_images_list.append(segmented_image)
# In[11]:
end = time.time()
print("Time consumed in working: ",end - start)

# # saving the clustered images in a folder
os.chdir('C:\\Users\\niroop.sugunaraj\\Documents\\Avhishek\\HeatLossProject\\ds\\img\\kmeans-output')
counter = 0
for img in clustered_images_list:
    # show the image
    #plt.imshow(cv2.cvtColor(segmented_image, cv2.COLOR_BGR2RGB))
    #cv2.imwrite(str(counter) + '.jpg', img)
    cv2.imwrite(filename[counter], img)
    counter = counter + 1

