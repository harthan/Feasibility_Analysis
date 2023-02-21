import pandas as pd
import matplotlib.pyplot as plt
from tabulate import tabulate


# Poniżej umieszczasz swój kod
# Od tego momentu wszystkie liczby zmiennoprzecinkowe zostaną zaokrąglone do
# dwóch miejsc po przecinku

# print('Bardzo proszę podać następujące dane z MPZP,
# jeśli któraś z danych nie została podana, proszę wpisać 0')

# site_size = float(input("Jaka jest powierzchnia całej działki"))

# base = float(input("Jaka jest powierzchnia terenu na dzialce,
# który przeznaczony jest w MPZP pod zabudowę"))
# base_underground = float(input("jaka jest powierzchnia terenu na dzialce,
# pod którym może być podziemie (wewnątrz nieprzekraczalnych linii zabudowy"))
# building_factor = int(input("ile procent wynosi współczynnik zabudowy"))
# intensity_factor = float(input("jaki jest współczynnik zabudowy"))
# building_height = float(input("jaka jest wysokość budynku"))
# green_area = int(input("ile procent wynosi współczynnik powierzchni
# biologicznie-czynnej")) * base / 100
# green_area_100 = int(input("ile procent wynosi współczynnik powierzchni
# biologicznie-czynnej bezpośrednio na gruncie")) * base / 100
# parking_place_M = float(input("ile jest wymaganych miesjc
# postojowych na mieszkanie"))
# parking_place_B = float(input("ile jest wymaganych miesjc
# postojowych na 100m2 powierzchni"))
# destiny = input("jeśli ma to być funkcja mieszkalna wpisz M,
# jeśli mają to być biura wpisz B")
# goal_flats_size = int(input("ile ma wynosić średnia wilkości mieszkania"))
# number_of_underground_floors = 2int(input("ile chcesz wybudować poziomów podziemnych"))

site_size = 6380
base = 6380
base_underground = 5735
building_factor = 35
intensity_factor = 2.8
building_height = 25
green_area = 50 / 100 * base
green_area_100 = 0 / 100 * base
parking_place_M = 1.2
parking_place_B = 30
destiny = "B"
number_of_underground_floors = 2

if 'M' in destiny:
    h = 3
if 'B' in destiny:
    h = 3.5
if "B" not in destiny and 'M' not in destiny:
    print('źle określona funkcja, nie da się wykonać analizy')
    # trzeba wrócić do wypełnienia tabeli na nowo


def building_area():   # Building_area = wyliczenie powierzchni zabudowy
    global BA

    if building_factor != 0:
        BAB = base * building_factor / 100
    if intensity_factor != 0:
        BAI = intensity_factor * base // count_floors()
        # BA = powierzchnia zabudowy
    else:
        pass
    BA = min(BAB, BAI)
    return BA


def total_area():   # total_area = wyliczenie powierzchni całkowitej
    global TA

    if building_factor != 0:
        TAB = building_area() * (building_height // h)
# TAB = powierzchnia całkowita wyliczona na podstawie współczynnika zabudowy
    if intensity_factor != 0:
        TAI = base * intensity_factor
# TAI = powierzchnia całkowita wyliczona na podstawie intensywności  zabudowy
    else:
        pass
    TA = min(TAB, TAI)
    return TA

def count_floors():
    global floors_amount

    if building_height != 0:
        floors_amount = building_height // h
    if building_height == 0:
        floors_amount = (intensity_factor * base) // h
    return floors_amount


def calculate_PUM():
    global PUM

    PUM = total_area() * 0.69
    return float(PUM)

def calculate_GLA():
    global GLA
    GLA = total_area() * 0.89
    return float(GLA)

def check_capability_for_underground_parking():
    global base_underground
    global area_parkings_on_the_ground
    global number_of_underground_floors
    global number_of_parkings

    if base - base_underground < green_area_100:
        base_underground = base - green_area_100

    number_of_parkings_underground = (base_underground * number_of_underground_floors) / 35
    number_of_parkings = number_of_parkings_underground // 0.96
    number_of_parkings_on_the_ground = 0.04 * number_of_parkings
    area_parkings_on_the_ground = 12 * number_of_parkings_on_the_ground

    return area_parkings_on_the_ground, base_underground, number_of_underground_floors, number_of_parkings

    # sprawdzenie czy zmieścimy na działce powierzchnie biologicznie czynną:
    #   1. Najpierw zakładamy że 85% powierzchni dachów przeznaczmy na pow.
    #   biol czynną(liczoną jako 50%)
    #   2. potem dodajemy teren, który nie jest nad garażem i zakładamy że
    #   w 80% przeznaczamy go na zieleń
    #   3. potem dodajemy teren nad garażem który w 85% przeznaczony jest
    #   na zieleń (liczoną jako 50%)
    #   4. potem odejmujemy teren parkingów na powierzchni działki.
    #   received_green =  building_area() * 0.85 * 0.5 + (base - base_underground) * 0.8 + (base_underground - building_area()) * 0,85 * 0,5 - area_parkings_on_the_ground =
    #   = 0,425 * building_area() + 0,8 * base - 0,8 * base_underground + 0,425 * base_underground - 0,425 * building_area() - area_parkings_on_the_ground =
    #   = 0,8 * base - 0,375 * base_underground - area_parkings_on_the_ground


def check_bioactiv_area():
    global received_green

    received_green = 0.8 * base - 0.375 * base_underground - area_parkings_on_the_ground
    print("received_green = ", received_green)
    print("green_area = ", green_area)
    if (green_area) - received_green >= 0:
        if green_area - received_green < 0.1 * green_area:
            print("""
            masz wystarczająco powierzchni biologicznie czynnej,
            jednak jej wartość jest graniczna, konieczna jest
            weryfikacja manualna na rysunku""")
        else: print("wymagana powierzchnia biologicznie czynna zmieści się na działce")

    else:
        print("""
        masz za mało powierzchni biologicznie czynnej,
        nastąpi korekta parametrów.""")

    print("base_underground = ", base_underground)


    # jeżeli brakuje pow. biol czynnej musimy ją zwiększyć poprzez:
    # zmniejszenie parkingu podziemnego (underground/2) tak aby po za jego granicami była powierzchnia biol. czynna w 100% a nie 50%
    # musimy uzyskać conajmniej równość green_area = received_area.
    # zmniejszając ilość miejsc postojowych o 1 zmniejszamy powierzchnię zabudowy dwupoziomowego parkingu o 17.5m2


def revision():
    global base_underground
    global received_green
    global new_number_of_parkings

    X = int(base_underground // 17.5)
    for i in range(X):

        # base_underground = base_underground - 17.5
        # received_green = 0.8 * base - 0.375 * base_underground - area_parkings_on_the_ground
        # received_green =  0.8 * base - 0.375 * (base_underground - 17.5)- area_parkings_on_the_ground + (goal_flats_size / 1.2 / floors_amount)
        # received_green =  0.8 * base - (0.375 * base_underground) + (0.375 * 17.5) - area_parkings_on_the_ground + (goal_flats_size / 1.2 / floors_amount)
        if 'M' in destiny:
            received_green = received_green + 6.56 + (PUM/((base_underground/17.5)+(area_parkings_on_the_ground/12))/ floors_amount)
        if 'B' in destiny:
            received_green = received_green + 6.56 + 1000/ 30 / floors_amount

        if received_green >= green_area:
            base_underground = base_underground - (i * 17.5)
            print(i)
            break
        else:
            continue

    print(base_underground, "= base_underground")

    new_number_of_parkings = int(base_underground // 17.5 + area_parkings_on_the_ground// 12)
    print('number of parkings =', new_number_of_parkings)
    return base_underground, number_of_parkings, new_number_of_parkings



building_area()
total_area()
count_floors()

if building_factor == 0:
    BA = total_area() // floors_amount

if "M" in destiny:
    calculate_PUM()

if "B" in destiny:
    calculate_GLA()



check_capability_for_underground_parking()
check_bioactiv_area()
revision()



if 'M' in destiny:
    table = [
    ['powierzchnia działki', ' ', str(site_size) + 'm2', ' '],
    ['współczynnik zabudowy -> powierzchnia zabudowy', str(building_factor) +'%',  str(BA)+'m2', str(BA/site_size*100)+'%'],
    ['intensywność zabudowy -> powierzchnia całkowita', str(intensity_factor), str(TA)+'m2', str(TA/site_size)],
    ['powierzchnia biologicznie czynna', str(green_area * 100 / base)+'%', str(round(received_green, 2))+'m2', str(round((received_green / base * 100), 2)) + '%'],
    ['wymagana zieleń na gruncie', str(green_area_100 * 100 / base) +'%', str(green_area_100) + 'm2', str(round((green_area_100 / base * 100), 2)) +'%'],
    ['wysokość zabudowy', str(building_height)+'m', str(floors_amount)+' kondygnacji', str(building_height)+'m'],
    ['ilość mieszkań', ' ', int(new_number_of_parkings / parking_place_M), ' '],
    ['średnia wielkość mieszkania', ' ', str(round((PUM/(new_number_of_parkings/ parking_place_M )),2)) + 'm2 lub większe', ' '],
    ['ilość miejsc postojowych', str(parking_place_M) + ' na mieszkanie', round(new_number_of_parkings, 2), str(parking_place_M) + ' na mieszkanie'],
    ['ilość kondygnacji podziemnych', '', number_of_underground_floors, ''],
    ['współczynnik do liczenia PUM', ' ', 0.69, ' '],
    ['PUM', '',str(PUM) + 'm2', '']]


elif 'B' in destiny:
    table = [
    ['powierzchnia działki', ' ', str(site_size) + 'm2', ' '],
    ['współczynnik zabudowy -> powierzchnia zabudowy', str(building_factor) +'%',  str(BA)+'m2', str(BA/site_size*100)+'%'],
    ['intensywność zabudowy -> powierzchnia całkowita', str(intensity_factor), str(TA)+'m2', str(TA/site_size)],
    ['powierzchnia biologicznie czynna', str(green_area * 100 / base)+'%', str(round(received_green, 2))+'m2', str(round((received_green / base * 100), 2)) + '%'],
    ['wymagana zieleń na gruncie', str(green_area_100 * 100 / base) +'%', str(green_area_100) + 'm2', str(round((green_area_100 / base * 100), 2)) +'%'],
    ['wysokość zabudowy', str(building_height)+'m', str(floors_amount)+' kondygnacji', str(building_height)+'m'],
    ['ilość miejsc postojowych', str(parking_place_B) + ' na 1000m2 pow. użytkowej', new_number_of_parkings, str(parking_place_B) + ' na 1000m2 pow. użytkowej'],
    ['ilość kondygnacji podziemnych', '', number_of_underground_floors, ''],
    ['powierzchnia użytkowa obsłużona przez parkingi', '', str(round((new_number_of_parkings * 1000 / parking_place_B), 2))+'m2', ' '],
    ['współczynnik do liczenia GLA', ' ', 0.69, ' '],
    ['GLA', '', str(GLA) + 'm2', '']]

df_table= pd.DataFrame(table)
df_table.columns = ['nazwa parametru', 'wymóg MPZT', 'osiągięte parametry', 'osiągnięte wskaźniki']

print(tabulate((df_table), stralign = "center", headers = [' ', 'nazwa parametru', 'wymóg MPZT', 'osiągięte parametry', 'osiągnięte wskaźniki'], tablefmt="presto"))
