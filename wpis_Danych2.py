import requests
import json
from sqlalchemy import create_engine, func
from sqlalchemy.orm import sessionmaker
from requests.exceptions import RequestException
from bazadanychall import Base, Stacje, Stanowiska, Dane, Indeks
from sqlalchemy import text
from datetime import datetime

def add_dane(sensorid, dane):
    engine = create_engine('sqlite:///stacje.db', echo=True)
    Session = sessionmaker(bind=engine)
    session = Session()

    s = Dane(sensor_id=sensorid, key=dane['key'], date=dane['values']['date'], value=dane['values']['value'])

    session.add(s)
    session.commit()

    session.close()

# def wpisz_dane(sensorid):
#     try:
#         res = requests.get(f"https://api.gios.gov.pl/pjp-api/rest/data/getData/{sensorid}")
#         res.raise_for_status()
#         packages_json = res.json()
#
#         packages_dict = []
#
#         if isinstance(packages_json, list):
#             packages_dict = packages_json
#         elif isinstance(packages_json, dict):
#             packages_dict.append(packages_json)
#
#         engine = create_engine('sqlite:///stacje.db', echo=True)
#         Session = sessionmaker(bind=engine)
#         session = Session()
#
#         Base.metadata.create_all(engine)
#
#         for package in packages_dict:
#             key = package.get('key')
#             values = package.get('values')
#
#             if isinstance(values, list):
#                 for value in values:
#                     date_str = value.get('date')
#                     date = datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S")
#                     if value.get('value') is not None:
#                         val = float(value.get('value'))
#
#                     # Sprawdzenie czy wpis istnieje w bazie danych
#                     existing_entry = session.query(Dane).filter_by(sensor_id=sensorid, date=date).first()
#                     if existing_entry:
#                         continue
#
#                     p = Dane(sensor_id=sensorid, key=key, date=date, value=val)
#                     session.add(p)
#             elif isinstance(values, dict):
#                 date_str = values.get('date')
#                 date = datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S")
#                 val = values.get('value')
#
#                 # Sprawdzenie czy wpis istnieje w bazie danych
#                 existing_entry = session.query(Dane).filter_by(sensor_id=sensorid, date=date).first()
#                 if existing_entry:
#                     continue
#
#                 p = Dane(sensor_id=sensorid, key=key, date=date, value=val)
#                 session.add(p)
#
#         session.commit()
#         session.close()
#
#     except RequestException as e:
#         print('Wystąpił błąd podczas żądania:', str(e))
#     except json.JSONDecodeError as e:
#         print('Błąd dekodowania odpowiedzi JSON:', str(e))


def wpisz_dane(sensorid):
    try:
        res = requests.get(f"https://api.gios.gov.pl/pjp-api/rest/data/getData/{sensorid}")
        res.raise_for_status()
        packages_json = res.json()

        packages_dict = []

        if isinstance(packages_json, list):
            packages_dict = packages_json
        elif isinstance(packages_json, dict):
            packages_dict.append(packages_json)

        engine = create_engine('sqlite:///stacje.db', echo=True)
        Session = sessionmaker(bind=engine)
        session = Session()

        Base.metadata.create_all(engine)

        for package in packages_dict:
            key = package.get('key')
            values = package.get('values')

            if isinstance(values, list):
                for value in values:
                    date_str = value.get('date')
                    date = datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S")
                    val = value.get('value')

                    if val is not None:
                        val = float(val)

                    # Sprawdzenie czy wpis istnieje w bazie danych
                    existing_entry = session.query(Dane).filter_by(sensor_id=sensorid, date=date).first()
                    if existing_entry:
                        continue

                    p = Dane(sensor_id=sensorid, key=key, date=date, value=val)
                    session.add(p)
            elif isinstance(values, dict):
                date_str = values.get('date')
                date = datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S")
                val = values.get('value')

                if val is not None:
                    val = float(val)

                # Sprawdzenie czy wpis istnieje w bazie danych
                existing_entry = session.query(Dane).filter_by(sensor_id=sensorid, date=date).first()
                if existing_entry:
                    continue

                p = Dane(sensor_id=sensorid,
                         key=key, date=date, value=val)
                session.add(p)

        session.commit()
        session.close()

    except RequestException as e:
        print('Wystąpił błąd podczas żądania:', str(e))
    except json.JSONDecodeError as e:
        print('Błąd dekodowania odpowiedzi JSON:', str(e))


def wypisz_dostepne_daty(sensorid):
    engine = create_engine('sqlite:///stacje.db', echo=True)
    Session = sessionmaker(bind=engine)
    session = Session()

    min_date = session.query(func.min(Dane.date)).filter_by(sensor_id=sensorid).scalar()
    max_date = session.query(func.max(Dane.date)).filter_by(sensor_id=sensorid).scalar()

    if min_date is None or max_date is None:
        print("Brak dostępnych danych w bazie dla sensora", sensorid)
    else:
        print("Dostępne dane w bazie dla sensora", sensorid, ":")
        print("Najwcześniejsza data:", min_date.strftime('%Y-%m-%d'))
        print("Najpóźniejsza data:", max_date.strftime('%Y-%m-%d'))

    session.close()




def pobierz_zakres_dat(min_date, max_date):
    while True:
        date_poczatkowa_str = input("Podaj datę początkową (RRRR-MM-DD): ")
        date_koncowa_str = input("Podaj datę końcową (RRRR-MM-DD): ")

        try:
            date_poczatkowa = datetime.strptime(date_poczatkowa_str, "%Y-%m-%d")
            date_koncowa = datetime.strptime(date_koncowa_str, "%Y-%m-%d")

            if date_poczatkowa < min_date:
                print("Podana data początkowa jest wcześniejsza niż minimalna dostępna data. Ustawiono datę początkową na:", min_date.strftime('%Y-%m-%d'))
                date_poczatkowa = min_date

            if date_koncowa > max_date:
                print("Podana data końcowa jest późniejsza niż maksymalna dostępna data. Ustawiono datę końcową na:", max_date.strftime('%Y-%m-%d'))
                date_koncowa = max_date

            return date_poczatkowa, date_koncowa

        except ValueError:
            print("Nieprawidłowy format daty. Spróbuj ponownie.")


def wypisz_dostepne_daty(sensorid):
    engine = create_engine('sqlite:///stacje.db', echo=True)
    Session = sessionmaker(bind=engine)
    session = Session()

    min_date = session.query(func.min(Dane.date)).filter_by(sensor_id=sensorid).scalar()
    max_date = session.query(func.max(Dane.date)).filter_by(sensor_id=sensorid).scalar()

    if min_date is None or max_date is None:
        print("Brak dostępnych danych w bazie dla sensora", sensorid)
    else:
        print("Dostępne dane w bazie dla sensora", sensorid, ":")
        print("Najwcześniejsza data:", min_date.strftime('%Y-%m-%d'))
        print("Najpóźniejsza data:", max_date.strftime('%Y-%m-%d'))

        date_poczatkowa, date_koncowa = pobierz_zakres_dat(min_date, max_date)
        print("Wybrany zakres dat:")
        print("Data początkowa:", date_poczatkowa.strftime('%Y-%m-%d'))
        print("Data końcowa:", date_koncowa.strftime('%Y-%m-%d'))

    session.close()





if __name__ == '__main__':
    wypisz_dostepne_daty(644)
