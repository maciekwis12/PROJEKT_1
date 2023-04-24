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
            return degrees(fi), degrees(la), h
        
# Tutaj będą wywoływane funkcje oraz odczytywane i zapisywane pliki tekstowe:
if __name__ == "__main__":
    
    # Utworzenie obiektu
    geo = Transformacje(model = "wgs84")
    #geo = Transformacje(model = "grs80")
    print('Transformacje do wyboru: \n XYZ -> BLH (1) \n BLH -> XYZ (2)')
    print('Wpisz numerek w nawiasie aby wykonać obliczenia dla odpowiedniej transformacji')
    
    wybrana_transformacja = input() 
    
    if wybrana_transformacja == '1':
        # Dane XYZ z pliku tekstowego
        with open('input_xyz.txt', 'r') as plik:
            wiersze = plik.readlines()
            punkty = [] # [[X1, Y1, Z1], ..., [Xn, Yn, Zn]]
            for i in range(0, len(wiersze)):
                wspolrzedne_punkt = wiersze[i].split(',')
                for xyz in range(0, len(wspolrzedne_punkt)):
                    wspolrzedne_punkt[xyz] = float(wspolrzedne_punkt[xyz])
                punkty.append(wspolrzedne_punkt)
                
        # Przerzucenie wyników do listy flh
        flh = []
        for punkt in range(0,len(punkty)):
            fi, la, h = geo.transformacja1(punkty[punkt][0], punkty[punkt][1], punkty[punkt][2])
            flh.append([fi,la,h])
        
        # Zapisanie wyników do pliku tekstowego
        with open('output_flh.txt', 'w') as plik:
            plik.write('Wyniki przedstawione w formacie: [fi, la, h] \n')
            for punkt in range(0, len(flh)):
                plik.write(f'{flh[punkt]} \n')

    if wybrana_transformacja == '2':
        # Kod dla transformacji2
        pass
    