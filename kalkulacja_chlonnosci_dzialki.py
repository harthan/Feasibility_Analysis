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

site_size = 6380
base = 6380
base_underground = 5735
building_factor = 35
intensity_factor = 2.8
building_height = 25
green_area = 50 / 100 * base
green_area_100 = 0 / 100 * base
parking_place_M = 1.2
parking_place_B = 0
destiny = "M"
goal_flats_size = 45

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
        BA = base * building_factor / 100
    if intensity_factor != 0:
        BA = intensity_factor * base // count_floors()
        # BA = powierzchnia zabudowy
    else:
        pass
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

# określenie ilości kondygnacji na podstawie wysokości lub intensywności
# zabudowy oraz biorąc pod uwagę fakt czy jest to budynek usługowy czy
# mieszkalny.


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


def count_flats():
    global number_of_flats

    number_of_flats = calculate_PUM() // goal_flats_size
    return int(number_of_flats)


def calculate_GLA():
    GLA = total_area() * 0.89
    return float(GLA)


def count_parking():
    global number_of_parkings

    number_of_parkings = 0
    if 'M' in destiny:
        number_of_parkings = count_flats() * parking_place_M
    elif 'B' in destiny:
        number_of_parkings = ((0.8 * calculate_GLA) / 100 * parking_place_B) + 1
    print("ilość parkingów =", number_of_parkings)
    return number_of_parkings


def calculate_size_of_underground_parking():
    global underground

    underground = (count_parking() - 5) * 35
    print("underground = ", underground)
    return underground


def check_capability_for_underground_parking():
    global base_underground
    global area_parkings_on_the_ground
    global number_of_underground_floors

    if base - base_underground < green_area_100:
        base_underground = base - green_area_100

    X = base_underground - underground
# X=potrzebny dodatkowa powierzchnia na poziomie terenu
    area_parkings_on_the_ground = 5

    if X < 0:
        X = base_underground - (underground/2)
        print('muszą być 2 kondygnacje podziemne')
        number_of_underground_floors = 2
        base_underground = underground/2

        if X >= 0:
            area_parkings_on_the_ground = 5

        if X < 0:
            area_parkings_on_the_ground = 62.5 + (abs(X) / 35) * 12.5

    if X >= 0:
        number_of_underground_floors = 1
        area_parkings_on_the_ground = 5


    print("area_parkings_on_the_ground", area_parkings_on_the_ground)
    print('pow. zabudowy gaarażu =', base_underground)
    return area_parkings_on_the_ground, base_underground, number_of_underground_floors

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


        print(f"""
        aby zmnieściła się cała wymagana powierzchnia biologicznie czynna,
        nastąpiło zmniejszenie ilości miejsc postojowych o
        {number_of_parkings - new_number_of_parkings}""")
        if "M" in destiny:
            print(f""" jeżeli chcesz utrzymać średnią wielkość mieszkania
             = {goal_flats_size} to zmniejszy się PUM o {(number_of_parkings - new_number_of_parkings)//1.2 * goal_flats_size}""")


    print("base_underground = ", base_underground)


    # jeżeli brakuje pow. biol czynnej musimy ją zwiększyć poprzez:
    # zmniejszenie parkingu podziemnego (underground/2) tak aby po za jego granicami była powierzchnia biol. czynna w 100% a nie 50%
    # musimy uzyskać conajmniej równość green_area = received_area.
    # zmniejszając ilość miejsc postojowych o 1 zmniejszamy powierzchnię zabudowy dwupoziomowego parkingu o 17.5m2


def revision():
    global base_underground
    global new_number_of_parkings
    global received_green

    X = int(base_underground // 17.5)
    for i in range(X):

        base_underground = base_underground - 17.5
        # received_green = 0.8 * base - 0.375 * base_underground - area_parkings_on_the_ground
        # received_green =  0.8 * base - 0.375 * (base_underground - 17.5)- area_parkings_on_the_ground + (goal_flats_size / 1.2 / floors_amount)
        # received_green =  0.8 * base - (0.375 * base_underground) - (0.375 * 17.5) - area_parkings_on_the_ground + (goal_flats_size / 1.2 / floors_amount)
        received_green = received_green + 6.56 + ((PUM/((base_underground/17.5)+(area_parkings_on_the_ground/12))*1.2) / parking_place_M / floors_amount)

        if received_green >= green_area:
            print(i)
            break
        else:
            continue

    print(base_underground, "= base_underground")

    new_number_of_parkings = base_underground // 17.5 + area_parkings_on_the_ground// 12
    print('number of parkings =', new_number_of_parkings)
    return base_underground, number_of_parkings, new_number_of_parkings

building_area()
total_area()
count_floors()

if building_factor == 0:
    BA = total_area() // floors_amount

if "M" in destiny:
    calculate_PUM()
    count_flats()

if "B" in destiny:
    calculate_GLA()

count_parking()
calculate_size_of_underground_parking()
check_capability_for_underground_parking()
check_bioactiv_area()
revision()
print (PUM/((base_underground/17.5)+(area_parkings_on_the_ground/12))*1.2)



table_PUM = [
['powierzchnia działki', ' ', site_size, ' '],
['współczynnik zabudowy -> powierzchnia zabudowy', str(building_factor) +'%',  str(BA)+'m2', str(BA/site_size)+'%'],
['intensywność zabudowy -> powierzchnia całkowita', str(intensity_factor), str(TA)+'m2', str(TA/site_size)],
['powierzchnia biologicznie czynna', str(green_area)+'%', str(round(received_green, 2))+'m2', ' '],
['wymagana zieleń na gruncie', str(green_area_100)+'%', str(green_area_100 *100/base)+'%', str(green_area_100)+'%'],
['wysokość zabudowy', str(building_height)+'m', str(floors_amount)+' kondygnacji', str(building_height)+'m'],
['ilość mieszkań', ' ', int(new_number_of_parkings / parking_place_M), ' '],
['średnia wielkość mieszkania', ' ', str(round((PUM/(new_number_of_parkings/ parking_place_M )),2)) + ' lub większe', ' '],
['ilość miejsc postojowych', str(parking_place_M) + ' na mieszkanie', round(new_number_of_parkings, 2), str(parking_place_M) + ' na mieszkanie'],
['ilość kondygnacji podziemnych', '', number_of_underground_floors, ''],
['współczynnik do liczenia PUM', ' ', 0.69, ' '],
['PUM', '', PUM, '']]

df_table_PUM = pd.DataFrame(table_PUM)
df_table_PUM.columns = ['nazwa parametru', 'wymóg MPZT', 'osiągięte parametry', 'osiągnięte wskaźniki']

zaokroglona = df_table_PUM.round(2)

print(tabulate((df_table_PUM), stralign = "center", headers = [' ', 'nazwa parametru', 'wymóg MPZT', 'osiągięte parametry', 'osiągnięte wskaźniki'], tablefmt="presto"))