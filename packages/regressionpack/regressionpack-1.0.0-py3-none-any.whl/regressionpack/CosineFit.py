import numpy as np
from typing import Tuple
from .GenericCurveFit import GenericCurveFit
from .utilities import FFTGuess
from nptyping import NDArray

class CosineFit(GenericCurveFit):
    
    def FitFunc(self, x:NDArray, amp:float, omega:float, phi:float, voff:float) -> NDArray:
        """
        A cosine function containing:
            amplitude (amp)
            frequency (omega)
            phase shift (phi)
            vertical offset (voff)
        """
        return amp * np.cos(omega * x + phi) + voff

    def Jacobian(self, x:NDArray, amp:float, omega:float, phi:float, voff:float) -> NDArray:
        """
        The jacobian of the cosine fit function. 
        Meant to return a matrix of shape [x.shape[0], 4], where
        every column contains the derivative of the function with 
        respect to the fit parameters in order. 
        """
        out = np.zeros((x.shape[0],4))
        out[:,0] = np.cos(omega*x + phi) # df/d(amp)
        out[:,1] = -amp*x*np.sin(omega*x + phi) # df/d(omega)
        out[:,2] = -amp*np.sin(omega*x + phi) # df/d(phi)
        out[:,3] = np.ones(x.shape) # df/d(voff)

        return out

    def __init__(self, x:NDArray, y:NDArray, p0:NDArray=None, bounds=(-np.inf, np.inf), confidenceInterval:float=0.95, simult:bool=False, **kwargs):

        if p0 is None:
            # Uses the fft to guess good p0 values
            p0 = FFTGuess(x, y)

        super(CosineFit, self).__init__(x, y, self.FitFunc, self.Jacobian, p0, bounds, confidenceInterval, simult, **kwargs )