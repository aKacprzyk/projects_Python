#!/usr/bin/env python
# coding: utf-8

# In[5]:


#funkcja bitwa oblicza na podstawie stanów początkowych obu armii: atakującej i broniącej ich stany po bitwie, 
#jednak pokazuje ona tyko wartości dla oddziałów, gdzie przeżyła conajmniej jedna jednostka
def Bitwa(armia_atak, armia_obrona):
    śmiertelnosc_atak = {}
    śmiertelnosc_obrona = {}

    #słownik postaci
    # dodanie nowej postaci
        # "nazwa_rasy": {"nazwa_przeciwnika": (ile postac zabija w ataku, ile postac zabija w obronie), }
    postacie = {
    "krasnolud": {'goblin': (22, 44), 'ork': (10, 20)},
    "hobbit": {'goblin': (75, 36), 'ork': (18, 22)},
    "goblin": {'hobbit': (1, 1)},
    "ork": {'krasnolud': (1, 1), 'hobbit': (2, 3)},
    "pirat": {'hobbit': (1, 4), 'goblin': (24, 42), 'ork': (4, 0)}
    }
    
    #definiowanie funckji do obliczenia siły
    def siła(armia, typ):
        siła = []
        # tworzymy pustą liczbę by w niej zapisywać informację
        for oddział in armia:
            #rozdzielamy armię  na oddziały ktore sa złożone z tylko jednej rasy 
            for postać in postacie:
                # następnie rodzielamy słownik na poszczególne rasy, by móc porównać je z rasami w oddziale armii
                if oddział == postać:
                    #jesli rasa z której składa się oddział jest taka sama jak ta wypisana w slowniku postacie 
                    #to dla tej rasy wypisuje się jej siłe bojową  przeciwko danej rasie 
                    for przeciwnik in postacie.get(postać):
                        wartość = armia.get(postać) * postacie.get(postać).get(przeciwnik)[typ]
                        # obliczamy siłe ataku wszytskich przedstawicieli danej rasy przeciko danej rasie 
                        # armia.get(postać) - daje liczbe przedstawicieli danej rasy
                        # postacie.get(postać).get(przeciwnik) - odwoluje sie do słownika postaci i pozwala pobrac dana rase atakujacą 
                        # i jej obrażenia przeciwko danemu przeciwnikomi
                        # postacie.get(postać).get(przeciwnik)[0] - odwołanie [0] pozwala dostac wartosć obrażen jaka dana rasa zadaje w przypadku ataku
                        # a - odwołanie [1] pozwala dostac wartosć obrażen jaka dana rasa zadaje w przypadku obrony
                        przeciwnik_siła = {przeciwnik: wartość}
                        # zapisujemy w slowniku ile dany przeciwnik otrzymal obrażeń w istotach, 
                        # czyli tyle przeciwników zginie jesli zaatakuje cala liczebnosc tej postaci
                        siła.append(przeciwnik_siła)
                        # dołaczamy każdy dołaczony poprzednio słownik do listy, które zbiera obrażenia zadane przez arm atakująca danym istotą
        return siła # koniec funkcji siła

    #definiowanie funkcji do obliczenia smiertelności
    def śmiertelność(siła):
        śmiertelność = {}
        for słownik in siła:
            # rozdzielamy listę na poszczegolne słowniki z obrazeniami jakie otrzymał dany przeciwnik od danych posatci 
            # by to zsumowac wszystkie obrazenia tego przeciwnika
            for klucz, wartość in słownik.items():
                # rozdzielamy słownik na poszczegolne klucze i wartosci
                śmiertelność[klucz] = śmiertelność.get(klucz, 0) + wartość
                # zapisujemy wartość w słowniku śmiertelność_atak dla danego klucza, czyli przeciwnika jako suma wartosci dla klucza ze slownika i wartosci
                #jesli wczesniej nie było niczego zapisanego w śmiertelnosc_atak dla tego przecwnika to przypisywane jest 0
        return śmiertelność # zwraca śmiertlenosc, koniec funkcji 
   
    armia_obrona_po = armia_obrona.copy()
    # tworzymy kopie armi, ktora się broni by móc od niej odjąć smiertelnosc armii atakujacej i otrzymać informacje kto przeżył po bitwie
    armia_obrona_po = {k: armia_obrona_po.get(k, 0) - śmiertelność(siła(armia_atak, 0)).get(k, 0) for k in śmiertelność(siła(armia_atak, 0)).keys() | armia_obrona_po.keys() 
                       if armia_obrona_po.get(k, 0) - śmiertelność(siła(armia_atak, 0)).get(k, 0) > 0}
    # odejmujemy od liczebnosci armii broniacej sie śmiertlenosci armi atakującej dla kazdego k,
    # czyli klucza ktory nalezy jednoczenie do śmiertelnosci i armii
    # jednak odejmujemy te wrtosci jedynie gdy reszta z działanie jest wieksza od zera by unikać nierealnych ujemnych wyników odnosni liczebnosci 

    armia_atak_po = armia_atak.copy()
    # tworzymy kopie armi, ktora atakuje by móc od niej odjąć smiertelnosc armii broniacej i otrzymać informacje kto przeżył po bitwie
    armia_atak_po = {k: armia_atak_po.get(k, 0) - śmiertelność(siła(armia_obrona, 1)).get(k, 0) for k in śmiertelność(siła(armia_obrona, 1)).keys() | armia_atak_po.keys()
                     if armia_atak_po.get(k, 0) - śmiertelność(siła(armia_obrona, 1)).get(k, 0) > 0}
    # odejmujemy od liczebnosci armii atakujacej śmiertlenosci armi broniacej dla kazdego k,
    # czyli klucza ktory nalezy jednoczenie do śmiertelnosci i armii
    # jednak odejmujemy te wrtosci jedynie gdy reszta z działanie jest wieksza od zera by unikać nierealnych ujemnych wyników odnosni liczebnosci 

    return('armia obrona po bitwie: ', armia_obrona_po, 'armia atak po bitwie: ', armia_atak_po) 
    # zwraca informacje o stanach po bitwie obu armii 

#testowanie funkcji
#stan armii początkowy testowy
armia_atak_test = {'krasnolud': 1000, 'hobbit': 2000}
armia_obrona_test = {'goblin': 140, 'ork': 300, 'pirat': 1}

#testowanie funkcji
Bitwa(armia_atak_test, armia_obrona_test)
print(Bitwa(armia_atak_test, armia_obrona_test))

