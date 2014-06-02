ner
===

Natural energy resources in Taiwan
----------------------------------

The potential_wind.py contains classes ws and ws_array to compute the vapor pressure and density of saturated
steam as a function of temperature (the original algorithm was written by Spang). The ws_array
class used pandas DataFrame to compute (in progress, not run)


Language
--------

Python


Calculation
-----------


    >>> from potential_wind import ws
    >>> import potential_wind as pw
    >>> import numpy as np

    >>> #initialization 
    >>> pws = pw.ws()

    # psatw will calculte the vapor pressure in 
    # given temperature (unit: K)
    >>> pws.psatw(283.15) 
    0.012281838693402238

    # calc_pw(tx, ps, rh, wd) compute the density of wind and
    # wind energy resources
    >>> pws.calc_pw(tx=283.15, ps=1000.6, rh=86, wd=2)
    (1.2, 42.38665324033601)

