from Base import InterestRateModels
from ZCB import ZCB
import numpy as np

class Hull_White(InterestRateModels):
    def __init__(self, lamda, eta, x, y):
        self._lamda = lamda
        self._eta = eta
        self._x = x
        self._y = y
        self._P0T = ZCB(self._x, self._y)
    
    def f0T(self):
        dt = 0.0001 # Define difference between time levels
        return lambda t : - np.log(ZCB.Bond_Value(t + dt) - ZCB.Bond_Value(t - dt)) / (2 * dt)
    
    def HW_theta(self):
        theta = lambda t : (1 / self._lamda) * self.f0T(t) + self.f0T(t) + \
            self._eta / (2 * np.power(self._lamda, 2)) * (1.0-np.exp(-2.0*self._lamda*t))
        return theta
    
    
    def HW_B(self, T1, T2):
        B = - (1 / self._lamda) * (1 - np.exp(- self._lamda * (T2 - T1)))
        return B
    
    
    def HW_A():
        pass
    

    
    def HW_ZCB():
        pass
    