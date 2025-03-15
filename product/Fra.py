from abc import abstractmethod
from product.InterestRateProduct import InterestRateProduct

class Fra(InterestRateProduct):
    @abstractmethod
    def product_value(self):
        pass
    

class Fra_Analytical(Fra):
    def __init__(self, T1, T2, K, N, P0T, x, y):
        self._T1 = T1
        self._T2 = T2
        self._K = K
        self._N = N
        self._zcb = P0T(x, y)
        self._P0T = self._zcb.Bond_Value
        #self._x = x
        #self._y = y
        
    
class PayerFra_Analytical(Fra_Analytical):
    def product_value(self):
        tau = self._T2 - self._T1
        temp1 = self._P0T(self._T2) * (1 + tau * self._K)
        temp2 = self._P0T(self._T1)
        return self._N * (temp2 - temp1)
        

class ReceiverFra_Analytical(Fra_Analytical):
    def product_value(self):
        tau = self._T2 - self._T1
        temp1 = self._P0T(self._T2) * (1 + tau * self._K)
        temp2 = self._P0T(self._T1)
        return self._N * (temp1 - temp2)
              