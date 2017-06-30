"Data Science Assignment"

__author__ = 'Kirill Efimov, Larisa Adamyan'

import os
import numpy as np
from scipy.misc import imread, imsave

def map_wavelength_to_rgb(l):
    """ Maps a wavelength of visible range of spectrum to its equivalent RGB values.
    https://stackoverflow.com/questions/3407942/rgb-values-of-visible-spectrum
     
     Args:
         l (float): wave length. 
    
    Returns:
        r (float), g (float), b (float): RGB color values in [0,1].

    """
    r,g,b = 0,0,0
    if ((l>=400.0) and (l<410.0)):
        t=(l-400.0)/(410.0-400.0)
        r=  +(0.33*t)-(0.20*t*t)
    elif ((l>=410.0) and (l<475.0)):
        t=(l-410.0)/(475.0-410.0)
        r=0.14         -(0.13*t*t)
    elif ((l>=545.0) and (l<595.0)):
        t=(l-545.0)/(595.0-545.0)
        r=    +(1.98*t)-(     t*t)
    elif ((l>=595.0) and (l<650.0)):
        t=(l-595.0)/(650.0-595.0)
        r=0.98+(0.06*t)-(0.40*t*t)
    elif ((l>=650.0) and (l<700.0)):
        t=(l-650.0)/(700.0-650.0)
        r=0.65-(0.84*t)+(0.20*t*t)
    
    if ((l>=415.0) and (l<475.0)):
        t=(l-415.0)/(475.0-415.0)
        g=             +(0.80*t*t)
    elif ((l>=475.0) and (l<590.0)):
        t=(l-475.0)/(590.0-475.0)
        g=0.8 +(0.76*t)-(0.80*t*t)
    elif ((l>=585.0) and (l<639.0)):
        t=(l-585.0)/(639.0-585.0)
        g=0.84-(0.84*t)           
    
    if ((l>=400.0) and (l<475.0)):
        t=(l-400.0)/(475.0-400.0)
        b=    +(2.20*t)-(1.50*t*t)
    elif ((l>=475.0) and (l<560.0)):
        t=(l-475.0)/(560.0-475.0)
        b=0.7 -(     t)+(0.30*t*t)
    return r,g,b

def get_color_curves(wavelengths):
    """ For each wavelength computes its RGB color values."""
    net_size = len(wavelengths)
    r_curve = np.zeros(net_size)
    g_curve = np.zeros(net_size)
    b_curve = np.zeros(net_size)
    for i, wavelength_i in enumerate(wavelengths):
        r_curve[i], g_curve[i], b_curve[i] = map_wavelength_to_rgb(wavelength_i)
        
    r_curve /= np.sum(r_curve[:-1])
    g_curve /= np.sum(g_curve[:-1])
    b_curve /= np.sum(b_curve[:-1])
    return r_curve, g_curve, b_curve
        
def load_image_data(dir_path, size):
    """ Loads image files from the data directory and stores them into array."""
    X = np.zeros((size, 512,512))
    for i, file_i in enumerate(os.listdir(dir_path)):
        if file_i.endswith(".png"):
            print file_i
            X[i, :, :] = imread(dir_path + '/' + file_i)
    X /= 2 ** 16 - 1
    return X

def compose_rgb_image(data_dir, size, net_size=None):
    """ Combines 8bit png multispectral images into RGB colored image 
    and saves the resulted image as answer.png file in the working directory.
    
    Args:
        data_dir (str): Input data directory containing only multispectral images.
        size (int): Number of images in the ``data_dir``.
        net_size (int, optional): Number of points for integral evaluation. Defaults to None.
        If not specified, it is assigned to 10 * size.  
      
    """
    if net_size is None:
        net_size = 10 * size
    
    data_path =  os.path.dirname(os.path.realpath(__file__)) + '/' + data_dir
    # minimum visible wavelength
    min_nm = 400
    # maximum visible wavelength
    max_nm = 700
    # X of shape (size, 512, 512) contains the measured spectral power for given wavelengths 
    # with values in [0,1]
    X = load_image_data(data_path, size)
    # net for integral evaluation
    data_net = np.linspace(min_nm, max_nm, size)
    # wavelengths on the net
    wavelengths = np.linspace(min_nm, max_nm, net_size)
    #color curves on the net
    r_curve, g_curve, b_curve = get_color_curves(wavelengths)
    # Y - spectral power distribution
    Y = np.zeros((net_size, 512, 512))
    # spectral power value of the wavelengths is approximated linearly by two closest
    # points from the given 31 wave lengths.
    # Kernel methods can be applied as well but the result is acceptable.
    k = 0
    for i, wavelength_i in enumerate(wavelengths):
        if i == 0:
            Y[i,:, :] = X[0, :, :]
            continue
        if wavelength_i >= data_net[k+1]:
            Y[i,:, :] = X[k + 1, :, :]
            k = k+1
            continue
        Y[i,:, :] = X[k, :, :] + (X[k + 1, :, :] - X[k, :, :]) * ((wavelength_i - data_net[k]) / (data_net[k+1] - data_net[k]))
        
    d_wavelength = (max_nm - min_nm) * 1. / net_size
    
    # convolution
    Y_r = np.einsum('ijk, i', Y[:-1, :, :], r_curve[:-1])
    Y_g = np.einsum('ijk, i', Y[:-1, :, :], g_curve[:-1])
    Y_b = np.einsum('ijk, i', Y[:-1, :, :], b_curve[:-1])
    
    # final matrix of shape (512,512,3)  with rgb values for each pixel
    answer_matrix = np.concatenate((Y_r[:, :,  np.newaxis], Y_g[:, :, np.newaxis], Y_b[:, :, np.newaxis]), axis=2)
    answer_matrix = answer_matrix * 255 / d_wavelength
    imsave(os.path.dirname(os.path.realpath(__file__)) + '/answer.png', answer_matrix)
    return 0


if __name__=="__main__":
    compose_rgb_image('multispectral_images', 31)
