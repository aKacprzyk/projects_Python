#klasa głowna i bazowa dla wszytskich roślin
class Roślina():
    def __init__(self, nazwa, nazwa_łac, cena, gleba = "kwaśna", miejsce = "ogród", kolor = "zielony"):
        #zminne defaultowe to gleba - kwaśna i miejsce - ogród i kolor - zielony
        #definiowanie zmiennych dla tej klasy 
        self.nazwa = nazwa
        self.nazwa_łac = nazwa_łac
        self.cena = float(cena)
        self.cena = "{:.2f}".format(self.cena) #"{:.2f}".format() zapewnia odpowiedni zapis ceny tak by było zero na końcu
        self.gleba = gleba
        self.miejsce = miejsce
        self.kolor = kolor
    def __repr__(self):
        #drukowanie zdania dla roślin
        return f"{self.nazwa} łac {self.nazwa_łac} w cenie {self.cena} zł na glębę {self.gleba} na miejsce {self.miejsce}"

#podklasa dla rośliny która jest iglakiem
class Iglak(Roślina):
    def __repr__(self):
        #zmienne są te same w tym zmienne defaultowe
        return f"Iglak {self.kolor} {super().__repr__()}" #zwraca tekst taki jak dla rośliny tylko z dopiską Iglak i kolorem defaultowym

# podklasa dla rośliny ktora jest ozdobna
class Ozdobny(Roślina):
    def __init__(self, nazwa, nazwa_łac, cena, gleba, kolor, miejsce = "dowolny"):
        # tutaj jest  inna wartosc defaultowa dla miejsca, dlatego definiujemy 
        super(Ozdobny, self).__init__(nazwa, nazwa_łac, cena, gleba)
        # to mówi ze te zmienne sa zaczerpięte z klasy bazowej
        self.miejsce = miejsce
        #definiowanie miejsca bo to zostało zmienione
    def __repr__(self):
        #drukowanie tekstu dla ozdobnych roslin z informacja o kolorze
        return f"{self.kolor} {super().__repr__()}"

class Kwiat(Roślina):
    def __init__(self, nazwa, nazwa_łac, cena, gleba, kolor, miejsce = "ogród"):
        super(Kwiat, self).__init__(nazwa, nazwa_łac, cena, gleba, miejsce)
        # tu jest kolor inny niż zdefiniowany dlatego robimy dodatkowa definicje dla kwiatu
        # z zdefiniowanym kolorem
        self.kolor = kolor
    def __repr__(self):
        # drukowanie tetu z uwzględnieniem tekstu Kait i jego koloru
        return f"Kwiat {self.kolor} {super().__repr__()}"
   
class Krzew(Roślina):
    def __init__(self, nazwa, nazwa_łac, cena, miejsce = "ogród", gleba = "lekko kwaśna"):
        # jest inna wartosc defaultowa ziemi dlatego trzeba to ponowne zdefiniowac 
        super(Krzew, self).__init__(nazwa, nazwa_łac, cena, miejsce )
        # inne wartosci są takie same jak z głowenej klasy i ich definicje sa takie same
        self.gleba = gleba 
        # ponowne definiowanie gleby
    def __repr__(self):
        #drukowanie tekstu jak dla głównej klasy
        return f"{super().__repr__()}"

#przykłady
cyprysik = Iglak("Cyprysik tępołuskowy", "Chamaecyparis obtusa", 30.90)
print(cyprysik)

monstera = Roślina("Monstera dziurawa", "Monstera deliciosa", 53.50, "lekko kwaśny", "Biuro")
print(monstera)

ozdobny = Ozdobny("Jałowiec płożący", "luniperus scopulocum", 32.40, "dowolny" , "Ogród")
print(ozdobny)

róża = Kwiat("Róża wielkokwiatowa 'Mister Lincoln'", "Rosa 'Mister Lincoln'", 77.10, "obojetny", "bordowy")
print(róża)

sosna = Krzew("Sosna Banksa 'Arctis'", "Pinus banksiana", 57.99)
print(sosna)

#klasa bazowa dla doniczki
class Doniczka():
    def __init__(self, materiał, wysokość, cena):
        #definiowanie zmiennych dla klas bazowych 
        self.materiał = materiał
        self.wysokość = wysokość
        self.cena = float(cena)
        self.cena = "{:.2f}".format(self.cena)
    def __repr__(self):
        return f"doniczka {self.materiał} wysokość:{self.wysokość} cm w cenie {self.cena} zł"

#podklasa dla doniczki okragłej
class okrągła_doniczka(Doniczka):
    def __init__(self, materiał, wysokość, cena, średnica):
        super(okrągła_doniczka, self).__init__(materiał, wysokość, cena)
        #dodanie zmiennej srednica i jej zdefiniowanie
        self.średnica = średnica
    def __repr__(self):
        return f"okrągła o średnicy {self.średnica} cm {super().__repr__()}"

#podklasa dla doniczki podłużnej
class podłużna_doniczka(Doniczka):
    def __init__(self, materiał, wysokość, cena, długość, szerokość):
        super(podłużna_doniczka, self).__init__(materiał, wysokość, cena)
        #dodanie zmiennych długoćs i szerokosc oraz ich zdefiniowanie
        self.długość = długość
        self.szerokość = szerokość
    def __repr__(self):
        return f"podłużna o wymiarach {self.długość} cm na {self.długość} cm {super().__repr__()}"

#przykłady
okrągła = okrągła_doniczka("terakota", "5 cm", 0.0, "7 cm")
print(okrągła)

kwadrat = podłużna_doniczka("plastik", "12 cm", 3.20, "40 cm", "10 cm")
print(kwadrat)

podstawka = okrągła_doniczka("plastik", "2 cm", 0.30, "9 cm")
print(podstawka)

#tworzenie klasy Pozycja
class Pozycja():
    #podajemy pierwszy numerTowaru i pojawia się gdy prierwszy raz uzyje się tej klasy w tej iteracji
    __nrTowaru__ = 100008    
    def __init__(self, ogród = None , doniczka = None):
        #definiowanie argumentów klasy Pozycja
        self.ogród = ogród
        self.doniczka = doniczka
        self.cena_ogród = self.ogród.cena if self.ogród else 0
        #jesli jest podany ogród to jego cena jest zapisywana w cena_ogród, a jak nie jest to cena_ogród = 0
        self.cena_doniczka = self.doniczka.cena if self.doniczka else 0
        #tak samo dla doniczki
        self.suma_cen = float(self.cena_ogród) + float(self.cena_doniczka)
        #dodajemy ceny_ogród do cena_doniczka i to jest definicja suma_cen
        self.nr = Pozycja.__nrTowaru__
        #zdefiniowanie nr_towaru jako częsci tej klasy jako nr
        Pozycja.__nrTowaru__ += 1
        #modyfikajcja nr_towaru poprzez dodanie 1 do poprzediej wartosci
    def __repr__(self):
        #drukowanie tekstu w zaleznosci jakie dane zostały podane
        if self.doniczka == None and self.ogród != None: #jesli podany był ogród to drukuje to:
            return f"Towar {self.nr} cena {float(self.cena_ogród):.2f} {self.ogród.nazwa} {self.ogród.nazwa_łac} bez doniczki"
        elif self.doniczka != None and self.ogród != None: #jesli podane były dwie wartosci to to:
            return f"Towar {self.nr} cena {float(self.suma_cen):.2f} {self.ogród.nazwa} {self.ogród.nazwa_łac} {self.doniczka}"
        elif self.doniczka != None and self.ogród == None: #jesli była podana doniczk to to
            return f"Towar {self.nr} cena {float(self.cena_doniczka):.2f} tylko {self.doniczka}"
    @classmethod #metoda klaspwa i jest potrzebna do tworzenia obiektu do podania ceny doniczki
    def doniczka(cls, doniczka): #cls to odniesienie do klasy pozycja
        return cls(doniczka = doniczka)
        # a ma zwrócić ona w miejsce tego odwołania to ze podany argument to jest doniczka

#przykłady
cyprys = Pozycja(cyprysik)
print(cyprys)

cyprys_z_podstawką = Pozycja(cyprysik, podstawka)
print(cyprys_z_podstawką)

różyczka = Pozycja(róża)
print(różyczka)

podst = Pozycja.doniczka(podstawka)
print(podst)





