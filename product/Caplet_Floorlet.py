from abc import abstractmethod
from scipy.stats import norm
from product.InterestRateProduct import InterestRateProduct
from model.Black76 import Black76

class Caplet(InterestRateProduct):
    @abstractmethod
    def product_value(self):
        pass

class Floorlet(InterestRateProduct):
    @abstractmethod
    def product_value(self):
        pass
    
class Caplet_Black76(Caplet):
    def __init__(self, N, tau, K, P0T, sigma, T, x, y):
        self._N = N
        self._T = T
        self._tau = tau
        self._K = K
        self._sigma = sigma
        self._Black76 = Black76(T, tau, K, sigma, P0T, x, y)
        
    def product_value(self):
        temp1 = self._N * self._tau * self._Black76.Discount_Factor()
        temp2 = self._Black76.Forward_Rate() * norm.cdf(self._Black76.d1()) - self._K * norm.cdf(self._Black76.d2())
        return temp1 * temp2
    

class Floorlet_Black76(Floorlet):
    def __init__(self, N, tau, K, P0T, sigma, T, x, y):
        self._N = N
        self._T = T
        self._tau = tau
        self._K = K
        self._sigma = sigma
        self._Black76 = Black76(T, tau, K, sigma, P0T, x, y)
        
    def product_value(self):
        temp1 = self._N * self._tau * self._Black76.Discount_Factor()
        temp2 = self._K * norm.cdf(-self._Black76.d2()) - self._Black76.Forward_Rate() * norm.cdf(-self._Black76.d1())
        return  temp1 * temp2   