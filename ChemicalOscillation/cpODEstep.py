#************************************************************************
# cpODEstep : performs steps for numerical solution of 
#             Ordinary Differential Equations using a variety of methods
#
# Classes
#   cpODEstep : base class (all other inherit from this)
#   cpODEstepEuler: implements Euler algorithm
#   cpODEstepRK2:   implements 2nd Order Runge-Kutta algorithm
#   cpODEstepRK4:   implements 4th Order Runge-Kutta algorithm
#   cpODEstepDP5:   implements 5th Order Dormand-Prince adaptive step algorithm
#
# Methods
#   cpODEstep( initStep,ODEmodel,tol )
#     h0       = initial step size
#     ODEmodel = pointer to an already-created cpODEmodelXXX class
#     tol      = convergence condition
#     step()   : takes one step forward based on algorithm
#
#************************************************************************

import numpy as np
import copy
from math import sqrt
from decimal import Decimal

DEFTOL = 1e-8
MAXITER = 10

#========================================================================
# cpODEstep: base class
#========================================================================
class cpODEstep:
  def __init__(self, h0, model, tol = DEFTOL):
    """
    Base class for different algorithms to step through ODE solution

    :param float h0: initial step size
    :param cpODEmodel model: ODE model to solve
    :param float tol: tolerance (optional, for adaptive step algorithms)
    """
    self._h = h0
    self._ode = model
    self._tol = tol
    return

  def step(self):
    """
    Move forward one step. Algorithm specific.

    "raises Exception: if not implemented by daughter class
    """
    raise Exception("ERROR: Calling step on the base class does nothing, you need to call it on an implementation.")

  def setStep(self, h):
    """
    Update step size.

    :param float h: new step size
    """
    self._h = h

  def getStep(self):
    """
    Get current step size.

    :return float h: current step size
    """
    return self._h

  def update(self, s):
    """
    Move from t_n,s_n --> t_(n+1),s_(n+1)
      t_n --> t_(n+1) = t_n + h
      s_n --> s_(n+1)

    :param array_like s: current state
    """
    t_n1 = self._ode.getTime() + self._h
    self._ode.setTime( t_n1 )
    self._ode.setState( s )
    self._ode.setRate( self._ode.getRate(t_n1, s) )
    self._ode.setAnalyticState( t_n1 )
    return


#========================================================================
# cpODEstepEuler: Euler step method
#========================================================================
class cpODEstepEuler(cpODEstep):
  def __init__(self, initStep, ODEmodel, tol = DEFTOL):
    """
    Euler method for stepping through ODE:
      t_[n+1] = t_n + h
      s_(n+1) = s_n  +  h (ds/dt)_n

    :param float h0: initial step size
    :param cpODEmodel model: ODE model to solve
    :param float tol: tolerance (not used for Euler)
    """
    cpODEstep.__init__(self, initStep, ODEmodel, tol)

  def step(self):
    """
    Take a step using Euler method:
      t_[n+1] = t_n + h
      s_(n+1) = s_n  +  h (ds/dt)_n

    :return float h: current step size
    """
    # Current state
    t    = self._ode.getTime()
    h   = self._h
    s    = np.array(self._ode.getState())
    dsdt = self._ode.getRate

    # Take step
    s += h * dsdt(t, s)
    self.update( s )

    return h


#========================================================================
# cpODEstepRK2: 2nd order Runge-Kutta step method
#========================================================================
class cpODEstepRK2(cpODEstep):
  def __init__(self, initStep, ODEmodel, tol = DEFTOL):
    """
    2nd order Runge-Kutta method for stepping through ODE:
      t_[n+1] = t_n + h
      k_1 = h ds/dt( t_n, s_n )
      k_2 = h ds/dt( t_n + h/2, s_n + k_1/2 )
      s^(i)( t_[n+1] ) = s^(i)( t_n )  +  k_2

    :param float h0: initial step size
    :param cpODEmodel model: ODE model to solve
    :param float tol: tolerance (not used for RK2)
    """
    cpODEstep.__init__(self, initStep, ODEmodel, tol)

  def step(self):
    """
    Take a step using RK2 method:
      t_[n+1] = t_n + h
      k_1 = h ds/dt( t_n, s_n )
      k_2 = h ds/dt( t_n + h/2, s_n + k_1/2 )
      s^(i)( t_[n+1] ) = s^(i)( t_n )  +  k_2

    :return float h: current step size
    """
    # Current state
    t    = self._ode.getTime()
    h    = self._h
    s    = np.array(self._ode.getState())
    dsdt = self._ode.getRate

    # Calculate intermediate states
    k1 = h * dsdt(t     , s      )
    k2 = h * dsdt(t+h/2., s+k1/2.)

    # Take step
    s += k2
    self.update( s )

    return h


#========================================================================
# cpODEstepRK4: 4th order Runge-Kutta step method
#========================================================================
class cpODEstepRK4(cpODEstep):
  def __init__(self, initStep, ODEmodel, tol = DEFTOL):
    """
    4th order Runge-Kutta method:
      t_[n+1] = t_n + h
      k_1 = h ds/dt( t_n, s_n )
      k_2 = h ds/dt( t_n + h/2, s_n + k_1/2 )
      k_3 = h ds/dt( t_n + h/2, s_n + k_2/2 )
      k_4 = h ds/dt( t_n + h  , s_n + k_3 )
      s^(i)( t_[n+1] ) = s^(i)( t_n )  +  (1/6)( k_2 + 2k_2 + 2k_3 + k_4 )

    :param float h0: initial step size
    :param cpODEmodel model: ODE model to solve
    :param float tol: tolerance (not used for RK4)
    """
    cpODEstep.__init__(self, initStep, ODEmodel, tol)

  def step(self):
    """
    Take a step using RK4 method:
      t_[n+1] = t_n + h
      k_1 = h ds/dt( t_n, s_n )
      k_2 = h ds/dt( t_n + h/2, s_n + k_1/2 )
      k_3 = h ds/dt( t_n + h/2, s_n + k_2/2 )
      k_4 = h ds/dt( t_n + h  , s_n + k_3 )
      s^(i)( t_[n+1] ) = s^(i)( t_n )  +  (1/6)( k_2 + 2k_2 + 2k_3 + k_4 )

    :return float h: current step size
    """
    # Current state
    t    = self._ode.getTime()
    h    = self._h
    s    = np.array(self._ode.getState())
    dsdt = self._ode.getRate

    # Calculate intermediate states
    k1 = h * dsdt(t     , s      )
    k2 = h * dsdt(t+h/2., s+k1/2.)
    k3 = h * dsdt(t+h/2., s+k2/2.)
    k4 = h * dsdt(t+h   , s+k3   )

    # Take step
    s += (1./6.)*(k1 + 2.*k2 + 2.*k3 + k4)
    self.update( s )

    return h


#=======================================================================
# cpODEstepDP5: Dormand-Price adaptive step algorithm
#=======================================================================
class cpODEstepDP5(cpODEstep):
  def __init__(self, initStep, ODEmodel, tol = DEFTOL):
    """
    Dormand-Price adaptive step algorithm using 4th vs 5th order Runge-Kutta methods.
    See NR 17.2 for details.
    """
    cpODEstep.__init__(self, initStep, ODEmodel, tol)

  def step(self):
    """
    Take a step using the Dormand-Price adaptive step algorithm using
    4th vs 5th order Runge-Kutta methods. See NR 17.2 for details.

    :param float h0: initial step size
    :param cpODEmodel model: ODE model to solve
    :param float tol: tolerance
    """
    # Current state
    h   = self._h

    # Iterate to find optimal step size for this step and next
    snext = np.array(self._ode.getState())
    hNext = h
    i = 0
    for i in range(MAXITER):
      snext, error = self._trialStep(h)
      tryagain, hNext = self._needNewStep(h, snext, error)

      if tryagain:
        h = hNext
      else:
        break

    if i == MAXITER-1:
      print("ERROR: DP5 algorithm did not converge")
      return -1

    self._h = h
    self.update( snext )
    self._h = hNext

    return h

  def _trialStep(self, h):
    """
    Take a trial step with step size h.

    :param float h: step size to try
    :return: tuple of (snext, error)
      snext is state at at step n+1 (using h)
      error is the vector of Delta y(5)_{n+1} - y(4)_{n+1}
    """
    # Dormand-Prince 5(4) coefficients from table in NR 17.2
    c = [0.0, 0.2, 0.3, 0.8, 8.0/9.0, 1.0, 1.0]
    a = [
      [ 0.0 ],
      [ 0.2 ],
      [ 3.0/40.0      , 9.0/40.0 ],
      [ 44.0/45.0     , -56.0/15.0     , 32.0/9.0 ],
      [ 19372.0/6561.0, -25360.0/2187.0, 64448.0/6561.0, -212.0/729.0 ],
      [ 9017.0/3168.0 , -355.0/33.0    , 46732.0/5247.0, 49.0/176.0  , -5103.0/18656.0 ],
      [ 35.0/384.0    , 0.0            , 500.0/1113.0  , 125.0/192.0 , -2187.0/6784.0 , 11.0/84.0 ]
    ]
    e = [71./57600., 0., -71./16695., 71./1920., -17253./339200, 22./525., -1./40. ]

    t = self._ode.getTime()
    s = self._ode.getState()
    dsdt = self._ode.getRate

    snext = np.array(s)

    k = [ dsdt(t, s) ]
    for i in range(1, 7):
      snext = np.array(s)
      for j in range(0, i):
        snext += h * a[i][j] * k[j]
      k.append( dsdt(t + c[i]*h, snext) )

    error = np.array([0.]*len(s))
    for j in range(7):
      error += h * e[j] * k[j]
    return snext, error

  def _needNewStep(self, h, snext, error):
    """
    Check s_{n+1} if a new step size is needed in order to achieve
    the desired tolerance and calculate the size of the
    next step (no PI control):

    :param float h: current step size
    :param float snext: current s_{n+1}
    :param float error: error vector of Delta = s(5)_{n+1} - s(4)_{n+1}
    :return: tuple of (tryagain, hNext)
      tryagain = True/False if another try is needed
      hNext = new step size
    """
    alpha = 0.2
    safe = 0.9
    minscale = 0.2
    maxscale = 10.0

    s = self._ode.getState()
    diff = self._errorCalc(snext, error)
    hNext = h

    if diff <= 1.0:
      scale = maxscale if diff == 0 else safe*pow(diff,-alpha)
      hNext = h * min(scale, maxscale)
      return False, hNext
    else:
      scale = safe * pow(diff, -alpha)
      hNext = h * max(scale, minscale)
      return True, hNext
    
  def _errorCalc(self, snext, error):
    """
    Calculate error [0.0-1.0] for this step 
    as Euclidean sum of individual state 
    equation error terms normalized to the tolerance:
      diff = 1/Neqn Sum_i=1,N ( Delta_i / tolerance_i )^2

    :param float snext: next step s_{n+1}
    :param float err: vector of Delta = s(5)_{n+1} - s(4)_{n+1}
    :return float: calculated error
    """
    esum = 0.
    s = self._ode.getState()
    N = len(s)
    
    for i in range(N):
      scale = self._tolerance(s[i], snext[i])
      esum += pow(error[i]/scale, 2)

    return sqrt( esum/N )

  def _tolerance(self, s, snext):
    """
    Calculate the error tolerance scale:
      scale = tol + max(|s_n|,|s_n+1|) tol
    Includes both relative tolerance (on state, s) and
    absolute tolerance (mainly for oscillatory cases).
    Uses max(s_n,s_n+1) to avoid division by zero
    :param float s_i: the state at step n for the ith ODE equation
    :param float snext_i: the state at steps n+1 for the ith ODE equation
    :return float: tolerance
    """
    return self._tol + self._tol * max(abs(s), abs(snext))

