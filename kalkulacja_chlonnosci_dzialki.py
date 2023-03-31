from tabulate import tabulate, SEPARATING_LINE
import csv


class Building:
    def __init__(self, table_rows):
        self.table_rows = table_rows
        self.float_value = 0
        self.building_area = 0
        self.total_area = 0
        self.base_underground = 1000
        self.area_parkings_on_the_ground = 12
        self.received_green = 1
        self.number_of_parkings_on_the_ground = 0
        self.number_of_parkings_underground = 0
        self.number_of_parkings = 1
        self.floors_amount = 1
        self.table = []

    @property
    def site_size(self):
        return self.table_rows[0][2]

    @property
    def base(self):
        return self.table_rows[1][2]

    @property
    def building_factor(self):
        return self.table_rows[3][2]

    @property
    def intensity_factor(self):
        return self.table_rows[4][2]

    @property
    def building_height(self):
        return self.table_rows[5][2]

    @property
    def green_area_percentage(self):
        return self.table_rows[6][2]

    @property
    def green_area(self):
        return self.table_rows[6][2] * self.table_rows[1][2] / 100

    @property
    def green_area_100_percentage(self):
        return self.table_rows[7][2]

    @property
    def green_area_100(self):
        return self.table_rows[7][2] * self.table_rows[1][2] / 100

    @property
    def number_of_underground_floors(self):
        return self.table_rows[10][2]

    @property
    def destiny(self):
        return self.table_rows[11][2]

    def what_prompt(self, field):
        self.table_rows[field][2] = input(f"{self.table_rows[field][1]} [{self.table_rows[field][3]}]: ")
        return self.table_rows[field][2]
    
    def check_parametr(self, field):

        try:
            if "," in str(self.table_rows[field][2]):
                self.table_rows[field][2] = float(self.table_rows[field][2].replace(",", "."))

            if self.table_rows[field][2] == "":
                self.table_rows[field][2] = 0.0

            if field < 11:
                if float(self.table_rows[field][2]) < 0.0:
                    raise ValueError
                else:
                    (self.table_rows[field][2]) = float(self.table_rows[field][2])

            if float(self.table_rows[5][2]) <= 3.5:
                print("Podałaś/eś złą wartość. Wysokość budynku musi być większa od 3. Wpisz ją jeszcze raz")
                self.what_prompt(5)
                self.check_parametr(5)

            if self.table_rows[11][2] not in ["M", "m", "B", "b"]:
                print("""
                Podałaś/eś złą wartość,
                jeśli teren jest przeznaczony na mieszkania wpisz "M",
                jeśli teren jest przeznaczony na usługi lub biura wpisz "B".""")
                self.check_parametr(11)
            else:
                self.table_rows[11][2] = self.table_rows[11][2].upper()

            if self.table_rows[3][2] == 0:
                if self.table_rows[4][2] == 0:
                    print("""
                        jeden z parametrów musi być większy od zera.
                        Popraw 'współczynnik zabudowy' lub 'współczynnik intensywności zabudowy'""")
                    self.what_prompt(3)
                    self.what_prompt(4)
                    self.check_parametr(3)
                    self.check_parametr(4)

            if float(self.table_rows[0][2]) != max(float(self.table_rows[0][2]), float(self.table_rows[1][2]), float(self.table_rows[2][2])):
                print("""
                'Powierchnia działki musi być większa lub równa
                'terenowi pod zabudowę' oraz większa od
                'terenu pod którym może być podziemie'""")
                self.what_prompt(0)
                self.check_parametr(0)
            elif float(self.table_rows[0][2]) == max(float(self.table_rows[0][2]), float(self.table_rows[1][2]), float(self.table_rows[2][2])):
                self.table_rows[0][2] = float(self.table_rows[0][2])

        except ValueError:
            print(type(self.table_rows[field][2]))
            print("Podałaś/eś złą wartość. Podana odowiedź musi być liczbą dodatnią. Wpisz ją jeszcze raz")
            self.what_prompt(field)
            self.check_parametr(field)

        return self.table_rows[field][2]

    def check_table_rows(self):
        for i in range(len(self.table_rows)):
            self.table_rows[i][2] = self.check_parametr(i)

    def ask_for_amendment(self):

        print(f"""
            PODAŁEŚ TAKIE PARAMETRY:
        {tabulate(self.table_rows, headers=["numer", "Parametr", "Wartość", "Jednostka"])}
        """)

        field = input("""
            JEŚLI CHCESZ POPRAWIĆ JEDEN Z PARAMETRÓW, WPISZ JEGO NUMER PORZĄDKOWY.
            JEŚLI WSZYSTKO SIĘ ZGADZA PRZEJDŹ DALEJ
            """)
        try:
            self.what_prompt(int(field)-1)
        except ValueError:
            pass

        self.check_table_rows()
        return self.table_rows

    def count_floors(self):
        self.floors_amount = int(self.building_height // self.h)
        return self.floors_amount

    def calculate_building_area(self):   # Building_area = wyliczenie powierzchni zabudowy
        list = []

        if self.building_factor != 0:
            BAB = self.base * self.building_factor / 100
            list.append(BAB)
        elif self.building_factor == 0:
            BAB = 0
        if self.intensity_factor != 0:
            BAI = self.intensity_factor * self.base // self.floors_amount
            list.append(BAI)
        elif self.intensity_factor == 0:
            BAI = 0

        self.building_area = min(list)
        return self.building_area

    def calculate_total_area(self):   # total_area = wyliczenie powierzchni całkowitej
        list = []

        if self.building_factor != 0:
            TAB = float(self.building_area) * (self.building_height // self.h)
            list.append(TAB)
    # TAB = powierzchnia całkowita wyliczona na podstawie współczynnika zabudowy
        if self.intensity_factor != 0:
            TAI = self.base * self.intensity_factor
            list.append(TAI)
    # TAI = powierzchnia całkowita wyliczona na podstawie intensywności  zabudowy
        self.total_area = min(list)
        return self.total_area

    def check_capability_for_underground_parking(self):

        if self.base - self.table_rows[2][2] < self.green_area_100:
            self.base_underground = self.base - self.green_area_100
        else:
            self.base_underground = self.table_rows[2][2]

        return self.base_underground

# przyjmujemy że 4% wszystkich parkingów zajmują parkingi naziemne.
    # 1 miejsce parkingowe pod ziemią potrzebuje 35m2
    # 1 miejsce parkingowe na ziemi liczymy jako 12m,
    # bo przestrzeń manewrowa wliczona jest już w pomniejszenie współczynnika
    # biologicznie czynnego i zazwyczaj wykorzystuje drogę dojazdową do garażu lub ppoż.

    def calculate_area_parkings_on_the_ground(self):

        self.area_parkings_on_the_ground = 0.014257 * (self.base_underground * self.number_of_underground_floors)
        return self.area_parkings_on_the_ground

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

    def check_bioactiv_area(self):

        self.received_green = 0.8 * self.base - 0.375 * self.base_underground - self.area_parkings_on_the_ground

        if self.green_area - self.received_green > 0:
            print("""
            wymagana powierzchnia biologicznie czynna nie zmieści się na działce,
            nastąpi zmniejszenie parkingu podziemnego""")

        return self.received_green

    # jeżeli brakuje pow. biol czynnej musimy ją zwiększyć poprzez:
    # zmniejszenie parkingu podziemnego (underground/2) tak aby po za jego granicami była powierzchnia biol. czynna w 100% a nie 50%
    # musimy uzyskać conajmniej równość green_area = received_area.
    # zmniejszając ilość miejsc postojowych o 1 zmniejszamy powierzchnię zabudowy dwupoziomowego parkingu o 17.5m2

    def calculate_number_of_parkings(self):
        self.number_of_parkings = int(self.number_of_parkings_on_the_ground + self.number_of_parkings_underground)

        return self.number_of_parkings


class Housing(Building):

    def __init__(self, table_rows):
        Building.__init__(self, table_rows)
        self.h = 3
        self.PUM = 1000
        self.average_size_of_app = 40

    @property
    def parking_place_index(self):
        return self.table_rows[8][2]

    def check_parking_place_index(self):
        if self.parking_place_index == 0:
            print("""
                Nie Podałaś/eś ilości parkingów wymaganych przez MPZT.
                Jeśli nie są wymagane przez prawo, wpisz liczbę której oczekujesz.
                Musi być to liczba dodatnia""")
            self.what_prompt(8)
            self.table_rows[8][2] = int(self.check_parametr(8))
            return self.table_rows[8][2]

    def calculate_usable_area(self):
        self.PUM = round(float(self.total_area * 0.69), 2)
        return self.PUM

    def calculate_average_size_of_app(self):
        try:
            self.average_size_of_app = round((self.PUM / (self.number_of_parkings / self.parking_place_index)), 2)

        except ZeroDivisionError:
            print("""
                Nie Podałaś/eś ilości parkingów wymaganych przez MPZT.
                Jeśli nie są wymagane przez prawo, wpisz liczbę której oczekujesz.
                Musi być to liczba dodatnia""")
            self.what_prompt(8)
            self.parking_place_index = int(self.check_parametr(8))
            self.average_size_of_app()

        return self.average_size_of_app

    def revision_received_green(self):

        return self.received_green + (13.125 / self.number_of_underground_floors) + (self.PUM/((self.base_underground / 35 / self.number_of_underground_floors)+(self.area_parkings_on_the_ground / 12)) / self.floors_amount)

    def print_table(self):
        self.table = [
            ['powierzchnia działki', ' ', f'{self.site_size}m2', ' '],
            ['współczynnik zabudowy -> powierzchnia zabudowy', f'{self.building_factor}%',  f'{self.building_area}m2', f'{round((self.building_area/self.site_size*100), 2)}%'],
            ['intensywność zabudowy -> powierzchnia całkowita', f'{self.intensity_factor}', f'{self.total_area}m2', f'{round((self.total_area/self.site_size), 2)}'],
            ['powierzchnia biologicznie czynna', f'{self.green_area * 100 / self.base}%', f'{round(self.received_green, 2)}m2', f'{round((self.received_green / self.base * 100), 2)}%'],
            ['wymagana zieleń na gruncie', f'{self.green_area_100 * 100 / self.base}%', f'{self.green_area_100}m2', f'{round((self.green_area_100 / self.base * 100), 2)}%'],
            ['wysokość zabudowy', f'{self.building_height}m', f'{int(self.floors_amount)} kondygnacji', f'{self.building_height}m'],
            ['ilość mieszkań', ' ', int(self.PUM / self.average_size_of_app), ' '], SEPARATING_LINE,
            ['średnia wielkość mieszkania', ' ', f"{self.average_size_of_app}m2 lub większe", ' '],
            ['ilość miejsc postojowych razem', f'{self.parking_place_index} na mieszkanie', round(self.number_of_parkings, 2), f'{self.parking_place_index} na mieszkanie'],
            ['w tym ilość miejsc postojowych na poziomie terenu', '', self.number_of_parkings_on_the_ground, ''],
            ['w tym ilość miejsc postojowych w parkingu podziemnym', '', self.number_of_parkings_underground, ''], SEPARATING_LINE,
            ['ilość kondygnacji podziemnych', '', self.number_of_underground_floors, ''],
            ['współczynnik do liczenia PUM', ' ', 0.69, ' '], SEPARATING_LINE,
            ['PUM', '', f'{self.PUM}m2', '']]
        return self.table


class Offices(Building):

    def __init__(self, table_rows):
        Building.__init__(self, table_rows)
        self.h = 3.5
        self.GLA = 1000
        self.parkings_served_area = 1000

    @property
    def parking_place_index(self):
        return self.table_rows[9][2]

    def calculate_usable_area(self):
        self.GLA = float(round((self.total_area * 0.89), 2))
        return self.GLA

    def revision_received_green(self):
        return self.received_green + (13.125 / self.number_of_underground_floors) + 6.56 + 1000 / self.parking_place_index / self.floors_amount

    def calculate_parkings_served_area(self):

        try:
            self.parkings_served_area = float(self.number_of_parkings * 1000 / self.parking_place_index)
            self.parkings_served_area = min(self.parkings_served_area, self.GLA)

        except ZeroDivisionError:
            print("""
                Nie Podałaś/eś ilości parkingów wymaganych przez MPZT.
                Jeśli nie są wymagane przez prawo, wpisz liczbę której oczekujesz.
                Musi być to liczba dodatnia""")
            self.what_prompt(9)
            self.parking_place_index = int(self.check_parametr(9))
            self.calculate_parkings_served_area()

        return self.parkings_served_area

    def print_table(self):
        self.table = [
            ['powierzchnia działki', ' ', f'{self.site_size}m2', ' '],
            ['współczynnik zabudowy -> powierzchnia zabudowy', f'{self.building_factor} %',  f'{self.building_area}m2', f'{round((self.building_area/self.site_size*100), 2)}%'],
            ['intensywność zabudowy -> powierzchnia całkowita', self.intensity_factor, f'{self.total_area}m2', round((self.total_area/self.site_size), 2)],
            ['powierzchnia biologicznie czynna', f'{self.green_area * 100 / self.base}%', f'{round(self.received_green, 2)}m2', f'{round((self.received_green / self.base * 100), 2)}%'],
            ['wymagana zieleń na gruncie', f'{self.green_area_100 * 100 / self.base}%', f'{self.green_area_100}m2', f'{round((self.green_area_100 / self.base * 100), 2)}%'],
            ['wysokość zabudowy', f'{self.building_height}m', f'{self.floors_amount} kondygnacji', f'{self.building_height}m'], SEPARATING_LINE,
            ['ilość miejsc postojowych razem', f'{self.parking_place_index} na 1000m2', round(self.number_of_parkings, 2), f'{round((self.number_of_parkings * 1000 / self.parkings_served_area), 2)} na 1000m2'],
            ['w tym ilość miejsc postojowych na poziomie terenu', '', self.number_of_parkings_on_the_ground, ''],
            ['w tym ilość miejsc postojowych w parkingu podziemnym', '', self.number_of_parkings_underground, ''], SEPARATING_LINE,
            ['ilość kondygnacji podziemnych', '', self.number_of_underground_floors, ''],
            ['powierzchnia użytkowa obsłużona przez parkingi', '', f'{round(self.parkings_served_area, 2)}m2', ' '],
            ['współczynnik do liczenia GLA', ' ', 0.89, ' '], SEPARATING_LINE,
            ['GLA', '', f'{self.GLA}m2', '']]
        return self.table


def main():

    with open('assets\\base_variabile.csv', 'r', encoding='ANSI', errors='ignore') as fields:
        csvreader = csv.DictReader(fields)

    # Tworzymy słownik, w którym kluczami są nazwy pól, a wartościami są wprowadzone przez użytkownika wartości.
        data = {}

        for field in csvreader:
            prompt = f"{field['label']} [{field['unit']}]: "
            value = str(input(prompt))
            data[field['name']] = value

    # Tworzymy listę, która będzie składać się z wierszy tabeli
        table_rows = []
        csvreader = csv.DictReader(open('assets\\base_variabile.csv', 'r', encoding='ANSI', errors='ignore'))
        number = 0
        for field in csvreader:
            number = number + 1
            label = field['label']
            value = data[field['name']]
            unit = field['unit']
            table_rows.append([number, label, value, unit])

        # print(tabulate(table_rows, headers=["#", "Label", "Value", "Unit"]))

    building = Building(table_rows)
    building.check_table_rows()
    building.ask_for_amendment()

    response = input('''
            CZY CHCESZ JESZCZE POPRAWIĆ JESZCZE KTÓRYŚ Z
            PARAMETRÓW? WPISZ 'TAK' LUB PRZEJDŹ DALEJ
            ''')

    while 'T' in response.upper():
        building.ask_for_amendment()
        response = input('''
            CZY CHCESZ JESZCZE POPRAWIĆ JESZCZE KTÓRYŚ Z
            PARAMETRÓW? WPISZ 'TAK' LUB PRZEJDŹ DALEJ
            ''')

    if 'M' in building.table_rows[11][2]:
        building = Housing(table_rows)
    elif 'B' in building.table_rows[11][2]:
        building = Offices(table_rows)

    building.count_floors()
    building.calculate_building_area()
    building.calculate_total_area()
    building.calculate_usable_area()
    building.check_capability_for_underground_parking()
    building.calculate_area_parkings_on_the_ground()
    building.check_bioactiv_area()
    building.calculate_number_of_parkings()

    X = int(building.base_underground // 17.5)

    for i in range(X):

        try:

            # base_underground = base_underground - 17.5
            # received_green = 0.8 * base - 0.375 * base_underground - area_parkings_on_the_ground
            # received_green =  0.8 * base - 0.375 * (base_underground - (35 / number_of_underground_floors)- area_parkings_on_the_ground) + (goal_flats_size / 1.2 / floors_amount)
            # received_green =  0.8 * base - (0.375 * base_underground) + (0.375 * (35 / number_of_underground_floors)) - area_parkings_on_the_ground + (goal_flats_size / 1.2 / floors_amount)

            building.revision_received_green()

            if building.revision_received_green() >= building.green_area:
                building.base_underground = building.base_underground - (i * (35 / building.number_of_underground_floors))
                building.number_of_parkings_underground = int(building.base_underground * building.number_of_underground_floors // 35)
                building.number_of_parkings_on_the_ground = int(building.area_parkings_on_the_ground // 12)
                building.number_of_parkings = int(building.number_of_parkings_on_the_ground + building.number_of_parkings_underground)
                break

        except ZeroDivisionError:

            building.received_green = building.received_green + 12
            building.base_underground = 0

            if building.received_green >= building.green_area:
                building.number_of_parkings = int((building.area_parkings_on_the_ground // 12) - i)
                building.number_of_parkings_underground = 0
                building.number_of_parkings_on_the_ground = int((building.area_parkings_on_the_ground // 12) - i)
                break

    try:
        building.calculate_average_size_of_app()
    except AttributeError:
        pass

    try:
        building.calculate_parkings_served_area()
    except AttributeError:
        pass

    building.print_table()

    print(tabulate((building.table), stralign="center", headers=['nazwa parametru', 'wymóg MPZT', 'osiągięte parametry', 'osiągnięte wskaźniki'], tablefmt="simple"), "\n")


if __name__ == "__main__":
    main()
