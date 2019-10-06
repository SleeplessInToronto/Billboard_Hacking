import numpy as np

def histogram_eq(I):
    """
    Histogram equalization for greyscale image.

    Perform histogram equalization on the 8-bit greyscale intensity image I
    to produce a contrast-enhanced image J. Full details of the algorithm are
    provided in the Szeliski text.

    Parameters:
    -----------
    I  - Single-band (greyscale) intensity image, 8-bit np.array (i.e., uint8).

    Returns:
    --------
    J  - Contrast-enhanced greyscale intensity image, 8-bit np.array (i.e., uint8).
    """
    #--- FILL ME IN ---

    # Verify I is grayscale.
    if I.dtype != np.uint8:
        raise ValueError('Incorrect image format!')
    
    #store the shape for later reshape step
    shape = I.shape
    #make the image flat for easier computation
    flat = I.flatten() 
    
    #define L-1 (up range) and low range for equalization
    scale_up = 255
    scale_low = 0
    #define the bin counts as the intensity values of the desired image
    bin_count = scale_up - scale_low

    #get the histogram and the bins
    hist, bins = np.histogram(flat, bins=bin_count, range = (scale_low,scale_up))
    #get the probability density function for each bin
    pdf = hist / (np.sum(hist))
    #get the cumulative distribution function
    cdf = np.cumsum(pdf)
    #calculate the transfer value
    c_i = np.round((cdf) * (scale_up - scale_low)).astype('uint8')
        
    #find the mapping of each intensity in the original image to the bins
    mapping = np.fmin(np.digitize(flat, bins), bin_count) 
    #assign the new intesities to each bin
    new_img = np.array([ c_i[k - 1]  for k in mapping])
    #reshape the image
    J = new_img.reshape(shape)
    
    #------------------

    return J