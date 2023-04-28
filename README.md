# PROJEKT_1

# Zastosowanie i funkcjonalność programu skrypt.py
1 Program służy transformacjom współrzędnych wypisanych poniżej
	XYZ -> BLH (Wspołrzędne geocentryczne elipsoidalne -> współrzędne geodezyjne)
	BLH -> XYZ (Współrzędne geodezyjne -> współrzędne geocentryczne elipsoidalne)
	XYZ -> NEUp (Wspołrzędne geocentryczne elipsoidalne -> współrzędne topocentryczne)
	BL -> 2000 (Współrzędne geodezyjne -> współrzędne płaskie w układzie 2000)
	BL -> 1992 (Wspołrzędne geodezyjne -> współrzędne płaskie w układzie 1992)
	
2 Dodatkowo program wykonuje powyższe transformacje na elipsoidach wypisanych poniżej
	GRS 80
	WGS 84

# Wymagania środowiskowe
3 Program został przetestowany w języku Python w wersji 3.10 oraz 3.11 i na tych wersjach działa poprawnie

4 Do wykonania obliczeń wykorzystywane są następujące funkcje z biblioteki 'math'
	sqrt, sin, cos, atan, atan2, degrees, radians
	oraz następujące funkcje z biblioteki 'numpy'
	rad2deg, arctan2, arctan, array, transpose, arccos

# Wymagania systemowe
5 Program został przetestowany na systemie operacyjnym Windows 10 oraz 11 i na tej wersji działa poprawnie

# Wykorzystywanie programu do obliczeń
6 Dane wejściowe dla wybranej transformacji powinny być plikiem tekstowym o strukturze opisanej poniżej 
	| Nazwa pliku 		| Zawartość pliku 	| Transformacja 
	| input_xyz.txt 	| X,Y,Z				| XYZ -> BLH 
	| input_blh.txt 	| B,L,H				| BLH -> XYZ 
	| input_xyzab.txt	| Xa,Ya,Za,Xb,Yb,Zb	| XYZ -> NEUp
	| input_flL0.txt	| f,l,L0			| BL -> 2000 
	| input_fl.txt		| f,l 				| BL -> 1992 
	
7 Dane wyjściowe dla wybranej transformacji będą plikiem tekstowym o strukturze opisanej poniżej
	| Nazwa pliku 		| Zawartość pliku 	| Transformacja 
	| output_blh.txt 	| B,L,H				| XYZ -> BLH 
	| output_xyz.txt 	| X,Y,Z				| BLH -> XYZ 
	| output_neu.txt	| N,E,U,p			| XYZ -> NEUp
	| output_xy2000.txt	| X,Y				| BL -> 2000 
	| output_xy1992.txt	| X,Y				| BL -> 1992 
	
8 Lokalizacja danych wejściowych i wyjściowych jest katalogiem, w którym mamy zainstalowanego Pythona

9 Przykład użycia
	> Chcemy użyć programu do transformacji współrzędnych XYZ -> BLH
	> Przygotowujemy plik tekstowy o nazwie input_xyz.txt 
	> Sprawdzamy czy zawartość pliku zawiera współrzędne XYZ oddzielone przecinkami
	> Umieszczamy plik w katalogu z zainstalowanym Pythonem
	> Uruchamiamy Command Line
	> Wpisujemy: python "ścieżka do programu"
	> Program przedstawi nam dostępne elipsoidy - należy wybrać jedną z nich zgodnie z wyświetlaną instrukcją
	> Następnie program przedstawi nam dostępne transformacje - postępujemy tak jak w kroku powyżej
	> Plik tekstowy został utworzony w katalogu z zainstalowanym Pythonem

# Znane błędy i nietypowe zachowania programu
10 Struktura plików wyjściowych
Program zapisuje pliki w formie list - tzn są widoczne nawiasy kwadratowe w plikach wynikowych. Jest to efektem iterowania po punktach, a nie po współrzędnych, w trakcie zapisywania pliku. 
Zdecydowaliśmy się na takie uproszczenie, ze względu na estetykę kodu - wygląda schludniej, jest mniej tekstu i pętli. Drugim powodem była oszczędność czasu.

11 Nazwa pliku wyjściowego oraz ścieżka dostępu
Program odczytuje pliki tekstowe z katalogu z zainstalowanym Pythonem. Nie wpływa to w żaden sposób na wyniki obliczeń, 
lecz idealnie byłoby, aby użytkownik mógł wpisać ścieżkę dostępu oraz nazwę pliku tesktowego, w którym przechowuje współrzędne. W tym przypadku, motywacją była jedynie oszczędność czasu.

