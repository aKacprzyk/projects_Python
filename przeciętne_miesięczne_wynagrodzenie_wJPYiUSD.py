# -*- coding: utf-8 -*-
import requests #biblioteka niezbędna do pobrania danych przy pomocy API
import pandas as pd 
import matplotlib.pyplot as plt #biblioteka potrzebna do stworzenia wykresu liniowego
import matplotlib.dates as mdates #biblioteka potrzena do poprawnej prezentacji osi x na wykresie w celu osiagniecia czytelnego wykresu

#pobieranie danych dotyczących przeciętnego wynagrodzenia z GUSU bo storna ministerstwa finansów nie pozwala pobrac danych
api_url = url= "https://bdl.stat.gov.pl/api/v1/data/by-unit/000000000000?var-id=64428&format=json" #adres api
response = requests.get(api_url)
response.raise_for_status()
data = response.json()
results = data.get("results", [])
values = results[0].get("values", []) if results else []
df_wynagrodzenie = pd.DataFrame(values)[["year", "val"]]

#funkcja do otworzenia z adresu api strony NBP by otrzymac kursy walut dla danego roku
def kursy_data(waluty, rok):
    kursy = [] #lista na zapisanie kursów
    for waluta in waluty: #jeśli jest wiecej niż jedna waluta dla przeliczenia wynagrodzenia ta dunkcja to uwzględnia
        url = f'https://api.nbp.pl/api/exchangerates/rates/a/{waluta}/{rok}-01-01/{rok}-12-13/?format=json' #adres na pobranie walut
        response = requests.get(url, headers={'Accept': 'application/json'})

        if response.status_code == 200:
            data_json = response.json()
            for rate in data_json['rates']: #dla kazdej raty zapisuje datę, jaka waluta i kurs
                kursy.append({
                    'Data': rate['effectiveDate'],
                    'Waluta': waluta,
                    'Kurs': rate['mid']
                })
        else:
            print(f"Error fetching data for currency: {waluta}")
    df = pd.DataFrame(kursy) #przkestzałceni listy na ramkę danych
    return df

def przeliczenie_wynagrodzenia(rok_p, rok_k):
    #funkcja na obliczenie wynagrodzenia na kazdego możłiwego dnia z lat (od rok_p do rok_k)
    df_wynagrodzenie['val'] = df_wynagrodzenie['val'].astype(float) #zamiana formatu danych na poprawny

    waluty = ['jpy', 'usd']#lista walut
    wynagrodzenia_lista = []#pusta lidta potrzebna do zapisania wynagrodzeń
    kursy_lista=[]#pusta lista do zapisanie kursów

    for rok in range(rok_p, rok_k+1):#petla gdzie rok przyjmuje dane od roku_p do roku_k włącznie
        df_kursy = kursy_data(waluty, rok) #zapisanie wyników z funkcji
        df_kursy['Rok'] = rok #dodanie nowej zmiennej do ramki danych z informacja o roku
        kursy_lista.append(df_kursy) #dodanie nowych wartosci do listy

    df_kursy_all = pd.concat(kursy_lista, ignore_index=True) #zapisanie listy jako ramki danych 
    #ramka danych zawiera wszytskie kursy ze wszystkimi datami dla tego okresu dla dwóch walut

    wynagrodzenia_lista = []#pusta lista do zapisania informacji

    for rok in range(rok_p, rok_k + 1): #petla gdzie rok przyjmuje dane od roku_p do roku_k włącznie
        wynagrodzenie_miesięczne = df_wynagrodzenie.loc[df_wynagrodzenie['year'] == str(rok), 'val'].iloc[0]#zapisanie wartości wynagrodzenia z ramki z wynagrodzenia dla danego roku
        df_kursy_rok = df_kursy_all[df_kursy_all['Rok'] == rok] #pobranie częsci tabeli dla której rok zgadza się z danym rokiem
        for _, row in df_kursy_rok.iterrows(): #iterowanie po wierszach
            kurs = row['Kurs'] #zapisanie wiersza z kursem pod nową wartoscia
            waluta = row['Waluta'] #podobnie jak dla kursu tylko, że dla waluty
            wynagrodzenie = wynagrodzenie_miesięczne / kurs #obliczenie wynagrodzenia względem danego kursu
            wynagrodzenia_lista.append({ #stworzenie nowego słownika z danymi zmiennymi i obserwacjami
                'Data': row['Data'],
                'Waluta': waluta,
                'Kurs': kurs,
                'Rok': rok,
                'Wynagrodzenie_Miesięczne': wynagrodzenie
            })

    df_wyniki = pd.DataFrame(wynagrodzenia_lista) #zapisanie danych z listy w formie ramki danych

    #podział ramki danych na dwa względem waluty, ponieważ ze względów estetycznych i formalnych należy dać różną skalę dla waluty
    df_jpy = df_wyniki[df_wyniki['Waluta'] == 'jpy'] #jpy
    df_usd = df_wyniki[df_wyniki['Waluta'] == 'usd'] #usd

    #zagwarantowanie poprawnego formatu daty - potrzbene do osi x w wykresie
    df_jpy.loc[:, 'Data'] = pd.to_datetime(df_jpy['Data'], errors='coerce')
    df_usd.loc[:, 'Data'] = pd.to_datetime(df_usd['Data'], errors='coerce')
    
    #wizualizacja danych
    #rozmiar wykresu 
    # z powodu dwóch róznych skali należy podzielić wykres na dwa etapy ax1 dla jpy i ax2 dla usd
    # na ten pierwszy nakładamy linie tego drugiego
    fig, ax1 = plt.subplots(figsize=(10, 6))

    #wykres dla jpy, gdzie x to data a wartości to wynagrodzenia_miesięczne
    ax1.plot(df_jpy['Data'], df_jpy['Wynagrodzenie_Miesięczne'], label='JPY', color='darkred')
    ax1.set_xlabel('Rok') #nazwa osi x
    ax1.set_ylabel('Wynagrodzenie Miesięczne (JPY)', color='darkred') #nazwa osi y dla jpy
    ax1.tick_params(axis='y', labelcolor='darkred')

    #foramtowanie osi y by wykres ył czytelny i wyświetlało tylko rok, zamiast wielu dat
    ax1.xaxis.set_major_formatter(mdates.DateFormatter('%Y')) #formatowanie zmiennej na rok
    ax1.xaxis.set_major_locator(mdates.YearLocator(base=2)) #co dwa lata ma pokazywać się rok
    plt.xticks(rotation=45) #mają być pod kątem 45 stopnii

    #wykres dla usd - podobny dla jpy
    ax2 = ax1.twinx() #zapewnia to ze oś x da dwóch wykresów jest ta sama
    ax2.plot(df_usd['Data'], df_usd['Wynagrodzenie_Miesięczne'], label='USD', color='darkblue')
    ax2.set_ylabel('Wynagrodzenie Miesięczne (USD)', color='darkblue') #nazwa osi y dla usd
    ax2.tick_params(axis='y', labelcolor='darkblue')
    
    plt.title('Wynagrodzenie Miesięczne w JPY i USD w czasie') # tytuł wykresu
    plt.grid(True, color='gray', linestyle='--', linewidth=0.7) #dodajemy do wykresu siatkę
    plt.show() #pokazanie się wykresu
    return() #funkcja ma pokazywać wykres i nic innego nie zwracać
    
#wywołanie funkcji
df_all_kursy = przeliczenie_wynagrodzenia(2005, 2021)


