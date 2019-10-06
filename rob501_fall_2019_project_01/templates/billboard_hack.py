#test
# import os
# os.chdir(r'C:\Users\Shahin\Documents\School\Skule\Year 4\Fall\ROB501\Assignment1\rob501_fall_2019_project_01\templates')
# import matplotlib.pyplot as plt


# Billboard hack script file.
import numpy as np
from matplotlib.path import Path
from imageio import imread, imwrite

from dlt_homography import dlt_homography
from bilinear_interp import bilinear_interp
from histogram_eq import histogram_eq

def billboard_hack():
    """
    Hack and replace the billboard!

    Parameters:
    ----------- 

    Returns:
    --------
    Ihack  - Hacked RGB intensity image, 8-bit np.array (i.e., uint8).
    """
    # Bounding box in Y & D Square image.
    bbox = np.array([[404, 490, 404, 490], [38,  38, 354, 354]])

    # Point correspondences.
    Iyd_pts = np.array([[416, 485, 488, 410], [40,  61, 353, 349]])
    Ist_pts = np.array([[2, 218, 218, 2], [2, 2, 409, 409]])

    Iyd = imread('../billboard/yonge_dundas_square.jpg')
    Ist = imread('../billboard/uoft_soldiers_tower_dark.png')

    Ihack = np.asarray(Iyd)
    Ist = np.asarray(Ist)

    #--- FILL ME IN ---

    # Let's do the histogram equalization first.
    st_equalized = histogram_eq(Ist)
    
    # Compute the perspective homography we need...
    H,A = dlt_homography(Iyd_pts,Ist_pts)

    # Main 'for' loop to do the warp and insertion 
    
    #define the polygon of the billboard
    billboard_polygon = Path(Iyd_pts.T)
    #loop through the bounding box
    for x in     range(np.min(bbox.T[:,0]) ,np.max(bbox.T[:,0]) ):
        for y in range(np.min(bbox.T[:,1]) ,np.max(bbox.T[:,1]) ):
            #check if the point in the bounding box is within the polygon
            if(billboard_polygon.contains_point(np.array([x,y]).T) == False):
                continue
            #define the homogenous point of the billboard
            homogenous_point = np.array([[x,y,1.0]]).T
            #get the corresponding point in the soldiers tower
            correspondence = H.dot(homogenous_point)
            #normalize the correspondence point by w
            correspondence = correspondence / correspondence[2,0]
            #bilinearly interpolate the soldiers tower
            interpolated = bilinear_interp(st_equalized,correspondence[:-1,0:])
            #set the intensity of the yd picture to st
            Ihack[y, x] = np.array([interpolated, interpolated, interpolated])                
                
    return Ihack
    
billboard_hack()