def Travalloni(V):
    import numpy as np
    return (R*T)/(V-b_p) - (a_p/V**2) - theta*(b/V**2)*(1-b/V)**(
                    (theta -1)) *(1-F_pr)*(R*T*(1-np.exp(
                    (-Na*espilon)/(R*T))-Na*espilon)) 

