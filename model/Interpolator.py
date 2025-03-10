from Base import InterestRateModels
from scipy.interpolate import CubicSpline
import matplotlib.pyplot  as plt
import numpy as np

class Interpolator(InterestRateModels):
    """Initialize with data points and compute cubic spline."""
    def __init__(self, x, y):
        self._x = x
        self._y = y
        self._spline = CubicSpline(self._x, self._y, bc_type="natural") 
    
    
    def interpolation(self, xi):
        return self._spline(xi)
    
    def plot_result(self):
        """Plot the spline interpolation with original data points."""
        Plotter.plot(self._x, self._y, self.interpolation) 



class Plotter:
    @staticmethod
    def plot(x, y, interpolation_func):
        xi = np.linspace(min(x), max(x), 100)
        yi = interpolation_func(xi)
        
        plt.plot(x, y, 'o', label="Data Points")
        plt.plot(xi, yi, label="Interpolation Curve")
        plt.legend()
        plt.show()
        
        




        
        