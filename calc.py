import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import CubicSpline
factor_of_error = 1

def spline_interpolation(x, y, num_points):
    """
    Performs cubic spline interpolation on the given x and y coordinates, 
    and returns an array of interpolated x and y coordinates for plotting.
    
    :param x: A list or numpy array of x-coordinates of the gravity anchor nodes
    :param y: A list or numpy array of y-coordinates of the gravity anchor nodes
    :param num_points: The number of points to interpolate between each pair of anchor nodes (default: 100)
    :return: A tuple of two numpy arrays representing the interpolated x and y coordinates
    """
    # Create a cubic spline object using the given x and y coordinates
    cs = CubicSpline(x, y)
    
    # Generate an array of num_points equally spaced x-coordinates between the minimum and maximum x-values
    x_interp = np.linspace(np.min(x), np.max(x), num=num_points)
    
    # Evaluate the cubic spline at the interpolated x-coordinates to get the corresponding y-coordinates
    y_interp = cs(x_interp)
    
    return x_interp, y_interp

def calcQ(T_in,T_out,Wind_vel):  #(F,F,MPH)
    T_in = (T_in-32)*5/9
    T_out = (T_out-32)*5/9
    A = 1345.7 #m^2
    D = 23.16  #meters

    h_out = 2+2*Wind_vel/7.5 #btu/hour/sqfoot/0F 
    h_out /= 3.41 # W/(ft^2*F)
    h_out *= 10.7639 # W/(m^2*F)
    h_out *= (9/5) # W/(m^2*K)
    R_convout = 1/(h_out) # degK/W
   
    h_in = 3 # BTU/(ft^2*hr*F)
    h_in /= 3.41 # W/(ft^2*F)
    h_in *= 10.7639 # W/(m^2*F)
    h_in *= (9/5) # W/(m^2*K)
    R_convin = 1/(h_in) # degK/W
    
    R_cond = 0.1 # ft^2*hr*F/BTU # Given by Saint-Gobain stats
    R_cond /= 10.7639 # m^2*hr*F/BTU
    R_cond *= 3.41 # m^2*F/W
    R_cond *= (5/9) # m^2*K/W

    return A*(T_in-T_out)/((R_cond+R_convout+R_convin)*1000*factor_of_error) #KiloWatts

def midpoint_riemann_sum(x, y):
    """
    Computes the positive accumulation of data using the midpoint Riemann sum method.
    
    Parameters:
    x (array): The x-values of the data points
    y (array): The y-values of the data points
    
    Returns:
    float: The positive accumulation of the data
    """
    n = len(x)
    dx = (x[-1] - x[0]) / (n - 1)
    area = 0
    for i in range(n - 1):
        x_mid = (x[i] + x[i+1]) / 2
        y_mid = (y[i] + y[i+1]) / 2
        if y_mid > 0:
            area += y_mid * dx
    return area
