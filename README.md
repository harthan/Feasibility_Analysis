![screen or GIF of your app](./assets/logo.jpg)

<!-- Nie powinno się mieszać dwóch języków w dokumentacji. 
Albo trzymamy się angielskiego albo polskiego.
Dalsza część dokumentacji jest po polsku. -->
# *Feasibility Analysis of Site*

*Have you ever wondered how much floor space for flats or commercial buildings can be obtained from a particular site? My programme, 'Land Investment Absorption Analysis', answers this question.
The programme is written in Polish, as it is primarily aimed at Polish users who are able to read and enter parameters from local zoning plans into the programme.*

*Who knows, maybe in the future I will be able to develop it in such a way that the programme itself will download the parameters from the local plans and recognise the size of the land, so that knowledge of the Polish language will no longer be necessary to estimate the absorption capacity of the plot and the programme will make sense in other language versions.*

## Analiza Chłonności Działki Inwestycyjnej

Zastanawiałeś się kiedyś, ile powierzchni użytkowej mieszkań lub budynków użytkowych można uzyskać z konkretnego terenu? Mój program, "Analiza chłonności inwestycyjnej gruntu", odpowiada na to pytanie.
<!-- nie informuj o tym, dlaczego jest w języku polskim. 
Powiedz lepiej, że produkt jest specjalnie dopiasowany do polskiego odbiorcy -->
Program jest napisany w języku polskim bo póki co jest skierowany głównie do polskich użytkowników, umiejąch przeczytać i wpisać do programu parametry z miejscowych planów zagospodarowania przestrzennego.

Kto wie moze uda mi się rozwinąć go w przyszłości tak aby program sam ściągał parametry z miejscowych planów i rozpoznawał wielkość terenów, wtedy już nie będzie potrzebna znajomość języka polskiego aby oszacować chłonność działki i program będzie miał sens w innych wersjach językowych.

## Table of Contents | Spis Treści

- [*Feasibility Analysis of Site*](#feasibility-analysis-of-site)
  - [Analiza Chłonności Działki Inwestycyjnej](#analiza-chłonności-działki-inwestycyjnej)
  - [Table of Contents | Spis Treści](#table-of-contents--spis-treści)
  - [General Information | Podstawowe Informacje](#general-information--podstawowe-informacje)
  - [Technologies Used | Użyte technologie](#technologies-used--użyte-technologie)
  - [Features | Funkcje](#features--funkcje)
  - [Usage | Sposób Użycia](#usage--sposób-użycia)
  - [Project Status | Status Projektu](#project-status--status-projektu)
  - [Room for Improvement | Planowane Aktualizacje](#room-for-improvement--planowane-aktualizacje)
  - [Contact | Kontakt](#contact--kontakt)
<!-- * [License](#license) -->

## General Information | Podstawowe Informacje

Zazwyczaj taka analiza jest wykonywana przez doświadczonego architekta, który analizuje działkę zawsze wg podobnego schematu:

![screen or GIF of your app](./assets/full_analyse.jpg)

<!-- takie rzeczy pisz w komentarzach w kodzie. Lepiej się czyta przemyślenia przechodząc przez kod :) -->
Algorytm Analizy opiera się na 3 podstawowych krokach i operacjach pomiędzy nimi. Udostępniony moduł jest drugim z nich. To część większego projektu, nad którym trwają prace. Obliczona powierzchnia wg tego programu może być tylko pomniejszona przez dwa pozostałe moduły, nie ma możliwości aby wzrosła.

Moduł ten oprócz wyliczenia maksymalnych powierzchni całkowitych na podstawie współczynników podanych  prawie miejscowym, sprawdza dwa inne krytyczne parametry, które bardzo często ograniczają inwestycję. Są to:


- Ilość powierzchni biologicznie czynnej
- ilość wymaganych miejsc postojowych w przeliczeniu na metry kwadratowe i ilość poziomów parkingów podziemnych.

Moduł został wykonany w oparciu o moje piętnastoletnie doswiadczenie w projektowaniu budynków o znacznej kubaturze. Przez ostatnie lata pracy jako architekt, zajmowałam się analizowaniem działek inwstycyjnych i marzyłam o programie automatyzującym tą pracę. W wyliczeniach wykorzystałam wskaźniki do których doszłam po wielu latach analiz.

## Technologies Used | Użyte technologie

<!-- Polecam dopasować się pod wersję minor a nie bugfix tzn - Python 3.11 zamiast 3.11.2 
Pamiętaj że za niedługo pojawi się kolejna łatka i będziesz musiała poprawiać dokumentację.
Osobiście uważam, że jeżeli chcesz taki program wykorzystać komercyjnie to musisz podnosić też
wersję minor. -->
- Python - version 3.11.2
<!-- tutaj to samo -->
- Pandas - version 1.5.3
- Tabulate - 0.9.0

## Features | Funkcje

<!-- Nie powinno się mieszać dwóch języków w dokumentacji. 
Albo trzymamy się angielskiego albo polskiego :) -->
List the ready features here:

- Obliczenie ile powierzchni użytkowej uda się uzyskać na badanej działce
- Sprawdzenie czy powierzchnia biologicznie czynna mieści się na działce przy wykorzstaniu maksymalnych wskaźników dotyczących zabudowy.
- Sprawdzenie czy przy podanym przez użytkownika średnim metrażu mieszkania zmieszczą się miejsca postojowe. W przypadku jakby się nie mieściły, podanie minimalnego średniego metrażu mieszkania, który może być obsłużony komunikacyjnie na tej działce (im mniejsze mieszkania, tym ich więcej i wymagają większej ilości miejsc postojowych.)
- Wyliczenie ile poziomów parkingu podziemnego będzie potrzebne
- określenie czy dla podanej inwestycji będzie potrzebna decyzja środowiskowa

## Usage | Sposób Użycia

użytkownik wprowadza dane z Miejscowego Planu Zagospodarowania Przestrzennego oraz własne preferencje.

![screen or GIF of your app](./assets/Zrzut_ekranu_dane_wprowadzane.jpg)

Następnie uzyskuje wyliczone paramentry w postaci tabeli:

![screen or GIF of your app](./assets/Zrzut_ekranu_wynik.jpg)

## Project Status | Status Projektu

<!-- Wykorzystaj WIP (Work in Progress).
W ten sposób na git oznaczamy rzeczy do zrobienia. -->
IN PROGRESS!!!

<!-- Release Notes | Plan Rozwoju 
Powyżej branżowe nazwy po angielsku i polsku -->
## Room for Improvement | Planowane Aktualizacje

planowane prace nad tym modułem:
- wprowadzenie możliwości podziału terenu na różne funkcje
- oprócz tabeli z wynikiem powinna pojawić się informacja dlaczego wskaźniki zostały ograniczone

planowane prace nad całym programem:
- Połączyć moduł nr. 2 z dwoma pozostałymi nad którymi trwają jeszcze prace.
- Sprawdzenie obliczonych parametrów na rysunku w autocadzie i wygenerowanie gotowej analizy.

## Contact | Kontakt

Created by [@AldonaKret] - feel free to contact me!


