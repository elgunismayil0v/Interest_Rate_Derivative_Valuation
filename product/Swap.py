from abc import abstractmethod
from model.ZCB import ZCB
from product.InterestRateProduct import InterestRateProduct
import numpy as np
from enum import Enum

class Swap(InterestRateProduct):
    @abstractmethod
    def product_value(self):
        pass
    
    


class Swap_Analytical(Swap):
    def __init__(self, T1, T2, t, K, N, NoOfPay, P0T, x, y):
        self._T1 = T1
        self._T2 = T2
        self._t = t
        self._K = K
        self._N = N
        self._NoOfPayment = NoOfPay
        self._zcb = P0T(x,y) 
        self._P0T = self._zcb.Bond_Value
        
    
    def time_interval(self):
        time_grid = np.linspace(self._T1, self._T2, self._NoOfPayment)
        return time_grid[time_grid > self._t]
    
    def discount_factor(self):
        temp = 0.0
        time_grid = self.time_interval()
        tau = time_grid[1] - time_grid[0]
        for grid in time_grid:
            temp += self._P0T(grid) * tau
            
        return temp
    
    def product_value(self):
        pass
        
class PayerSwap(Swap_Analytical):
    def product_value(self):
        return self._N * (self._P0T(self._T1) - self._P0T(self._T2) - self._K * self.discount_factor())
    
class ReceiverSwap(Swap_Analytical):
    
    def product_value(self):
        return self._N * (self._K * self.discount_factor() - self._P0T(self._T1) + self._P0T(self._T2)) 
    
            
