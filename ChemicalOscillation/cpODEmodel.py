#************************************************************************
# cpODEmodel : Ordinary Differential Equations for different models
#   Problem is broken into a set of coupled 1st order ODEs
#     ds^(i)/dt = f( t,s^(0),...,s^(N-1) )
#   These classes specify the state vector (s) and the functions ds/dt
#
# Classes
#   cpODEmodel        : base class (all other inherit from this)
#   cpODEmodelFall1D  : falling motion in 1D
#   cpODEmodelFallAir : falling motion in 1D with air resistance
#   cpODEmodelSHO     : Simple Harmonic Oscillator
#   cpODEmodelDecay   : exponential decay
#
# Methods
#   cpODEmodel(s0,p,[t0] )
#     s0 = vector of initial values at t0
#     p  = vector with other params for this model
#     t0 = initial time (default=0)
#************************************************************************

from math import sin, cos, exp
import numpy as np

class cpODEmodel:
  """
  Base class for different models of Ordinary Differential Equations.
  Problem is broken into a set of coupled 1st order ODEs:
    ds^(i)/dt = f( t,s^(0),...,s^(N-1) )
  Daughter classes specify the state vector (s) and the functions ds/dt.
  """
  def __init__(self, s0, p, t0):
    """
    cpODEmodel constructor

    :param array_like s0: vector of initial values at t0
    :param array_like p: vector with other parameters for this model
    :param float t0: initial time
    """
    self._t0 = t0
    self._t = t0
    self._s0 = np.array(s0, dtype=np.double)
    self._s = np.array(s0, dtype=np.double)
    self._sAnalytic = np.array(s0, dtype=np.double)
    self._dsdt = np.array(self.getRate(t0, s0), dtype=np.double)

  def getRate(self, t, s):
    """
    Unimplementd function calculating the rate of the system for the passed
    time/state. Model dependent.

    :param float t: time
    :param array_like s: state
    :raises Exception: if not implemented by daughter class
    """
    raise Exception("ERROR: cpODEmodel.getRate(t,s) not implemented!")

  def setAnalyticState(self, t):
    """
    Unimplemented function that updates the analytic state (if available)
    based on current time. Model dependent.

    :param float t: current time
    """
    return

  def energy(self):
    """
    Unimplemented function for calculating current energy of the system. Model dependent.

    :raises Exception: if not implemented by daughter class
    """
    raise Exception("ERROR: cpODEmodel.energy() not implemented!")

  def deviation(self, ana, num):
    """
    Fractional deviation between analytic and numeric state:
      dev = ( Ana - Num ) / Ana             if Ana not too close to zero
          = ( Ana - Num ) / max( Num,Ana )  otherwise

    :param float ana: analytic state
    :param float num: numeric state
    :return float: deviation
    """
    if num == 0 and ana == 0:
      return 0
    if abs(ana) > 1e-10:
      return 1.0 - num/ana
    return (ana - num) / max(abs(num), abs(ana))

  def setTime(self, t):
    """
    Sets the current time

    :param float t: time
    """
    self._t = t
    return

  def setState(self, s):
    """
    Sets the state vector.

    :param array_like s: current state
    """
    self._s = np.array(s, dtype=np.double)
    return

  def setRate(self, dsdt):
    """
    Sets the rate vector.

    :param array_like dsdt: curent rate ds/dt
    """
    self._dsdt = np.array(dsdt, dtype=np.double)
    return

  def reset(self):
    """
    Sets everything to initial conditions.
    """
    self.setState( self._s0 )
    self.setAnalyticState( self._t0 )
    self.setTime( self._t0 )
    self.setRate( np.array(self.getRate(self._t0, self._s0), dtype=np.double) )
    return

  def getTime(self):
    """
    Returns the current time.

    :return float: current time
    """
    return self._t

  def getState(self):
    """
    Returns the current state.

    :return array: current state
    """
    return self._s

#===========================================================
# cpODEmodelFall1D: 1D falling object w/o air resistant
#===========================================================
class cpODEmodelFall1D(cpODEmodel):
  def __init__(self, s0, p, t0):
    """
    Model describing 1-D falling point mass near earth surface:
      dx/dt = v
      dv/dt = -g

    :param array_like s0: initial values s0 = [y0, v0]
    :param array_like p: model parameters
      p[0] = |g| (accel due to gravity)
    :param float t0: initial time
    """
    self._g = p[0]
    cpODEmodel.__init__(self, s0, p, t0)

  def getRate(self, t, s):
    """
    Implements free fall near earth surface:
      dx/dt = v
      dv/dt = -g
    note: ds/dt does not depend on t here.

    :param float t: current time
    :param array_like s: current state = [y, v]
    :return array: current rate = [v, a]
    """
    dsdt = np.array([0] * len(s), dtype=np.double)
    dsdt[0] = s[1]
    dsdt[1] = -self._g
    return dsdt

  def setAnalyticState(self, t):
    """
    Solves 1-D falling analytically at time t:
      x(t) = x_0 + v_0 [t-t0] - 1/2 g [t-t0]^2
      v(t) = v_0 - g [t-t0]

    :param float t: current time
    """    
    self._sAnalytic[0] = self._s0[0] + self._s0[1]*(t - self._t0) - 0.5*self._g*pow(t - self._t0, 2)
    self._sAnalytic[1] = self._s0[1] - self._g*(t - self._t0)
    return self._sAnalytic

  def energy(self):
    """
    Returns E = K + U for current state:
      K = 1/2 v^2
      U = g x

    :return float: energy
    """
    K = 0.5 * pow(self._s[1],2)
    U = self._g * self._s[0]
    return K + U

#===========================================================
# cpODEmodelFallAir: 1D falling object w/ air resistant
#===========================================================
class cpODEmodelFallAir(cpODEmodel):
  def __init__(self, s0, p, t0):
    """
    Model describing 1-D falling with air resistance:
      dx/dt = v
      dv/dt = -g( 1 - v^2 / v_t^2 )

    Note:
      No energy calculated (not conserved)
      Analytic state = state w/ *no* air resistance

    :param array_like s0: initial state s0 = [y0, v0]
    :param array_like p: model parameters
      p[0] = |g| (accel due to gravity)
      p[1] = vt (terminal velocity)
    :param float t0: initial time
    """
    self._g = p[0]
    self._vt = p[1]
    cpODEmodel.__init__(self, s0, p, t0)

  def getRate(self, t, s):
    """
    Implements 1D falling with air resistance
      dx/dt = v
      dv/dt = -g( 1 - v^2 / v_t^2 )
    note: ds/dt does not depend on t here

    :param float t: current time
    :param array_like s: current state = [y, v]
    :return array: current rate = [v, a]
    """
    dsdt = np.array([0] * len(s), dtype=np.double)
    dsdt[0] = s[1]
    dsdt[1] = -self._g * ( 1.0 - pow(s[1],2)/pow(self._vt,2) )
    return dsdt

  def setAnalyticState(self, t):
    """
    Returns analytic solution for no air resistance case:
      x(t) = x_0 + v_0 [t-t0] - 1/2 g [t-t0]^2
      v(t) = v_0 - g [t-t0]

    :param float t: current time
    """
    self._sAnalytic[0] = self._s0[0] + self._s0[1]*(t - self._t0) - 0.5*self._g*pow(t - self._t0, 2)
    self._sAnalytic[1] = self._s0[1] - self._g*(t - self._t0)
    return

#===========================================================
# cpODEmodelSHO: Simple Harmonic Oscillator
#===========================================================
class cpODEmodelSHO(cpODEmodel):
  def __init__(self, s0, p, t0):
    """
    Model describing simple harmonic oscillator:
      dx/dt = v
      dv/dt = -omega^2 x

    :param array_like s0: initial state = [Amplitude, 0] (assumed to be released at maximum)
    :param array_like p: model parameters
      p[0] = T (period of oscillation)
    :param float t0: initial time
    """
    self._omega = 2*np.pi/p[0]  # angular frequency = sqrt(k/m) = 2pi/T
    cpODEmodel.__init__(self, s0, p, t0)

  def getRate(self, t, s):
    """
    Implements Simple Harmonic Oscillator:
      dx/dt = v
      dv/dt = -omega^2 x
    note: ds/dt does not depend on t here

    :param float t: current time
    :param array_like s: current state = [x, v]
    :return array: current rate = [v, a]
    """
    dsdt = np.array([0] * len(s), dtype=np.double)
    dsdt[0] = s[1]
    dsdt[1] = -pow(self._omega,2) * s[0]
    return dsdt

  def setAnalyticState(self, t):
    """
    Solves SHO analytically at time t (not general - assumes x0=A, v0=0)
      x(t) = x_0 cos( omega t )
      v(t) = v_0 - g [t-t0]

    :param float t: current time
    """
    self._sAnalytic[0] = self._s0[0] * cos( self._omega*(t - self._t0) )
    self._sAnalytic[1] = -self._s0[0] * self._omega * sin( self._omega*(t - self._t0) )
    return

  def energy(self):
    """
    Returns E = K + U for current state
      K = 1/2 v^2
      U = 1/2 k x^2

    Note: assumes unit mass

    :return float: current energy
    """
    K = 0.5 * pow(self._s[1],2)
    U = 0.5 * pow(self._omega*self._s0[0],2)
    return K + U

#===========================================================
# cpODEmodelDecay: Exponential Decay - dN/dt = -lambda N
#===========================================================
class cpODEmodelDecay(cpODEmodel):
  def __init__(self, s0, p, t0):
    """
    Model describing exponential decay
      dN/dt = -lambda N

    Note: no energy calculated

    :param array_like s0: initial state = [N0]
    :param array_like p: model parameters
      p[0] = lambda (1/tau)
    :param float t0: initial time
    """
    self._lambda = p[0] 
    cpODEmodel.__init__(self, s0, p, t0)

  def getRate(self, t, s):
    """
    Implements exponential decay
      dN/dt = -lambda N
    note: dN/dt does not depend on t here

    :param float t: current time
    :param array_like s: current state = [N]
    :return array: current rate = [dN/dt]
    """
    dsdt = np.array([0] * len(s), dtype=np.double)
    dsdt[0] = -self._lambda * s[0]
    return dsdt

  def setAnalyticState(self, t):
    """
    Solves N at time t:
      N(t) = N0 exp( -lambda t )

    :param float t: current time
    """
    self._sAnalytic[0] = self._s0[0] * exp(-self._lambda * (t - self._t0))
    return
