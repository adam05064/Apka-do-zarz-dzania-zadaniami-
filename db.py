import mysql.connector
from mysql.connector import Error
from task import Zadanie

class Baza:
    def __init__(self):
        try:
            self.polaczenie = mysql.connector.connect(
                database="BazaZZ",
                user="adam",
                password="adam",
                host="172.29.37.125",
                port="3306"
            )
            print("Połączono z bazą danych MariaDB!")
        except Error:
            print("Wystąpił błąd podczas łączenia z bazą danych MariaDB:")
            self.polaczenie = None

    def pobierz_zadania(self):
        zadania = []
        if self.polaczenie:
            try:
                cur = self.polaczenie.cursor()
                cur.execute("SELECT id, tytul, opis, data_realizacji, priorytet, ukonczone FROM zadania WHERE ukonczone = 0")
                rows = cur.fetchall()
                zadania = [Zadanie(*row) for row in rows]
            except Error as e:
                print("Wystąpił błąd podczas ładowania zadań:")
        return zadania

    def dodaj_zadanie(self, tytul, opis, data_realizacji, priorytet):
        if self.polaczenie:
            try:
                cur = self.polaczenie.cursor()
                cur.execute(
                    "INSERT INTO zadania (tytul, opis, data_realizacji, priorytet) VALUES (%s, %s, %s, %s)",
                    (tytul, opis, data_realizacji, priorytet)
                )
                self.polaczenie.commit()
                return cur.lastrowid
            except Error:
                print("Wystąpił błąd podczas dodawania zadania:")
        return None

    def edytuj_zadanie(self, id_zadania, tytul, opis, data_realizacji, priorytet):
        if self.polaczenie:
            try:
                cur = self.polaczenie.cursor()
                cur.execute(
                    "UPDATE zadania SET tytul = %s, opis = %s, data_realizacji = %s, priorytet = %s WHERE id = %s",
                    (tytul, opis, data_realizacji, priorytet, id_zadania)
                )
                self.polaczenie.commit()
                return True
            except Error:
                print("Wystąpił błąd podczas edytowania zadania:")
        return False

    def usun_zadanie(self, id_zadania):
        if self.polaczenie:
            try:
                cur = self.polaczenie.cursor()
                cur.execute("UPDATE zadania SET ukonczone = 1 WHERE id = %s", (id_zadania,))
                self.polaczenie.commit()
                return True
            except Error:
                print("Wystąpił błąd podczas usuwania zadania:")
        return False

    def zakoncz_zadanie(self, id_zadania):
        if self.polaczenie:
            try:
                cur = self.polaczenie.cursor()
                cur.execute("UPDATE zadania SET ukonczone = 1 WHERE id = %s", (id_zadania,))
                self.polaczenie.commit()
                return True
            except Error:
                print("Wystąpił błąd podczas oznaczania zadania jako ukończone:")
        return False

    def __del__(self):
        if self.polaczenie:
            self.polaczenie.close()
            print("Połączenie z bazą danych zostało zamknięte.")
