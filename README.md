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


    from potential_wind import ws
    from preprocess import cwb_preproc
    import potential_wind as pw
    import pandas as pd
    import numpy as np
    \#initialization 
    pws = pw.ws()
    cwb = cwb_preproc()

    pws.psatw(283.15) 
    
