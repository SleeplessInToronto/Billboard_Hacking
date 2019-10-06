import numpy as np
from numpy.linalg import inv

def bilinear_interp(I, pt):
    """
    Performs bilinear interpolation for a given image point.

    Given the (x, y) location of a point in an input image, use the surrounding
    4 pixels to conmpute the bilinearly-interpolated output pixel intensity.

    Note that images are (usually) integer-valued functions (in 2D), therefore
    the intensity value you return must be an integer (use round()).

    This function is for a *single* image band only - for RGB images, you will 
    need to call the function once for each colour channel.

    Parameters:
    -----------
    I   - Single-band (greyscale) intensity image, 8-bit np.array (i.e., uint8).
    pt  - 2x1 np.array of point in input image (x, y), with subpixel precision.

    Returns:
    --------
    b  - Interpolated brightness or intensity value (whole number >= 0).
    """
    #--- FILL ME IN ---

    if pt.shape != (2, 1):
        raise ValueError('Point size is incorrect.')
    
    #Get the x and y value from the point
    x = pt[0,0]
    y = pt[1,0]
    #define the x_vector
    x_vec = np.array([[1],[x],[y],[x*y]])
    #define the lower and upper bounds of x and y
    x_low = np.ceil(x).astype(int)  - 1
    x_up = np.floor(x).astype(int)  + 1
    y_low = np.ceil(y).astype(int)  - 1
    y_up = np.floor(y).astype(int)  + 1
    

    #x is across columns of the image, y is across rows, also clip to get the nearest pixel (np)
    x_low_np = np.clip( x_low ,0, I.shape[1] - 1)
    x_up_np  = np.clip( x_up  ,0, I.shape[1] - 1) 
    y_low_np = np.clip( y_low ,0, I.shape[0] - 1) 
    y_up_np  = np.clip( y_up  ,0, I.shape[0] - 1) 
    
    #get the values for the 4 nearest points from the Image
    left_down  = I[y_low_np,x_low_np]
    right_down = I[y_low_np,x_up_np ]
    left_up    = I[y_up_np ,x_low_np]
    right_up   = I[y_up_np ,x_up_np ]
    
    #get the B coefficients
    b_coefs = inv(np.array([
                        [1,x_low, y_low, x_low * y_low],
                        [1,x_low, y_up , x_low * y_up ],
                        [1,x_up , y_low, x_up  * y_low],
                        [1,x_up , y_up , x_up  * y_up ]
                    ])).T.dot(x_vec)
    #calculate the value of b and round, make sure it is >= 0
    b =  np.max(np.round(b_coefs.T.dot(np.array([[left_down], [left_up], [right_down], [right_up]]))), 0)[0]
    #------------------

    return b
