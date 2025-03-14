from abc import ABC, abstractmethod

class InterestRateProduct(ABC):
    @abstractmethod
    def product_value(self):
        pass