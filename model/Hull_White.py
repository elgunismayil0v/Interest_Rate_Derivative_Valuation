from .Base import InterestRateModels
import numpy as np

class HullWhiteBase(InterestRateModels):
    def __init__(self, lamda, eta, P0T):
        self._lamda = lamda
        self._eta = eta
        self._P0T = P0T


    def f0T(self, t):
        """Instantaneous forward rate using finite difference approximation."""
        dt = 0.0001 # Define difference between time levels
        
        # Ensure _P0T is used correctly as a callable function
        bond_value_function = self._P0T.Bond_Value()  # Get the callable ZCB function

        return - (np.log(bond_value_function(t + dt)) - np.log(bond_value_function(t - dt))) / (2 * dt)

        #return - (np.log(self._P0T(t + dt)) - np.log(self._P0T(t - dt))) / (2 * dt)

    def HW_theta(self, t):
        theta = (1 / self._lamda) * self.f0T(t) + self.f0T(t) + \
            self._eta * self._eta / (2 * np.power(self._lamda, 2)) * (1.0-np.exp(-2.0*self._lamda*t))
        return theta

class HullWhiteBondPricing(HullWhiteBase):
    def __init__(self, lamda, eta, P0T, T1, T2):
        super().__init__(lamda, eta, P0T)
        self._T1 = T1
        self._T2 = T2

    def HW_B(self):
        """Computes the B function in the Hull-White model."""
        return (1 / self._lamda) * (1 - np.exp(-self._lamda * (self._T2 - self._T1)))

    def HW_A(self):
        """Computes the A function in the Hull-White model."""
        tau = self._T2 - self._T1
        zGrid = np.linspace(0.0, tau, 250)
        B_r = lambda tau: (1.0 / self._lamda) * (np.exp(-self._lamda * tau) - 1.0)
        
        temp1 = (self._eta ** 2 / (4 * self._lamda ** 3)) * (
        np.exp(-2 * self._lamda * tau) * (4 * np.exp(self._lamda * tau) - 1) - 3) + \
        (self._eta ** 2 * tau / (2 * self._lamda ** 2))



        temp2 = self._lamda * np.trapz(self.HW_theta(self._T2 - zGrid) * B_r(zGrid), zGrid)
        return temp1 + temp2

    def HW_ZCB(self, r_Ti):
        """Zero-Coupon Bond pricing using Hull-White model."""
        return np.exp(self.HW_A() + self.HW_B() * r_Ti)

class HullWhiteStatistics(HullWhiteBase):
    def __init__(self, lamda, eta, P0T, T1):
        super().__init__(lamda, eta, P0T)
        self._T1 = T1

    def HW_R_0(self):
        """Initial short rate."""
        return self.f0T(0.001)

    def HW_Mean_Forward_Measure(self):
        """Mean of short rate under the forward measure."""
        zGrid = np.linspace(0.0, self._T1, 500)
        theta_hat = lambda t, T: self.HW_theta(t) + (self._eta ** 2 / self._lamda) * \
                                 (1.0 / self._lamda) * (np.exp(-self._lamda * (T - t)) - 1.0)
        temp = lambda z: theta_hat(z, self._T1) * np.exp(-self._lamda * (self._T1 - z))
        
        r_mean = self.HW_R_0() * np.exp(-self._lamda * self._T1) + self._lamda * np.trapz(temp(zGrid), zGrid)
        return r_mean

    def HW_Var_Forward_Measure(self):
        """Variance of short rate under the forward measure."""
        return (self._eta ** 2 / (2 * self._lamda)) * (1 - np.exp(-2 * self._lamda * self._T1))

    
    