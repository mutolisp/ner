# -*- coding: utf-8 -*-
# <nbformat>3.0</nbformat>

# <codecell>

# The original program water97_v13 was written in Visual Basic by Spang, Hamburg, Germany, 2000 - 2002
#      E-Mail: b.spang@hamburg.de
# translated to python by Cheng-Tao Lin 2014-05-30
import math

class water97:

    def __init__(self):
        # constants
        self.rgas_water = 461.526 # gas constant in J/(kg K)
        self.tc_water = 647.096   # critical temperature in K
        self.pc_water = 220.64    # critical pressure in bar
        self.dc_water = 322.0       # critical density in kg/m^3
        self.ireg1 = (0,0,0,0,0,0,0,0,1,1,1,1,1,1,2,2,2,2,2,3,3,3,4,4,4,5,8,8,21,23,29,30,31,32)
        self.jreg1 = (-2,-1,0,1,2,3,4,5,-9,-7,-1,0,1,3,-3,0,1,3,17,-4,0,6,-5,-2,10,-8,-11,-6,-29,-31,-38,-39,-40,-41)
        self.nreg1 = (0.14632971213167,-0.84548187169114,-3.756360367204,3.3855169168385,-0.95791963387872,
                 0.15772038513228,-0.016616417199501,0.00081214629983568,0.00028319080123804,
                 -0.00060706301565874,-0.018990068218419,-0.032529748770505,-0.021841717175414,
                 -5.283835796993e-05,-0.00047184321073267,-0.00030001780793026,4.7661393906987e-05,
                 -4.4141845330846e-06,-7.2694996297594e-16,-3.1679644845054e-05,-2.8270797985312e-06,
                 -8.5205128120103e-10,-2.2425281908e-06,-6.5171222895601e-07,-1.4341729937924e-13,
                 -4.0516996860117e-07,-1.2734301741641e-09,-1.7424871230634e-10,-6.8762131295531e-19,
                 1.4478307828521e-20,2.6335781662795e-23,-1.1947622640071e-23,1.8228094581404e-24,
                 -9.3537087292458e-26)
        self.j0reg2 = (0, 1, -5, -4, -3, -2, -1, 2, 3)
        self.n0reg2 = (-9.6927686500217, 10.086655968018, -0.005608791128302, 0.071452738081455, -0.40710498223928,
                  1.4240819171444, -4.383951131945, -0.28408632460772, 0.021268463753307)
        self.ireg2 = (1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 3, 3, 3, 3, 3, 4, 4, 4, 5, 6, 6, 6, 7, 7, 7, 8, 8, 9, 10, 10, 10, 
                 16, 16, 18, 20, 20, 20, 21, 22, 23, 24, 24, 24)
        self.jreg2 = (0, 1, 2, 3, 6, 1, 2, 4, 7, 36, 0, 1, 3, 6, 35, 1, 2, 3, 7, 3, 16, 35, 0, 11, 25, 8, 36, 13, 4, 
                 10, 14, 29, 50, 57, 20, 35, 48, 21, 53, 39, 26, 40, 58)
        self.nreg2 = (-0.0017731742473213, -0.017834862292358, -0.045996013696365, -0.057581259083432, 
                 -0.05032527872793, -3.3032641670203e-05, -0.00018948987516315, -0.0039392777243355, 
                 -0.043797295650573, -2.6674547914087e-05, 2.0481737692309e-08, 4.3870667284435e-07, 
                 -3.227767723857e-05, -0.0015033924542148, -0.040668253562649, -7.8847309559367e-10, 
                 1.2790717852285e-08, 4.8225372718507e-07, 2.2922076337661e-06, -1.6714766451061e-11, 
                 -0.0021171472321355, -23.895741934104, -5.905956432427e-18, -1.2621808899101e-06, 
                 -0.038946842435739, 1.1256211360459e-11, -8.2311340897998, 1.9809712802088e-08, 
                 1.0406965210174e-19, -1.0234747095929e-13, -1.0018179379511e-09, -8.0882908646985e-11, 
                 0.10693031879409, -0.33662250574171, 8.9185845355421e-25, 3.0629316876232e-13, 
                 -4.2002467698208e-06, -5.9056029685639e-26, 3.7826947613457e-06, -1.2768608934681e-15, 
                 7.3087610595061e-29, 5.5414715350778e-17, -9.436970724121e-07)
        self.ireg3 = (0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 
                 1, 1, 2, 2, 2, 2, 2, 2, 3, 3, 
                 3, 3, 3, 4, 4, 4, 4, 5, 5, 5,
                 6, 6, 6, 7, 8, 9, 9, 10, 10, 11)
        self.jreg3 = (0, 0, 1, 2, 7, 10, 12, 23, 2, 6, 
                 15, 17, 0, 2, 6, 7, 22, 26, 0, 2, 
                 4, 16, 26, 0, 2, 4, 26, 1, 3, 26,
                 0, 2, 26, 2, 26, 2, 26, 0, 1, 26)
        self.nreg3 = (1.0658070028513, -15.732845290239, 20.944396974307, -7.6867707878716, 2.6185947787954,
                 -2.808078114862, 1.2053369696517, -0.0084566812812502, -1.2654315477714, -1.1524407806681,
                 0.88521043984318, -0.64207765181607, 0.38493460186671, -0.85214708824206, 4.8972281541877,
                 -3.0502617256965, 0.039420536879154, 0.12558408424308, -0.2799932969871, 1.389979956946,
                 -2.018991502357, -0.0082147637173963, -0.47596035734923, 0.0439840744735, -0.44476435428739, 
                 0.90572070719733, 0.70522450087967, 0.10770512626332, -0.32913623258954, -0.50871062041158, 
                 -0.022175400873096, 0.094260751665092, 0.16436278447961, -0.013503372241348, -0.014834345352472, 
                 0.00057922953628084, 0.0032308904703711, 8.0964802996215e-05, -0.00016557679795037, 
                 -4.4923899061815e-05)
        self.nreg4 = (1167.0521452767, -724213.16703206, -17.073846940092, 12020.82470247, -3232555.0322333, 
                 14.91510861353, -4823.2657361591, 405113.40542057, -0.23855557567849, 650.17534844798)
        self.nbound = (348.05185628969, -1.1671859879975, 0.0010192970039326, 572.54459862746, 13.91883977887)
        self.n0visc = (1.0, 0.978197, 0.579829, -0.202354)
        self.ivisc = (0, 0, 0, 0, 1, 1, 1, 1, 2, 2, 2, 3, 3, 3, 3, 4, 4, 5, 6)
        self.jvisc = (0, 1, 4, 5, 0, 1, 2, 3, 0, 1, 2, 0, 1, 2, 3, 0, 3, 1, 3)
        self.nvisc = (0.5132047, 0.3205656, -0.7782567, 0.1885447, 0.2151778, 0.7317883, 1.241044, 1.476783,
                 -0.2818107, -1.070786, -1.263184, 0.1778064, 0.460504, 0.2340379, -0.4924179, -0.0417661,
                 0.1600435, -0.01578386, -0.003629481)
        self.n0thcon = (1.0, 6.978267, 2.599096, -0.998254)
        self.nthcon = (1.3293046, -0.40452437, 0.2440949, 0.018660751, -0.12961068, 0.044809953, 1.7018363,
                  -2.2156845, 1.6511057, -0.76736002, 0.37283344, -0.1120316, 5.2246158, -10.124111, 
                  4.9874687, -0.27297694, -0.43083393, 0.13333849, 8.7127675, -9.5000611, 4.3786606, 
                  -0.91783782, 0.0, 0.0, -1.8525999, 0.9340469, 0.0, 0.0, 0.0, 0.0)

    def __gammareg1__(self, tau, pi):
        # Fundamental equation for region 1
        ireg1 = self.ireg1
        jreg1 = self.jreg1
        nreg1 = self.nreg1
        gammareg1 = 0
        g = gammareg1
        for i in range(0,len(nreg1)):
            g = g + nreg1[i]*( 7.1 - math.pi ) ** ireg1[i] * (tau - 1.222) ** jreg1[i]
        return(g)
        #except:
        #    print("Exception caught!")
        #    pass
        
    def __gammapireg1__(self, tau, pi):
        gammapireg1 = 0
        for i in range(0,len(nreg1)):
            gammapireg1 = gammapireg1 - nreg1[i] * ireg1[i] * (7.1 - math.pi) ** (ireg1[i] - 1.0) * (tau - 1.222) ** jreg1[i]
        return(gammapireg1)
    

    def __pbound__(self, t):
        nbound = ws97.nbound
        if t < 623.15 or t > 863.15:
            pbound = -1
        else:
            pbound = (nbound[0] + nbound[1] * t + nbound[2] * t ** 2) * 10.0
        return(pbound)
        
    def __volreg2__(self, t, p):
        
        """
        ' specific volume in region 2
        ' volreg2 in m^3/kg
        ' temperature in K
        ' pressure in bar
        """
        tau = 540.0 / t
        pi = 0.1 * p
        gamma0pireg2 = 1 / pi 
        # where is tau???? original vb
        # Private Function gamma0pireg2(tau,pi)
        #    gamma0pireg2 = 1 / pi
        # End Function
        volreg2 = self.rgas_water * t * pi * (gamma0pireg2+ self.__gammarpireg2__(tau, pi)) / (p * 100000.0)
        return(volreg2)

    #def __gamma0pireg2__(self, tau, pi):
    #    return(gamma0pireg2)
    
    def __gammarpireg2__(self, tau, pi):
        nreg2 = self.nreg2
        ireg2 = self.ireg2
        jreg2 = self.jreg2
        gammarpireg2 = 0
        for i in range(0, len(nreg2)):
            gammarpireg2 = gammarpireg2 + nreg2[i] * ireg2[i] * pi ** (ireg2[i] - 1) * (tau - 0.5) ** jreg2[i]
        return(gammarpireg2)
    
    def __fideltareg3__(self, tau, delta):
        nreg3 = self.nreg3
        ireg3 = self.ireg3
        jreg3 = self.jreg3
        fideltareg3 = nreg3[0] / delta
        for i in range(2,41):
            fideltareg3 = fideltareg3 + nreg3[i] * ireg3[i] * delta ** (ireg3[i] - 1) * tau ** jreg3[i]
        return(fideltareg3)
    
    def __fideltadeltareg3__(tau, delta):
        nreg3 = self.nreg3
        ireg3 = self.ireg3
        jreg3 = self.jreg3
        ideltadeltareg3 = -nreg3[0] / delta ^ 2
        for i in range(2,41):
            fideltadeltareg3 = fideltadeltareg3 + nreg3[i] * ireg3[i] * (ireg3[i] - 1) * delta ** (ireg3[i] - 2) * tau ** jreg3[i]
        return(fideltadeltareg3)
    
    def __densreg3__(self, t, p):
        """
        Determine density in region 3 iteratively using Newton method
        densreg3 in kg/m^3
        temperature in K
        pressure in bar
        densreg3 = -2: not converged
        """
        dc_water = self.dc_water
        tc_water = self.tc_water
        rgas_water = self.rgas_water
        if t < tc_water and p < self.psatw(t):
            densold = 100.0
        else:
            densold = 600.0
        tau = tc_water / t

        for i in range(0,1000):
            delta = densold / self.dc_water
            derivprho = rgas_water * t / dc_water * (2 * densold * self.__fideltareg3__(tau, delta) \
                                    + densold ** 2 / dc_water * self.__fideltadeltareg3__(tau, delta))
            densnew = densold + (p * 100000.0 - rgas_water * t * densold ** 2 / dc_water * \
                                 self.__fideltareg3__(tau, delta)) / derivprho
            diffdens = np.abs(densnew - densold)
            if diffdens < 5e-06:
                densreg3 = densnew
                return(densreg3)
            densold = densnew
        return(-2)
    
    #####################


    def tsatw(self,p):
        """
        9. Boiling point as a function of pressure    
        ==========================================
        """
        try:
            nreg4 = self.nreg4
            if p < 0.00611213 or p > 220.64:
                tsatw = -1
            else:
                bet = (0.1 * p)**0.25
                eco = bet ** 2 + nreg4[2] * bet + nreg4[5]
                fco = nreg4[0] * bet ** 2 + nreg4[3] * bet + nreg4[6]
                gco = nreg4[1] * bet ** 2 + nreg4[4] * bet + nreg4[7]
                dco = 2 * gco / (-fco - (fco ** 2 - 4 * eco * gco) ** 0.5)
                tsatw = 0.5 * (nreg4[9] + dco - ((nreg4[9] + dco) ** 2 - 4 * (nreg4[8] + nreg4[9] * dco)) ** 0.5)
            return(tsatw)
        except:
            raise
    
    def psatw(self,t):
        """
        10. Vapor pressure
        ==================
        """
        nreg4 = self.nreg4
        if t < 273.15 or t > 647.096:
            psatw = -1
        else:
            d = t + nreg4[8] / ( t - nreg4[9])
            aco = d **  2 + nreg4[0] * d + nreg4[1]
            bco = nreg4[2] * d**2 + nreg4[3]* d + nreg4[4]
            cco = nreg4[5] * d**2 + nreg4[6]* d + nreg4[7]
            psatw = (2 * cco / (-bco + (bco ** 2 - 4 * aco * cco) ** 0.5)) ** 4 * 10
        return(psatw)
           
    def dens_sat_vaptw(self, t):
        """
        Density of saturated steam as a function of temperature
        =======================================================
        densSatVapTW in kg/m^3
        temperature in K
        densSatVapTW = -1: temperature outside range
        """
        if t >= 273.15 and t <= 623.15:
            p = self.psatw(t)
            dens_sat_vaptw = 1 / self.__volreg2__(t, p)
        elif t > 623.15 and t <= self.tc_water:
            p = self.psatw(t) - 1e-05
            dens_sat_vaptw = self.__densreg3__(t, p)
        else:
            dens_sat_vaptw = -1
        return(dens_sat_vaptw)
# <codecell>
