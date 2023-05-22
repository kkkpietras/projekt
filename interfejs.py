import tkinter as tk
from sqlalchemy import create_engine

import lista_sensorow_stacji
from bazadanychall import Base
import import_stacje3
from pobierz_liste_stacji2 import display_stations
import lista_stacji_w_miejscowosci2
import znajdz_stacje_promien
import wpis_Danych2
import okienko_analiza2
import mapa_stacji

def create_database():
    # Tworzenie silnika bazy danych SQLite
    engine = create_engine('sqlite:///stacje.db', echo=True)

    # Utworzenie tabel w bazie danych
    Base.metadata.create_all(engine)

    # Wyświetlenie informacji o utworzeniu bazy danych
    print("Pusta baza danych została utworzona.")

def on_button_click():
    create_database()

def on_button2_click():
    import_stacje3.wpisz_stacje()

def display_string():
    string = display_stations()
    new_window = tk.Toplevel(root)  # Tworzenie nowego okna
    text_area = tk.Text(new_window, height=10, width=50)  # Tworzenie pola tekstowego
    text_area.insert(tk.END, string)
    text_area.pack(fill=tk.BOTH, expand=True)  # Ustawianie wypełnienia i rozszerzania na całe okno

def display_string2(city):
    results = lista_stacji_w_miejscowosci2.display_stations2(city)

    if not results:
        text_area.delete("1.0", tk.END)
        text_area.insert(tk.END, "Nie znaleziono informacji o stacj ach w podanym mieście.")
        return

    column_widths = [20, 20, 30]
    string = f'{"MIASTO":<{column_widths[0]}} {"ID STACJI":<{column_widths[1]}} {"ADRES":<{column_widths[2]}}\n'
    for row in results:
        miasto = row[5] if row[5] is not None else ""
        id_stacji = str(row[1]) if row[1] is not None else ""
        adres = row[9] if row[9] is not None else ""
        string += f'{miasto:<{column_widths[0]}} {id_stacji:<{column_widths[1]}} {adres:<{column_widths[2]}}\n'

    text_area.delete("1.0", tk.END)
    text_area.insert(tk.END, string)


def display_string3(idstacja):
    #results = lista_stacji_w_miejscowosci2.display_stations2(city)
    results = lista_sensorow_stacji.display_sensory(idstacja)

    # if not results:
    #     text_area.delete("1.0", tk.END)
    #     text_area.insert(tk.END, "Nie znaleziono informacji o stacjach w podanej stacji.")
    #     return

    if results:
        text_area.delete("1.0", "end")
        text_area.insert("end", f"***Dostępne stanowiska pomiarowe dla stacji o id {idstacja}:\n")
        text_area.insert("end", "{:<10s} {:<20s}\n".format("ID stanowiska", "Nazwa parametru"))
        text_area.insert("end", "-" * 30 + "\n")
        for result in results:
            text_area.insert("end", "{:<10s} {:<20s}\n".format(str(result[1]), result[3]))
    else:
        text_area.delete("1.0", "end")
        text_area.insert("end", "Nie znaleziono informacji o stanowiskach pomiarowych dla podanej stacji.")



    # column_widths = [20, 20, 30]
    # string = f'{"MIASTO":<{column_widths[0]}} {"ID STACJI":<{column_widths[1]}} {"ADRES":<{column_widths[2]}}\n'
    # for row in results:
    #     miasto = row[5] if row[5] is not None else ""
    #     id_stacji = str(row[1]) if row[1] is not None else ""
    #     adres = row[9] if row[9] is not None else ""
    #     string += f'{miasto:<{column_widths[0]}} {id_stacji:<{column_widths[1]}} {adres:<{column_widths[2]}}\n'
    #
    # text_area.delete("1.0", tk.END)
    # text_area.insert(tk.END, string)

def wpisz_dane_do_bazy(sesorid):
    wpis_Danych2.wpisz_dane(sesorid)





def open_new_window():
    new_window = tk.Toplevel(root)
    new_window.title("Wyszukiwanie stacji w mieście")

    label = tk.Label(new_window, text="Podaj nazwę miasta:")
    label.pack()

    entry = tk.Entry(new_window)
    entry.pack()

    button5 = tk.Button(new_window, text="Wyświetl stacje", command=lambda: display_string2(entry.get()))
    button5.pack()

def open_new_window2():
    def search_button_click():
        location = location_entry.get()
        radius = float(radius_entry.get())

        # Wywołanie funkcji search_stations z podanymi parametrami
        result = znajdz_stacje_promien.search_stations(location, radius)

        # Wyświetlanie wyników w oknie aplikacji
        if result:
            result
            result_text.delete(1.0, tk.END)
            result_text.insert(tk.END, f'Stacje w promieniu {radius} km od {location}:\n')
            for station in result:
                station_name, distance = station
                result_text.insert(tk.END, f'{station_name} - {distance:.2f} km\n')
        else:
            result_text.delete(1.0, tk.END)
            result_text.insert(tk.END, 'Nie znaleziono stacji w zadanym promieniu.')

    new_window = tk.Toplevel(root)
    new_window.title("Wyszukiwanie stacji")

    # Tworzenie etykiety i pola tekstowego dla lokalizacji
    location_label = tk.Label(new_window, text='Lokalizacja:')
    location_label.pack()
    location_entry = tk.Entry(new_window)
    location_entry.pack()

    # Tworzenie etykiety i pola tekstowego dla promienia
    radius_label = tk.Label(new_window, text='Promień (km):')
    radius_label.pack()
    radius_entry = tk.Entry(new_window)
    radius_entry.pack()

    # Tworzenie przycisku wyszukiwania
    search_button = tk.Button(new_window, text='Wyszukaj', command=search_button_click)
    search_button.pack()

    # Tworzenie pola tekstowego na wyniki
    result_text = tk.Text(new_window)
    result_text.pack()


def open_new_window3():
    new_window = tk.Toplevel(root)
    new_window.title("Wyszukiwanie senserów w stacji")

    label = tk.Label(new_window, text="Podaj ID stacji:")
    label.pack()

    entry = tk.Entry(new_window)
    entry.pack()

    button5 = tk.Button(new_window, text="Wyświetl sensory", command=lambda: display_string3(entry.get()))
    button5.pack()

def open_new_window4():
    new_window = tk.Toplevel(root)
    new_window.title("Dane pomiarowe")

    label = tk.Label(new_window, text="Podaj ID sensora:")
    label.pack()

    entry = tk.Entry(new_window)
    entry.pack()

    button9 = tk.Button(new_window, text="Wpisz dane do bazy danych", command=lambda: wpisz_dane_do_bazy(entry.get()))
    button9.pack()

    button10 = tk.Button(new_window, text="Analiza danych pomiarowych", command=lambda: okienko_analiza2.pobierz_zakres_dat(entry.get()))
    button10.pack()


def mapa():
    mapa_stacji.create_map()
    mapa_stacji.display_map()




root = tk.Tk()

button = tk.Button(root, text="Utwórz bazę danych", command=on_button_click)
button.pack()

button2 = tk.Button(root, text="Importuj STACJE do bazy danych", command=on_button2_click)
button2.pack()

button3 = tk.Button(root, text="Lista stacji w Polsce!", command=display_string)
button3.pack()

button4 = tk.Button(root, text="Wyszukaj w miejscowości", command=open_new_window)
button4.pack()

button6 = tk.Button(root, text="Wyszukaj w promieniu", command=open_new_window2)
button6.pack()

button7 = tk.Button(root, text="Wypisz sensory", command=open_new_window3)
button7.pack()

button8 = tk.Button(root, text="Dane pomiarowe", command=open_new_window4)
button8.pack()

button12 = tk.Button(root, text="Mapa stacji", command=mapa)
button12.pack()




text_area = tk.Text(root, height=10, width=50)
text_area.pack()

root.mainloop()
