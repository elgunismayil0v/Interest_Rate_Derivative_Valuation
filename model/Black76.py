from model.Base import InterestRateModels
import numpy as np

class Black76(InterestRateModels):
    def __init__(self, T, tau, K, sigma, P0T, x, y):
        self._T = T
        self._tau = tau
        self._K = K
        self._sigma = sigma
        self._zcb = P0T(x ,y)
        self._P0T = self._zcb.Bond_Value
        
    def Forward_Rate(self):
        temp1 = 1 / self._tau
        temp2 = self._P0T(self._T) / self._P0T(self._T + self._tau) - 1
        return temp1 * temp2
    
    def d1(self):
        temp1 = np.log(self.Forward_Rate() / self._K) + 0.5 * np.power(self._sigma, 2) * self._T
        temp2 = self._sigma * np.sqrt(self._T)
        return temp1 / temp2
    
    def d2(self):
        return self.d1() - self._sigma * np.sqrt(self._T)
    
    def Discount_Factor(self):
        return self._P0T(self._T + self._tau)
        
        
        