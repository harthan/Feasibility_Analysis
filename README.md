# Analiza chłonności działki inwestycyjnej | Feasibility analysis of site

Zastanawiałeś się kiedyś, ile powierzchni użytkowej mieszkań lub budynków użytkowych można uzyskać z konkretnego terenu? Mój program, "Analiza chłonności inwestycyjnej gruntu", odpowiada na to pytanie.
Program jest napisany w języku polskim bo póki co jest skierowany głównie do polskich użytkowników, umiejąch przeczytać i wpisać do programu parametry z miejscowych planów zagospodarowania przestrzennego.

Have you ever wondered how much floor space for flats or commercial buildings can be obtained from a particular site? My programme, 'Land Investment Absorption Analysis', answers this question.
The programme is written in Polish, as it is primarily aimed at Polish users who are able to read and enter parameters from local zoning plans into the programme.

## Spis treści | Table of Contents

- [Analiza chłonności działki inwestycyjnej | Feasibility analysis of site](#analiza-chłonności-działki-inwestycyjnej--feasibility-analysis-of-site)
  - [Spis treści | Table of Contents](#spis-treści--table-of-contents)
  - [Podstawowe informacje General Information](#podstawowe-informacje-general-information)
  - [Technologies Used](#technologies-used)
  - [Features](#features)
  - [Project Status](#project-status)
  - [Room for Improvement](#room-for-improvement)
  - [Contact](#contact)
<!-- * [License](#license) -->

## Podstawowe informacje General Information

Zazwyczaj taka analiza jest wykonywana przez doświadczonego architekta, który analizuje działkę zawsze wg podobnego schematu:
:::image type="complex" source="./assets/full_analyse.jpg" alt-text="algorithm for full analys":::
   Algorytm Analizy opiera się na 3 podstawowych krokach: sprawdzenie na jakim terenie dozwolona jest zabudowa po wykonaniu analizy przesłaniania i zacieniania istniejących budynków, wyliczenie parametrów z miejscowego planu zagospodarowania przestrzennego lub warunków zabudowy oraz analiza przesłaniania i zacieniania dla parterów projektowanych budynków.
:::image-end:::

Algorytm Analizy opiera się na 3 podstawowych krokach i operacjach pomiędzy nimi. Udostępniony moduł jest drugim z nich. To część większego projektu, nad którym trwają prace. Obliczona powierzchnia wg tego programu może być tylko pomniejszona przez dwa pozostałe moduły, nie ma możliwości aby wzrosła.

Moduł ten oprócz wyliczenia maksymalnych powierzchni całkowitych na podstawie współczynników podanych  prawie miejscowym, sprawdza dwa inne krytyczne parametry, które bardzo często ograniczają inwestycję. Są to:

* Ilość powierzchni biologicznie czynnej
* ilość wymaganych miejsc postojowych w przeliczeniu na metry kwadratowe i ilość poziomów parkingów podziemnych.

Moduł został wykonany w oparciu o moje piętnastoletnie doswiadczenie w projektowaniu budynków o znacznej kubaturze (mieszkaniówka do 30000 PUM, biurowce do 50000 GLA). Przez ostatnie lata pracy jako architekt, zajmowałam się analizowaniem działek inwstycyjnych i marzyłam o programie automatyzującym tą pracę. W wyliczeniach wykorzystałam wskaźniki do których doszłam po wielu latach analiz.

Jest to mój pierwszy samodzielnie napisany program (nie licząc wielu ćwiczeń i tutaoriali).
Dzięki niemu nabrałam biegłości w podstawowych komendach i pętlach w języku python. Oprócz napisania przydatnego narzędzia to właśnie chęć nauki i praktyki w programowaniu było moją główną motywację aby napisać ten program.

## Technologies Used

* Python - version 3.11.2
* Pandas - version 1.5.3
* Matplotlib - version 3.6.2

## Features

List the ready features here:

* Sprawdzenie czy powierzchnia biologicznie czynna mieści się na działce przy wykorzstaniu maksymalnych wskaźników dotyczących zabudowy.
* Sprawdzenie czy przy podanym przez użytkownika średnim metrażu mieszkania zmieszczą się miejsca postojowe. W przypadku jakby się nie mieściły, podanie minimalnego średniego metrażu mieszkania, który może być obsłużony komunikacyjnie na tej działce (im mniejsze mieszkania, tym ich więcej i wymagają większej ilości miejsc postojowych.)
* Wyliczenie ile poziomów parkingu podziemnego będzie potrzebne
* określenie czy dla podanej inwestycji będzie potrzebna decyzja środowiskowa

## Project Status

Project is: in progress

## Room for Improvement

Include areas you believe need improvement / could be improved. Also add TODOs for future development.

To do:

* Połączyć moduł nr. 2 z dwoma pozostałymi nad którymi trwają jeszcze prace.
* Sprawdzenie obliczonych parametrów na rysunku w autocadzie i wygenerowanie gotowej analizy. Część ta jest możliwa do wykonania ale wymaga odemnie sporo nauki (biblioteka pyautocad). Generowanie rysunku opierałoby się na danych wynikających z mojego doświadczenia architektonicznego (szerokość traktu stała lecz inna dla obiektów biurowych a inna dla mieszkalnych, odległości ppoż i droga poż. itd.)

## Contact

Created by [@AldonaKret] - feel free to contact me!

<!-- Optional -->
<!-- ## License -->
<!-- This project is open source and available under the [... License](). -->

<!-- You don't have to include all sections - just the one's relevant to your project -->
