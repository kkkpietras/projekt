import tkinter as tk
from datetime import datetime
from sqlalchemy import create_engine, func
from sqlalchemy.orm import sessionmaker
from bazadanychall import Dane
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

#

def pobierz_zakres_dat(sensorid):
    engine = create_engine('sqlite:///stacje.db', echo=True)
    Session = sessionmaker(bind=engine)
    session = Session()

    min_date = session.query(func.min(Dane.date)).filter_by(sensor_id=sensorid).scalar()
    max_date = session.query(func.max(Dane.date)).filter_by(sensor_id=sensorid).scalar()

    if min_date is None or max_date is None:
        info = "Brak dostępnych danych w bazie dla sensora {}".format(sensorid)
    else:
        info = "Dostępne dane w bazie dla sensora {}:\n".format(sensorid)
        info += "Najwcześniejsza data: {}\n".format(min_date.strftime('%Y-%m-%d'))
        info += "Najpóźniejsza data: {}\n".format(max_date.strftime('%Y-%m-%d'))
        #
        # date_poczatkowa, date_koncowa = pobierz_zakres_dat(min_date, max_date)
        # info += "\nWybrany zakres dat:\n"
        # info += "Data początkowa: {}\n".format(date_poczatkowa.strftime('%Y-%m-%d'))
        # info += "Data końcowa: {}".format(date_koncowa.strftime('%Y-%m-%d'))



    session.close()

    root = tk.Tk()
    root.title("Wyniki")
    root.geometry("300x200")

    label_info = tk.Label(root, text=info)
    label_info.pack()

    # button_wykres = tk.Button(root, text="Wykres",
    #                           command=lambda: wyswietl_wykres(sensorid, date_poczatkowa, date_koncowa))
    # button_wykres.pack()







    def zatwierdz():
        global date_poczatkowa, date_koncowa
        date_poczatkowa = datetime.strptime(entry_poczatkowa.get(), "%Y-%m-%d")
        date_koncowa = datetime.strptime(entry_koncowa.get(), "%Y-%m-%d")
        if date_poczatkowa < min_date:
            date_poczatkowa = min_date
        if date_koncowa > max_date:
            date_koncowa = max_date
        analiza_danych(sensorid, date_poczatkowa, date_koncowa)
        #root.destroy()

    # root = tk.Tk()
    # root.title("Podaj zakres dat")
    # root.geometry("300x200")

    label_poczatkowa = tk.Label(root, text="Data początkowa (RRRR-MM-DD):")
    label_poczatkowa.pack()

    default_poczatkowa = min_date.strftime("%Y-%m-%d") if min_date else ""
    entry_poczatkowa = tk.Entry(root)
    entry_poczatkowa.insert(0, default_poczatkowa)
    entry_poczatkowa.pack()

    label_koncowa = tk.Label(root, text="Data końcowa (RRRR-MM-DD):")
    label_koncowa.pack()

    default_koncowa = max_date.strftime("%Y-%m-%d") if max_date else ""
    entry_koncowa = tk.Entry(root)
    entry_koncowa.insert(0, default_koncowa)
    entry_koncowa.pack()

    button_zatwierdz = tk.Button(root, text="Zatwierdź", command=zatwierdz)
    button_zatwierdz.pack()

    root.mainloop()

    return date_poczatkowa, date_koncowa




#def wypisz_dostepne_daty(sensorid):
    # engine = create_engine('sqlite:///stacje.db', echo=True)
    # Session = sessionmaker(bind=engine)
    # session = Session()
    #
    # min_date = session.query(func.min(Dane.date)).filter_by(sensor_id=sensorid).scalar()
    # max_date = session.query(func.max(Dane.date)).filter_by(sensor_id=sensorid).scalar()
    #
    # if min_date is None or max_date is None:
    #     info = "Brak dostępnych danych w bazie dla sensora {}".format(sensorid)
    # else:
    #     info = "Dostępne dane w bazie dla sensora {}:\n".format(sensorid)
    #     info += "Najwcześniejsza data: {}\n".format(min_date.strftime('%Y-%m-%d'))
    #     info += "Najpóźniejsza data: {}\n".format(max_date.strftime('%Y-%m-%d'))
    #     #
    #     date_poczatkowa, date_koncowa = pobierz_zakres_dat(min_date, max_date)
    #     info += "\nWybrany zakres dat:\n"
    #     info += "Data początkowa: {}\n".format(date_poczatkowa.strftime('%Y-%m-%d'))
    #     info += "Data końcowa: {}".format(date_koncowa.strftime('%Y-%m-%d'))
    #
    #     analiza_danych(sensorid, date_poczatkowa, date_koncowa)
    #
    # session.close()
    #
    # root = tk.Tk()
    # root.title("Wyniki")
    # root.geometry("300x200")
    #
    # label_info = tk.Label(root, text=info)
    # label_info.pack()
    #
    # # button_wykres = tk.Button(root, text="Wykres",
    # #                           command=lambda: wyswietl_wykres(sensorid, date_poczatkowa, date_koncowa))
    # # button_wykres.pack()
    #
    # root.mainloop()


def analiza_danych(sensorid, data_poczatkowa, data_koncowa):
    engine = create_engine('sqlite:///stacje.db', echo=True)
    Session = sessionmaker(bind=engine)
    session = Session()

    # Wykonaj zapytanie do bazy danych, aby otrzymać wartości dla zadanego zakresu dat i określonego sensora
    result = session.query(Dane).filter(
        Dane.sensor_id == sensorid,
        Dane.date >= data_poczatkowa,
        Dane.date <= data_koncowa
    ).all()

    if not result:
        info = "Brak danych w podanym zakresie dla sensora {}".format(sensorid)
    else:
        df = pd.DataFrame([(row.date, row.value) for row in result], columns=['date', 'value'])
        min_value = round(df['value'].min(), 2)
        max_value = round(df['value'].max(), 2)
        min_date = df.loc[df['value'].idxmin(), 'date']
        max_date = df.loc[df['value'].idxmax(), 'date']
        avg_value = round(df['value'].mean(), 2)

        values = df['value'].values
        indices = np.arange(len(values))
        correlation = round(np.corrcoef(values, indices)[0, 1], 2)

        info = "Analiza danych dla sensora {}\n".format(sensorid)
        info += "Najmniejsza wartość: {} (Data: {})\n".format(min_value, min_date)
        info += "Największa wartość: {} (Data: {})\n".format(max_value, max_date)
        info += "Średnia wartość: {}\n".format(avg_value)
        info += "Współczynnik korelacji Pearsona: {}".format(correlation)

    session.close()

    wypisz_wyniki_analizy(info, sensorid)


def wypisz_wyniki_analizy(info,sensorid):
    # root = tk.Tk()
    # root.title("Wyniki analizy")
    # root.geometry("300x200")
    #
    # label_info = tk.Label(root, text=info)
    # label_info.pack()
    # button_wykres = tk.Button(root, text="Wykres",
    #                           command=lambda: wyswietl_wykres(sensorid, date_poczatkowa, date_koncowa))
    # button_wykres.pack()

    new_window = tk.Toplevel()
    new_window.title("Wyniki analizy")
    new_window.geometry("300x200")

    label_info = tk.Label(new_window, text=info)
    label_info.pack()

    button_wykres = tk.Button(new_window, text="Wykres",
                              command=lambda: wyswietl_wykres(sensorid, date_poczatkowa, date_koncowa))
    button_wykres.pack()


def wyswietl_wykres(sensorid, data_poczatkowa, data_koncowa):
    engine = create_engine('sqlite:///stacje.db', echo=True)
    Session = sessionmaker(bind=engine)
    session = Session()

    # Wykonaj zapytanie do bazy danych, aby otrzymać wartości dla zadanego zakresu dat i określonego sensora
    result = session.query(Dane).filter(
        Dane.sensor_id == sensorid,
        Dane.date >= data_poczatkowa,
        Dane.date <= data_koncowa
    ).all()

    if not result:
        print("Brak danych w podanym zakresie dla sensora", sensorid)
    else:
        df = pd.DataFrame([(row.date, row.value) for row in result], columns=['date', 'value'])
        df['date'] = pd.to_datetime(df['date'])

        # Generuj wykres punktowy
        plt.scatter(df['date'], df['value'])
        plt.xlabel('Data')
        plt.ylabel('Wartość')
        plt.title('Wykres punktowy')

        # Wyświetl wykres
        plt.show()

    session.close()

if __name__ == '__main__':

    # Przykładowe użycie:
    # data_poczatkowa = datetime.strptime('2023-01-01', '%Y-%m-%d')
    # data_koncowa = datetime.strptime('2023-12-31', '%Y-%m-%d')

   sensorid = 644
   pobierz_zakres_dat(sensorid)

