from .Base import InterestRateModels
from .Interpolator import Interpolator
import numpy as np


class ZCB(InterestRateModels):
    def __init__(self, x, y):
        self._x = x
        self._y =y
        self._interpolator = Interpolator(self._x, self._y)
        self._zcb_values = None
        
    def Bond_Value(self, t):
        """Calculate ZCB values for all time points in self._x"""
    
    # Compute discount factors for given time points
        self._zcb_values = np.exp(-self._interpolator.interpolation(t) * t)
        return self._zcb_values

    
    
    def ZCB_Values(self):
        """Return the calculated ZCB values (if already calculated)"""
        if self._zcb_values is None:
            # If the ZCB values haven't been calculated yet, calculate them first
            self.Bond_Value()
        return self._zcb_values
    
    

