# -*- coding: utf-8 -*-
"""
Created on Wed Apr 19 17:15:28 2023

@author: Lenovo
"""

from math import sqrt, sin, cos, atan, atan2, degrees


class Transformacje:
    def __init__(self, model: str = 'wgs84'):
        """
        Parametry elipsoid:
            a - duża półoś elipsoidy - promień równikowy
            b - mała półoś elipsoidy - promień południkowy
            flat - spłaszczenie
            e2 - mimośród^2
        """
        if model == "wgs84":
            self.a = 6378137.0
            self.b = 6356752.31424518
        elif model == "grs80":
            self.a = 6378137.0
            self.b = 6356752.31414036
        else:
            raise NotImplementedError(f"{model} model not implemented")
        self.flat = (self.a - self.b) / self.a
        self.e = sqrt(2 * self.flat - self.flat ** 2) # eccentricity
        self.e2 = (2 * self.flat - self.flat ** 2) # eccentricity**2

    def transformacja1(self, X, Y, Z):
            """
            Algorytm Hirvonena – algorytm służący do transformacji współrzędnych ortokartezjańskich 
            (prostokątnych) x, y, z na współrzędne geodezyjne B, L, h. Jest to proces iteracyjny. 
            W wyniku 3-4-krotnego powtarzania procedury można przeliczyć współrzędne n
            a poziomie dokładności 1 cm
            Parameters
            ----------
            X, Y, Z : FLOAT
                 współrzędne w układzie orto-kartezjańskim, 

            Returns
            -------
            fi : FLOAT
                [stopnie dziesiętne] - szerokość geodezyjna
            la : FLOAT
                [stopnie dziesiętne] - długośc geodezyjna.
            h : FLOAT
                [metry] - wysokość elipsoidalna
            output [STR] - optional, defaulf 
                dec_degree - decimal degree
                dms - degree, minutes, sec

            """
            r = sqrt(X**2 + Y**2) # promień
            fi = atan(Z/(r*(1 - self.e2))) # pierwsze przybliżenie fi
            while True:
                N = self.a / sqrt(1 - self.e2 * sin(fi)**2)
                h = (r/cos(fi)) - N
                fp = fi
                fi = atan(Z/(r *(1-(self.e2*(N/(N+h))))))
                if abs(fp-fi) < (0.000001/206265):
                    break 
            la = atan2(Y,X)
            N = self.a / sqrt(1 - self.e2 * (sin(fi))**2)
            h = r / cos(fi) - N     
            return degrees(fi), degrees(la), h
        
# wywołanie funkcji trasformacja1 - przykład na jednym punkcie żeby sprawdzić poprawność kodu
if __name__ == "__main__":
    # utworzenie obiektu
    geo = Transformacje(model = "wgs84")
    # dane XYZ geocentryczne
    X = 3664940.500; Y = 1409153.590; Z = 5009571.170
    fi, la, h = geo.transformacja1(X, Y, Z)
    print(fi, la, h)
    # phi, lam, h = geo.xyz2plh2(X, Y, Z)
    # print(phi, lam, h)