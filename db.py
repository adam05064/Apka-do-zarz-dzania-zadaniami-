import mysql.connector
from mysql.connector import Error
from task import Zadanie
import logging
import os

class Baza:
    def __init__(self):
        try:
            self.polaczenie = mysql.connector.connect(
                database=os.getenv("DB_NAME", "bazadanych"),
                user=os.getenv("DB_USER", "adam"),
                password=os.getenv("DB_PASSWORD", "adam"),
                host=os.getenv("DB_HOST", "192.168.1.16"),
                port=os.getenv("DB_PORT", "3306")
            )
            print("Połączono z bazą danych MariaDB!")
        except Error as e:
            print(f"Wystąpił błąd podczas łączenia z bazą danych MariaDB: {e}")
            self.polaczenie = None

    def pobierz_zadania(self):
        zadania = []
        if self.polaczenie:
            try:
                with self.polaczenie.cursor() as cur:
                    cur.execute("SELECT id, tytul, opis, data_realizacji, priorytet, ukonczone FROM zadania WHERE ukonczone = 0")
                    rows = cur.fetchall()
                    zadania = [Zadanie(*row) for row in rows]
            except Error as e:
                print(f"Wystąpił błąd podczas ładowania zadań: {e}")
        return zadania

    def dodaj_zadanie(self, tytul, opis, data_realizacji, priorytet):
        if self.polaczenie:
            try:
                with self.polaczenie.cursor() as cur:
                    cur.execute(
                        "INSERT INTO zadania (tytul, opis, data_realizacji, priorytet) VALUES (%s, %s, %s, %s)",
                        (tytul, opis, data_realizacji, priorytet)
                    )
                    self.polaczenie.commit()
                    return cur.lastrowid
            except Error as e:
                print(f"Wystąpił błąd podczas dodawania zadania: {e}")
        return None

    def edytuj_zadanie(self, id_zadania, tytul, opis, data_realizacji, priorytet):
        if self.polaczenie:
            try:
                with self.polaczenie.cursor() as cur:
                    cur.execute(
                        "UPDATE zadania SET tytul = %s, opis = %s, data_realizacji = %s, priorytet = %s WHERE id = %s",
                        (tytul, opis, data_realizacji, priorytet, id_zadania)
                    )
                    self.polaczenie.commit()
                    return True
            except Error as e:
                # Informuj użytkownika o błędzie
                messagebox.showerror("Błąd podczas edytowania zadania", f"Wystąpił błąd: {e}")
        else:
            messagebox.showerror("Błąd", "Brak połączenia z bazą danych.")
        return False

    def usun_zadanie(self, id_zadania):
        if self.polaczenie:
            try:
                with self.polaczenie.cursor() as cur:
                    cur.execute("UPDATE zadania SET ukonczone = 1 WHERE id = %s", (id_zadania,))
                    self.polaczenie.commit()
                    return True
            except Error as e:
                print(f"Wystąpił błąd podczas usuwania zadania: {e}")
        return False

    def zakoncz_zadanie(self, id_zadania):
        if self.polaczenie:
            try:
                with self.polaczenie.cursor() as cur:
                    cur.execute("UPDATE zadania SET ukonczone = 1 WHERE id = %s", (id_zadania,))
                    self.polaczenie.commit()
                    return True
            except Error as e:
                print(f"Wystąpił błąd podczas oznaczania zadania jako ukończone: {e}")
        return False

    def __del__(self):
        if self.polaczenie:
            self.polaczenie.close()
            print("Połączenie z bazą danych zostało zamknięte.")
