from tabulate import tabulate, SEPARATING_LINE

fields = [
    {"label": "Powierzchnia całej działki", "name": "site_size", "unit": "m2"},
    {"label": "Powierzchnia terenu pod zabudowę", "name": "base", "unit": "m2"},
    {"label": "Powierzchnia terenu pod którym może być podziemie", "name": "underground_area", "unit": "m2"},
    {"label": "Współczynnik zabudowy", "name": "building_factor", "unit": "%"},
    {"label": "Współczynnik intensywności zabudowy", "name": "intensity_factor", "unit": ""},
    {"label": "Wysokość budynku", "name": "building_height", "unit": "m"},
    {"label": "Współczynnik powierzchni biologicznie-czynnej", "name": "green_area_percentage", "unit": "%"},
    {"label": "Współczynnik powierzchni biologicznie-czynnej bezpośrednio na gruncie", "name": "green_area_100_percentage", "unit": "%"},
    {"label": "Liczba wymaganych miejsc postojowych na mieszkanie", "name": "parking_place_M", "unit": ""},
    {"label": "Liczba wymaganych miejsc postojowych na 1000m2 powierzchni usługowej", "name": "parking_place_B", "unit": ""},
    {"label": "Liczba kondygnacji podziemnych", "name":  "number_of_underground_floors", "unit": ""},
    {"label": "Funkcja (mieszkalna lub biurowa)", "name": "destiny", "unit": ""}]

# Tworzymy słownik, w którym kluczami są nazwy pól, a wartościami są wprowadzone przez użytkownika wartości.
data = {}

for field in fields:
    prompt = f"{field['label']} [{field['unit']}]: "
    value = input(prompt)
    data[field['name']] = value

# Tworzymy listę, która będzie składać się z wierszy tabeli, a następnie wyświetlamy tabelę za pomocą funkcji `tabulate`.
table_rows = []
for field in fields:
    label = field['label']
    value = data.get(field['name'], "0")
    unit = field['unit']
    table_rows.append([label, value, unit])

print(tabulate(table_rows, headers=["Parametr", "Wartość", "Jednostka"]),"\n")
# konwersja danych tekstowych na liczbowe

site_size = float(table_rows[0][1])
base = float(table_rows[1][1])
base_underground = float(table_rows[2][1])
building_factor = float(table_rows[3][1])
intensity_factor = float(table_rows[4][1])
building_height = float(table_rows[5][1])
green_area_percentage = float(table_rows[6][1])
green_area = green_area_percentage * base / 100
green_area_100_percentage = float(table_rows[7][1])
green_area_100 = green_area_100_percentage * base / 100
parking_place_M = float(table_rows[8][1])
parking_place_B = float(table_rows[9][1])
number_of_underground_floors = float(table_rows[10][1])
destiny = table_rows[11][1]

# PRZYKŁADOWE DANE TESTOWE:
# site_size = 6380
# base = 6380
# base_underground = 5735
# building_factor = 35
# intensity_factor = 2.8
# building_height = 25
# green_area = 50 / 100 * base
# green_area_100 = 0 / 100 * base
# parking_place_M = 1.2
# parking_place_B = 30
# destiny = "B"
# number_of_underground_floors = 2

if 'M' in destiny:
    h = 3
if 'B' in destiny:
    h = 3.5

def building_area():   # Building_area = wyliczenie powierzchni zabudowy
    global BA

    if building_factor != 0:
        BAB = base * building_factor / 100
    if intensity_factor != 0:
        BAI = intensity_factor * base // count_floors()
        # BA = powierzchnia zabudowy
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

    if base - base_underground < green_area_100:
        base_underground = base - green_area_100

    print('base_underground =', base_underground)
    return base_underground,

# przyjmujemy że 4% wszystkich parkingów zajmują parkingi naziemne.
    # 1 miejsce parkingowe pod ziemią potrzebuje 35m2
    # 1 miejsce parkingowe na ziemi liczymy jako 12m,
    # bo przestrzeń manewrowa wliczona jest już w pomniejszenie współczynnika
    # biologicznie czynnego i zazwyczaj wykorzystuje drogę dojazdową do garażu lub ppoż.

def calculate_area_parkings_on_the_ground():
    global area_parkings_on_the_ground

    area_parkings_on_the_ground = 0.014257 * (base_underground * number_of_underground_floors)
    print('area_parkings_on_the_ground =', area_parkings_on_the_ground)
    return area_parkings_on_the_ground

# Sprawdzenie czy zmieścimy na działce powierzchnie biologicznie czynną:
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
    if green_area - received_green > 0:
        print("""
        wymagana powierzchnia biologicznie czynna nie zmieści się na działce,
        nastąpi zmniejszenie parkingu podziemnego""")

    else:
        print("""
        masz wystarczająco powierzchni biologicznie czynnej""")

    print("base_underground = ", base_underground)

    # jeżeli brakuje pow. biol czynnej musimy ją zwiększyć poprzez:
    # zmniejszenie parkingu podziemnego (underground/2) tak aby po za jego granicami była powierzchnia biol. czynna w 100% a nie 50%
    # musimy uzyskać conajmniej równość green_area = received_area.
    # zmniejszając ilość miejsc postojowych o 1 zmniejszamy powierzchnię zabudowy dwupoziomowego parkingu o 17.5m2


def revision():
    global base_underground
    global received_green
    global number_of_parkings

    X = int(base_underground // 17.5)
    for i in range(X):

        # base_underground = base_underground - 17.5
        # received_green = 0.8 * base - 0.375 * base_underground - area_parkings_on_the_ground
        # received_green =  0.8 * base - 0.375 * (base_underground - (35 / number_of_underground_floors)- area_parkings_on_the_ground + (goal_flats_size / 1.2 / floors_amount)
        # received_green =  0.8 * base - (0.375 * base_underground) + (0.375 * (35 / number_of_underground_floors)) - area_parkings_on_the_ground + (goal_flats_size / 1.2 / floors_amount)

        if 'M' in destiny:
            received_green = received_green + (13.125 / number_of_underground_floors) + (PUM/((base_underground / 35 / number_of_underground_floors)+(area_parkings_on_the_ground/12))/ floors_amount)
        if 'B' in destiny:
            received_green = received_green + 6.56 + 1000/ 30 / floors_amount

        if received_green >= green_area:
            base_underground = base_underground - (i * (35 / number_of_underground_floors))
            print(i)
            break
        else:
            continue

    print(base_underground, "= base_underground")

    number_of_parkings = int(base_underground // (35 // number_of_underground_floors) + area_parkings_on_the_ground// 12)
    print('number of parkings =', number_of_parkings)
    return base_underground, number_of_parkings

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
calculate_area_parkings_on_the_ground()
check_bioactiv_area()
revision()



if 'M' in destiny:
    table = [
    ['powierzchnia działki', ' ', str(site_size) + 'm2', ' '],
    ['współczynnik zabudowy -> powierzchnia zabudowy', str(building_factor) +'%',  str(BA)+'m2', str(round((BA/site_size*100), 2))+'%'],
    ['intensywność zabudowy -> powierzchnia całkowita', str(intensity_factor), str(TA)+'m2', str(round((TA/site_size), 2))],
    ['powierzchnia biologicznie czynna', str(green_area * 100 / base)+'%', str(round(received_green, 2))+'m2', str(round((received_green / base * 100), 2)) + '%'],
    ['wymagana zieleń na gruncie', str(green_area_100 * 100 / base) +'%', str(green_area_100) + 'm2', str(round((green_area_100 / base * 100), 2)) +'%'],
    ['wysokość zabudowy', str(building_height)+'m', str(floors_amount)+' kondygnacji', str(building_height)+'m'],
    ['ilość mieszkań', ' ', int(number_of_parkings / parking_place_M), ' '],
    ['średnia wielkość mieszkania', ' ', str(round((PUM/(number_of_parkings/ parking_place_M )),2)) + 'm2 lub większe', ' '], SEPARATING_LINE,
    ['ilość miejsc postojowych razem', str(parking_place_M) + ' na mieszkanie', round(number_of_parkings, 2), str(parking_place_M) + ' na mieszkanie'],
    ['w tym ilość miejsc postojowych na poziomie terenu', '', int(area_parkings_on_the_ground // 12), ''],
    ['w tym ilość miejsc postojowych w parkingu podziemnym', '', int(base_underground // (35 // number_of_underground_floors)), ''], SEPARATING_LINE,
    ['ilość kondygnacji podziemnych', '', number_of_underground_floors, ''],
    ['współczynnik do liczenia PUM', ' ', 0.69, ' '], SEPARATING_LINE,
    ['PUM', '',str(PUM) + 'm2', '']]


elif 'B' in destiny:
    table = [
    ['powierzchnia działki', ' ', str(site_size) + 'm2', ' '],
    ['współczynnik zabudowy -> powierzchnia zabudowy', str(building_factor) +'%',  str(BA)+'m2', str(round((BA/site_size*100), 2))+'%'],
    ['intensywność zabudowy -> powierzchnia całkowita', str(intensity_factor), str(TA)+'m2', str(round((TA/site_size), 2))],
    ['powierzchnia biologicznie czynna', str(green_area * 100 / base)+'%', str(round(received_green, 2))+'m2', str(round((received_green / base * 100), 2)) + '%'],
    ['wymagana zieleń na gruncie', str(green_area_100 * 100 / base) +'%', str(green_area_100) + 'm2', str(round((green_area_100 / base * 100), 2)) +'%'],
    ['wysokość zabudowy', str(building_height)+'m', str(floors_amount)+' kondygnacji', str(building_height)+'m'],
    ['ilość miejsc postojowych razem', str(parking_place_B) + ' na 1000m2', round(number_of_parkings, 2), str(parking_place_B) + ' na 1000m2'], SEPARATING_LINE,
    ['w tym ilość miejsc postojowych na poziomie terenu', '', int(area_parkings_on_the_ground // 12), ''],
    ['w tym ilość miejsc postojowych w parkingu podziemnym', '', int(base_underground // (35 // number_of_underground_floors)), ''], SEPARATING_LINE,
    ['ilość kondygnacji podziemnych', '', number_of_underground_floors, ''],
    ['powierzchnia użytkowa obsłużona przez parkingi', '', str(round((number_of_parkings * 1000 / parking_place_B), 2))+'m2', ' '],
    ['współczynnik do liczenia GLA', ' ', 0.69, ' '], SEPARATING_LINE,
    ['GLA', '', str(GLA) + 'm2', '']]
7

print(tabulate((table), stralign = "center", headers = [' ', 'nazwa parametru', 'wymóg MPZT', 'osiągięte parametry', 'osiągnięte wskaźniki'], tablefmt="simple"),"\n")
