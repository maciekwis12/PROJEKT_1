# -*- coding: utf-8 -*-
"""
Created on Wed Apr 19 17:15:28 2023

@author: Lenovo
"""

from math import sqrt, sin, cos, tan, atan, atan2, degrees, radians, pi
from numpy import arctan2, arctan, array, transpose, arccos

class Transformacje:
    def __init__(self, model: str = 'wgs84'):
        """
        Parametry elipsoid:
            a - duża półoś elipsoidy - promień równikowy
            b - mała półoś elipsoidy - promień południkowy
            flat - spłaszczenie
            e2 - mimośród**2
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
            (prostokątnych) X, Y, Z na współrzędne geodezyjne B, L, H. Jest to proces iteracyjny. 
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
            
            return(round(degrees(fi),6), round(degrees(la),6), round(h,6))
        
    def transformacja2(self, fi, la, h):
        """
        Zadanie odwrotne do algorytmu Hirvonena. 
        Przeliczenie z układu geodezyjnego BLH do układu ortokartezjańskiego XYZ.
        Parameters
        ----------
        fi, la, h : FLOAT
             współrzędne w układzie geodezyjnym BLH, 

        Returns
        -------
        X : FLOAT
            [metry]
        Y : FLOAT
            [metry]
        Z : FLOAT
            [metry]
        output [STR] 

        """
        fi = radians(fi)
        la = radians(la)
        N = self.a / sqrt(1 - self.e2 * sin(fi)**2)
        X = (N+h)*cos(fi)*cos(la)
        Y = (N+h)*cos(fi)*sin(la)
        Z = (N*(1-self.e2)+h)*sin(fi)
        return(round(X,6), round(Y,6), round(Z,6))
    
    def transformacja3(self, Xa, Ya, Za, Xb, Yb, Zb):
        """
        Transformacja współrzędnych kartezjańskich na parametry wektora przestrzennego w układzie
        topocentrycznym.
        Parameters
        ----------
        Xa, Ya, Za, Xb, Yb, Zb : FLOAT
            początkowe(a) i końcowe(b) współrzędne kartezjańkie wektora przestrzennego
        Returns
        ----------
        sab : FLOAT
            [metry]
        alfaab : FLOAT
            [stopnie dziesiętne]
        zab: FLOAT
            [stopnie dziesiętne]
        
        
        """
        r = sqrt(Xa**2 + Ya**2) 
        fi_a = arctan(Za/(r*(1 - self.e2))) 
        while True:
            N = self.a / sqrt(1 - self.e2 * sin(fi_a)**2)
            h = (r/cos(fi_a)) - N
            fp = fi_a
            fi_a = arctan(Za/(r *(1-(self.e2*(N/(N+h))))))
            if abs(fp-fi_a) < (0.000001/206265):
                break 
        la_a = atan2(Ya, Xa)
        
        R = array([[-sin(fi_a)*cos(la_a), -sin(la_a), cos(fi_a)*cos(la_a)], 
                 [-sin(fi_a)*sin(la_a), cos(la_a), cos(fi_a)*sin(la_a)],
                 [ cos(fi_a), 0, sin(fi_a)]])
        dX = array([[Xb-Xa],
                           [Yb-Ya],
                           [Zb-Za]])
        dneu = transpose(R)@dX
        sab = sqrt(dneu[0]**2 + dneu[1]**2 + dneu[2]**2)
        alfaab = arctan2(dneu[1],dneu[0])
        zab = arccos(dneu[2]/sab)
        return(round(sab,6), round(degrees(alfaab),6), round(degrees(zab),6))
        
    def transformacja4(self, fi, la, L0):
        """
        Transformacja współrzędnych do układu 2000 - transformacja stosowana na potrzeby wykonania map w skalach większych
        od 1:10 000. Odwzorowanie oparte na na odwzorowaniu Gaussa-Krugera w czterech trzystopniowych strefach południkowych
        osiowych: 15st E, 18st E, 21st E i 24 st E, oznaczone odpowiednio numerami - 5,6,7,8. 
        Prowadzi kolejno do wyznaczenia płaskich współrzędnych kartezjańsich (xgk, ygk) w oparciu o współrzędne geodezyjne
        (fi, la), a następnie w oparciu o skalę (m0 = 0.999923) do wzynaczenia współrzędnych w układzie 2000.
        
        Parameters
        ----------
        fi, la, L0 : FLOAT
            Współrzędne geodezyjne
       
        Returns
        -------
        x2000 : FLOAT
            [metry] - pierwsza współrzędna
        y2000 : FLOAT
            [metry] - druga współrzędna
        
        """
        fi = radians(fi)
        la = radians(la)
        L0 = radians(L0)
        b2 = (self.a**2)*(1-self.e2)
        ep2 = ((self.a**2)-(b2))/(b2)
        t = tan(fi)
        n2 = ep2*((cos(fi))**2)
        N = (self.a)/sqrt(1-self.e2*sin(fi)**2)
        A0 = 1-(self.e2/4)-((3*(self.e2**2))/64)-((5*(self.e2**3))/256)
        A2 = (3/8)*(self.e2+((self.e2**2)/4)+(15*(self.e2**3)/128))
        A4 = (15/256)*((self.e2**2)+((3*(self.e2**3))/4))
        A6 = (35*(self.e2**3))/3972;
        
        si = self.a *(A0*fi - A2*sin(2*fi) + A4*sin(4*fi) - A6*sin(6*fi))
        dL = la - L0
        
        xgk = si + ((dL**2)/2)*N*sin(fi)*cos(fi)*(1+((dL**2)/12)*((cos(fi))**2)*(5-t**2+9*n2+4*(n2**2))+((dL**4)/360)*((cos(fi))**4)*(61-58*(t**2)+(t**2)+t**4+270*n2-330*n2*(t**2))) 
        ygk = dL*N*cos(fi)*(1+((dL**2)/6)*((cos(fi))**2)*(1-(t**2)+n2)+((dL**4)/120)*((cos(fi))**4)*(5-18*(t**2)+(t**4)+12*n2-58*n2*(t**2)))
        x2000=xgk*0.999923
        y2000=ygk*0.999923+(L0*180/pi/3)*1000000+500000
        
        return(round(x2000,6), round(y2000,6))
    
    def transformacja5(self, fi, la):
        """
        Transformacja współrzędnych do układu 1992 - transformacja stosowana na potrzeby wykonania map w skalach większych
        od 1:10 000. Odwzorowanie oparte na na odwzorowaniu Gaussa-Krugera w jednej strefie. Początkiem układu jest przecięcie
        południka 19 stE z obrazem równika. Prowadzi kolejno do wyznaczenia płaskich współrzędnych kartezjańsich (xgk,ygk) 
        w oparciu o współrzędne geodezyjne(fi, la), a następnie w oparciu o skalę (m0 = 0.9993) do wzynaczenia współrzędnych 
        w układzie 1992.

        Parameters
        ----------
        fi, la : FLOAT
            Współrzędne geodezyjne
        
        Returns
        -------
        x1992: FLOAT
            [metry] - pierwsza współrzędna
        y1992: FLOAT
            [metry] - druga współrzędna

        """
        fi = radians(fi)
        la = radians(la)
        L0 = radians(19)
        b2 = (self.a**2)*(1-self.e2)
        ep2 = ((self.a**2)-(b2))/(b2)
        t = tan(fi)
        n2 = ep2*((cos(fi))**2)
        N = (self.a)/sqrt(1-self.e2*sin(fi)**2)
        A0 = 1-(self.e2/4)-((3*(self.e2**2))/64)-((5*(self.e2**3))/256)
        A2 = (3/8)*(self.e2+((self.e2**2)/4)+(15*(self.e2**3)/128))
        A4 = (15/256)*((self.e2**2)+((3*(self.e2**3))/4))
        A6 = (35*(self.e2**3))/3972;
        
        si = self.a *(A0*fi - A2*sin(2*fi) + A4*sin(4*fi) - A6*sin(6*fi))
        dL = la - L0
        
        xgk = si + ((dL**2)/2)*N*sin(fi)*cos(fi)*(1+((dL**2)/12)*((cos(fi))**2)*(5-t**2+9*n2+4*(n2**2))+((dL**4)/360)*((cos(fi))**4)*(61-58*(t**2)+(t**2)+t**4+270*n2-330*n2*(t**2))) 
        ygk = dL*N*cos(fi)*(1+((dL**2)/6)*((cos(fi))**2)*(1-(t**2)+n2)+((dL**4)/120)*((cos(fi))**4)*(5-18*(t**2)+(t**4)+12*n2-58*n2*(t**2)))
        x1992 = xgk*0.9993-5300000
        y1992 = ygk*0.9993+500000
        return(round(x1992,6), round(y1992,6))
   
        
# Tutaj będą wywoływane funkcje oraz odczytywane i zapisywane pliki tekstowe:
if __name__ == "__main__":
    
    oblicz = '1'
    while oblicz == '1':
        # Utworzenie obiektu
        print('Elipsoidy do wyboru: \nwgs84 (1)\ngrs80 (2)')
        print('Wybierz numerek w nawiasie aby wykonać obliczenia dla odpowiedniej elipsoidy')
        wybrana_elips = input()
        if wybrana_elips == '1':
            geo = Transformacje(model = "wgs84")
        elif wybrana_elips == '2':
            geo = Transformacje(model = "grs80")
        else:
            print('Obsługiwane elipsoidy: wgs84 oraz grs80')
        
        
        print('Transformacje do wyboru: \n XYZ -> BLH (1) \n BLH -> XYZ (2) \n XYZ -> NEUp (3) \n BL -> 2000 (4) \n BL -> 1992 (5) \n')
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
                flh.append([fi, la, h])
            
            # Zapisanie wyników do pliku tekstowego
            with open('output_flh.txt', 'w') as plik:
                plik.write('Wyniki przedstawione w formacie: [fi, la, h] \n')
                for punkt in range(0, len(flh)):
                    plik.write(f'{flh[punkt]} \n')
    
        elif wybrana_transformacja == '2':
            # Dane XYZ z pliku tekstowego
            with open('input_blh.txt', 'r') as plik:
                wiersze = plik.readlines()
                punkty = [] # [[B1, L1, H1], ..., [Bn, Ln, Hn]]
                for i in range(0, len(wiersze)):
                    wspolrzedne_punkt = wiersze[i].split(',')
                    for blh in range(0, len(wspolrzedne_punkt)):
                        wspolrzedne_punkt[blh] = float(wspolrzedne_punkt[blh])
                    punkty.append(wspolrzedne_punkt)
                    
            # Przerzucenie wyników do listy xyz
            xyz = []
            for punkt in range(0,len(punkty)):
                x, y, z = geo.transformacja2(punkty[punkt][0], punkty[punkt][1], punkty[punkt][2])
                xyz.append([x, y, z])
            
            # Zapisanie wyników do pliku tekstowego
            with open('output_xyz.txt', 'w') as plik:
                plik.write('Wyniki przedstawione w formacie: [X, Y, Z] \n')
                for punkt in range(0, len(xyz)):
                    plik.write(f'{xyz[punkt]} \n')
                    
        elif wybrana_transformacja == '3':
            with open('input_xyzab.txt', 'r') as plik:
                wiersze = plik.readlines()
                punkty = [] # [[X1a, Y1a, Z1a, X1b, Y1b, Z1b], ..., [Xna, Yna, Zna, Xnb, Ynb, Znb]]
                for i in range(0, len(wiersze)):
                    wspolrzedne_punkt = wiersze[i].split(',')
                    for xyzab in range(0, len(wspolrzedne_punkt)):
                        wspolrzedne_punkt[xyzab] = float(wspolrzedne_punkt[xyzab])
                    punkty.append(wspolrzedne_punkt)
                    
            # Przerzucenie wyników do listy neu
            neu = []
            for punkt in range(0,len(punkty)):
                sab, alfaab, zab = geo.transformacja3(punkty[punkt][0], punkty[punkt][1], punkty[punkt][2], punkty[punkt][3], punkty[punkt][4], punkty[punkt][5])
                neu.append([sab, alfaab, zab])
            
            # Zapisanie wyników do pliku tekstowego
            with open('output_neu.txt', 'w') as plik:
                plik.write('Wyniki przedstawione w formacie: [sab, alfaab, zab] \n')
                for punkt in range(0, len(neu)):
                    plik.write(f'{neu[punkt]} \n')
        
        elif wybrana_transformacja == '4':
             #Dane fi, la, L0 z pliku tekstowego
            with open('input_flL0.txt', 'r') as plik:
                wiersze = plik.readlines()
                punkty = [] # [[f1, l1, L0{15/18/21/24}], ..., [xn, yn, L0{15/18/21/24}]]
                for i in range(0, len(wiersze)):
                    wspolrzedne_punkt = wiersze[i].split(',')
                    for flL0 in range(0, len(wspolrzedne_punkt)):
                        wspolrzedne_punkt[flL0] = float(wspolrzedne_punkt[flL0])
                    punkty.append(wspolrzedne_punkt)
                    
            # Przerzucenie wyników do listy xy2000
            xy00 = []
            for punkt in range(0,len(punkty)):
                x2000, y2000 = geo.transformacja4(punkty[punkt][0], punkty[punkt][1], punkty[punkt][2])
                xy00.append([x2000, y2000])
            
            # Zapisanie wyników do pliku tekstowego
            with open('output_xy2000.txt', 'w') as plik:
                plik.write('Wyniki przedstawione w formacie: [x2000, y2000] \n')
                for punkt in range(0, len(xy00)):
                    plik.write(f'{xy00[punkt]} \n')
            
           
        
        elif wybrana_transformacja == '5':
             #Dane fi, la z pliku tekstowego
            with open('input_fl.txt', 'r') as plik:
                wiersze = plik.readlines()
                punkty = [] # [[f1, l1], ..., [xn, yn]]
                for i in range(0, len(wiersze)):
                    wspolrzedne_punkt = wiersze[i].split(',')
                    for fl in range(0, len(wspolrzedne_punkt)):
                        wspolrzedne_punkt[fl] = float(wspolrzedne_punkt[fl])
                    punkty.append(wspolrzedne_punkt)
                    
            # Przerzucenie wyników do listy xy1992
            xy92 = []
            for punkt in range(0,len(punkty)):
                x1992, y1992 = geo.transformacja5(punkty[punkt][0], punkty[punkt][1])
                xy92.append([x1992, y1992])
            
            # Zapisanie wyników do pliku tekstowego
            with open('output_xy1992.txt', 'w') as plik:
                plik.write('Wyniki przedstawione w formacie: [x1992, y1992] \n')
                for punkt in range(0, len(xy92)):
                    plik.write(f'{xy92[punkt]} \n')
            
        print('Wciśnij (1), aby wykonać kolejną transformację, \nwciśnij (2), aby przerwać')
        oblicz = input()
    
    
                
            
        
        
        
    