import numpy as np
from numpy.linalg import inv, norm
from scipy.linalg import null_space

def dlt_homography(I1pts, I2pts):
    """
    Find perspective Homography between two images.

    Given 4 points from 2 separate images, compute the perspective homography
    (warp) between these points using the DLT algorithm.

    Parameters:
    ----------- 
    I1pts  - 2x4 np.array of points from Image 1 (each column is x, y).
    I2pts  - 2x4 np.array of points from Image 2 (in 1-to-1 correspondence).

    Returns:
    --------
    H  - 3x3 np.array of perspective homography (matrix map) between image coordinates.
    A  - 8x9 np.array of DLT matrix used to determine homography.
    """
    #--- FILL ME IN ---
    #initialize the A matrix with zeros
    A = np.zeros([8,9])
    #loop through every point in source and create the A matrix, 2 row by 2 row
    for i,point in enumerate(I1pts.T):
        x = point[0]
        y = point[1]
        #get the corresponce point from the input destinations points
        correspondence = I2pts.T[i]
        u = correspondence[0]
        v = correspondence[1]
        #construct the A matrix use the formula in the paper
        A_i = np.array([ [-1*x, -1*y, -1,   0 ,   0 ,  0, u*x, u*y, u],
                         [0   ,    0,  0, -1*x, -1*y, -1, v*x, v*y, v],
                        ])
        #add these 2 rows to the resultant A matrix (the one we initialize at the beginning)
        A[i*2 : (i+1)*2,:] = A_i
    
    #calculate the H matrix using null space
    H = null_space(A)
    #reshape the H matrix
    H = H.reshape(3,3)
    #get the last entry and normalize
    last_entry = H[2][2]
    #normalize
    H = H * (1.0/last_entry)

    
    #------------------

    return H, A