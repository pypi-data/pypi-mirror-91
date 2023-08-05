from scipy.optimize import fsolve
from gas_dynamics.extra import arctand
from gas_dynamics.fluids import fluid, air



#==================================================
#prandtl_meyer_turn
#need to add examples
#==================================================
def prandtl_meyer_turn(M: float, gas=air) -> float:
    """Returns the angle through which a flow has turned to reach a Mach number
    
    Notes
    -----
    Given a Mach number and ratio of specific heats, calculate the angle of a turn
    through which a flow has traversed to reach the Mach number given, from a  Mach number
    of 1. Also known as the Prandtl-Meyer function. Default fluid is air.
    
    Parameters
    ----------
    M : `float`
        The Mach number \n
    gas : `fluid`
        A user defined fluid object. Default is air \n    
    
    Returns
    -------
    float
        The angle in degrees through which the flow has turned\n

    Examples
    --------
    >>> import gas_dynamics as gd
    >>> M = 2 
    >>> delta = gd.prandtl_meyer_turn(M=2)
    26.379760813416475
    >>>
    """

    gamma = gas.gamma
    nu = ((gamma+1)/(gamma-1))**.5 * arctand(((M**2-1)*(gamma-1)/(gamma+1))**.5) - arctand((M**2-1)**.5)
    return nu



#==================================================
#prandtl_meyer_mach
#need to add examples
#==================================================
def prandtl_meyer_mach(nu: float, gas=air) -> float:
    """Returns the Mach number given an angle through which the flow has turned from a starting Mach of one
    
    Notes
    -----
    Given a smooth turn through which a flow has turned and the ratio of specific
    heats, return the Mach number after the turn.

    Parameters
    ----------
    nu : `float`
        The turn angle in degrees \n    
    gas : `fluid`
        A user defined fluid object. Default is air \n    

    Returns
    -------
    float
        The mach number\n

    Examples
    --------
    >>> import gas_dynamics as gd
    >>> nu = 26.37
    >>> M = gd.prandtl_meyer_mach(nu=nu) 
    >>> M
    1.9996459342662083
    >>>
    """
    
    def get_mach(M: float, nu=nu, gas=gas) -> float:
        return prandtl_meyer_turn(M, gas=gas) - nu
    
    sol = fsolve(get_mach, x0=1.5, args=(nu, gas))
    return sol[0]