def obliczanie_dochodu(nazwa_pliku_z_wynikami, nazwa_pliku_z_dochodzami, nazwa_pliku_z_kursami_walut):
    #funkcja, ktora potrzebuje trzech argumentów takich jak: 
        # - nazwa pliku z wynikami ( czyli gdzie maja byc zapisane wyniki) musi być w formacie json,
        # - nazwa pliku z dochodami format txt,
        # - nazwa pliku z walutami fromat csv

    #BIBLIOTEKA
    import json
    #jest ona niezbędna do zapisu pliku z wynikami w formacie json
    
    #odczytywanie zawartości plików podanych w argumntach
    dochody = open(str(nazwa_pliku_z_dochodzami), "r", encoding='utf8')
    waluty = open(str(nazwa_pliku_z_kursami_walut), 'r', encoding='utf8')
    wiersze_waluty = waluty.readlines() 
    # jako ze jest to plik csv, chce by kazdą linie zapisało mi jako elemenent w liscie i zapisujemy ta liste pod wiersze_waluty

    #otwieranie pliku z wynikami by zapisać w nim wyniki, ale on usuwa wszystko co było poprzednio w pliku o tej nazwie 
    wyniki = open(str(nazwa_pliku_z_wynikami), "w", encoding = "utf8")
    
    #SŁOWNIK WALUT
    # tworzeni i edycja nagłowka (usunięcie zbędnych znaków)
    nagłówek_waluty = wiersze_waluty[0].split(",")
    nagłówek_waluty[-1] = nagłówek_waluty[-1].strip()
    #tworzenie słownika z walutami = pusty do poźniejszego uzupełnienia w kodzie
    słownik_walut = {}
    
    
    #DOCHODY
    wiersze = dochody.readlines()
    # tworzenie wierszy poprzez funkcje readlines(), która czyta plik i każdy wiersz jest zapisywany jako element w liście

    #PRZYGOTOWANIE PLIKU DO WYDRUKU W NIM WYNIKÓW
    wyniki_wydruk = {}

    #zamiana informacji zawartych w pliku o dochodach na słownik o formacie {id: {data: {waluta: wartośći, waluta: wartość}}}
    for wiersz in wiersze: # odczytuje kazdy element z listy
        słowa = wiersz.split() # podział wiersza na słowa czyli zamiana elementu na lsitę gdzie kazde słowo jest nowym elementem
        id = słowa[0] # przydzielenie pierwszego elementu z listy do kategorii id
        data = słowa[1] # przydzielenie drugiego elementu z listy do kategorii data
        n = len(słowa) - 2 # ustalenie długości wyrazów w liscie słowa nie licząc dwóch pierwszych
        i = 2 # liczba pomocnicza do tworzenia słownika z wartosciami i walutami
        podsłownik = {} # pusty podsłownik potrzebny do storzenia słownika z wartościami i walutami
        
        while n > 0: # petla która będzie się powtarzać dopóki każde słowo nie jest włożone w kategorie
            if słowa[i].startswith("!"): # jeśli słowo rozpoczyna się na ! to robi zwartość w pętli
                suma = 0 # wartość lokalna , która jest niezbędna do wprowadzenia zmennej która będzie zliczać sumę wszystkich 
                #wartości dochodu dla danej waluty
                waluta = słowa[i] # przypisanie słowa, które zaczyna się na ! jako walita
                j = i + 1 # zwiększenie wartosci liczby pomocniczej o jeden i przypisanie nowej licznie pomocniczej 
                # w celu uzyskania koljenego słowa po walucie
                m = (n - 1)/2 # stworzenie liczby pomocniczej która jest połową długosci listy słowa 
                # po odcieciu wczesniej przypisanych wartosci
                
                while m > 0: # kolejna petla, która będzie sie powtrzać dopoki kazde słowo nieprzypisane się nie za kategoryzuje
                    if słowa[j].startswith("!"): # sprawdzenie czy pojawia się jakąs inna waluta 
                        break # jesli jest koniec tej petli i przechodzimy do petli while n > 0
                    else: # jelsi nie ma kolejnej waluty to:
                        suma += float(słowa[j]) # do sumy jest dopisisywana wartosci podana w dochodach z kategorią float
                        j +=2 # zwiększenie liczby pomocniczej o 2 by dostac kolejna wartość zamiast powodu zarobku
                        m -= 1 # zmniejszenie się liczby pomocniczej do petli  
                podsłownik[waluta] = suma # zapisanie waluty jako klucza i sumy jako wartosci, 
                # jesli juz byla ta waluta to ja nadpisuje z nowa suma ktora jest suma tej i wszytskich poprzednich wartosci
            i += 1 # zwiększenie liczby pomocniczej o 1 by dostac kolejne słowo
            n -=1 # zmniejszenie się liczby pomocniczej do petli 
        słownik = {id: {data: podsłownik}} # stworzenie słownika i jego formy

        # PODZIAŁ LISTY DOCHODY NA POSZCZEGÓLNE ELEMENTY POJEDYNCZO
        for id_klucz, data_wartość in słownik.items(): # podział elementów z słownika na klucz id i kolejny słownik {data: podsłownik}
            for data_klucz, waluta_wartość in data_wartość.items(): # podział {data: podsłownik} na datę i podsłownik
                data_klucz_format = data_klucz.replace("-", "") # zmiana formatu daty na ten co jest w waluty.csv
                # zamiana znaku - na nic
                lista_pomocnicza = [] # stworzenie listy_pomocniczej niezbędnej do podliczenia sumy dla wielu wartości różnych walut
                
                if not słownik[id_klucz][data_klucz]: # jeśli nie ma na dane id i date poddanej wartości to ma dać zero 
                        wyniki_wydruk[id_klucz] = 0
                        break
                    
                for waluta_klucz, suma_wartość in waluta_wartość.items(): # podział podsłwonika na walute klucz i sumę wartosci
                    waluta_klucz_format = waluta_klucz.replace("!", "") # zmiana formatu waluty by była tylko nazwa waluty
                    # czyli usuniecie znaku !

                    if waluta_klucz_format == 'PLN': # jesli waluta to PLN 
                        wyniki_wydruk[id_klucz] = suma_wartość # to wspisuje do klucza id sumę_wartości w słowniku wyniki wydruk
                        break       
                        
                    else: # jesli jest to inna waluta to:
                        for i in range(1, len(wiersze_waluty)): # jest tworzona petla która będzie się powtarzać 
                            #od 1 do długosci wiersza_walut z słownika walut wczesniej utworzonego
                            # i przyjmuje te wartosci z tego przedziału
                            
                            # modyfikacja zawartosci tego słownika
                            wiersz_waluty = wiersze_waluty[i].split(",") # podzielenie wierszy w miejscu gdzie jest przecinek
                            wiersz_waluty[-1] = wiersz_waluty[-1].strip() # ostatnia warotść ma dopisek /n i tu go usuwamy
                            
                            for j in range(0, len(nagłówek_waluty)): # tak samo jak powyższa petla 
                                #tylko j przyjmuje wartosci od 0 do długosci nagłowka słownika walut
                                
                                słownik_walut[nagłówek_waluty[j].replace("1", "").replace("00", "")] = wiersz_waluty[j]
                                # modyfikacja nagłowka walut by usunąć 1 lub 100 przed nazwami walut, na poczatku 1 a potem 00
                            
                            if słownik_walut["data"] == data_klucz_format: # jesli data ze słownika zagdza się z iterowana datą to:
                                ### WAZNE - jesli nie ma daty w pliku csv to nie obliczy dla tej pozycji wyniku
                                for klucz in słownik_walut.keys(): # iterowanie po kluczu z słownika walut
                                    if waluta_klucz_format == klucz: 
                                        # jesli iterowany klucz z słownika walut zgadza się z iterowanym kluczem to:
                                        if len(waluta_wartość) == 1: 
                                            # jesli dlugosci podsłownika jest jeden czyli byla tyko jedna waluta to:
                                            suma_wartość = round(suma_wartość * float(słownik_walut[waluta_klucz_format]), 2)
                                            # nowa suma wartosci to zaokraglony wynik mnozenia starej sumy_wartosci 
                                            # z przelicznikiem tej waluty na dany dzien 
                                            wyniki_wydruk[id_klucz] = suma_wartość 
                                            # zapisani do klucza id sumę_wartości w słowniku wyniki wydruk
                                        else: # jesli jest wiećej niż jedna waluta to:
                                            suma_wartość = round(suma_wartość * float(słownik_walut[waluta_klucz_format]), 2)
                                            # nowa suma wartosci to zaokraglony wynik mnozenia starej sumy_wartosci 
                                            # z przelicznikiem tej waluty na dany dzien 
                                            lista_pomocnicza.append(suma_wartość) # potem jest zapisywanie w liscie pomocniczej
                                            wyniki_wydruk[id_klucz] = sum(lista_pomocnicza)
                                            # zapisani do klucza id sumy z elementów listy pomoczniczej w słowniku wyniki wydruk

    json.dump(wyniki_wydruk, wyniki, ensure_ascii=False) # zapisanie wyników do pliku z wynikami
    wyniki.close() # zamnknięcie pliku z wynikami