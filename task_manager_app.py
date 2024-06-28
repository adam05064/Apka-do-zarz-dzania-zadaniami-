import mysql.connector
from tkinter import simpledialog, messagebox
from task import Zadanie
from ui import ZarzadzanieZadaniamiUI

class ZarzadzanieZadaniami:
    def __init__(self, root):
        self.root = root
        self.root.title("Zarządzanie Zadaniami")
        self.zadania = []

        # Połączenie z bazą danych MariaDB
        try:
            self.conn = mysql.connector.connect(
                database="BazaZZ",
                user="adam",
                password="adam",
                host="172.22.136.205",
                port="3306"
            )
            print("Połączono z bazą danych MariaDB!")
        except mysql.connector.Error:
            print("Wystąpił błąd podczas łączenia z bazą danych MariaDB:")
            self.conn = None

        self.ui = ZarzadzanieZadaniamiUI(self.root, self)
        self.wczytaj_zadania()

    def wczytaj_zadania(self):
        if self.conn is not None:
            try:
                cur = self.conn.cursor()
                cur.execute("SELECT id, title, description, due_date, priority, completed FROM tasks WHERE completed = 0")
                rows = cur.fetchall()
                self.zadania = [Zadanie(*row) for row in rows]
                self.ui.aktualizuj_liste_zadan(self.zadania)
            except mysql.connector.Error:
                print("Wystąpił błąd podczas ładowania zadań:")

    def dodaj_lub_edytuj_zadanie(self, zadanie=None):
        tytul = simpledialog.askstring("Tytuł zadania", "Wprowadź tytuł zadania:", initialvalue=zadanie.title if zadanie else "")
        if tytul:
            opis = simpledialog.askstring("Opis zadania", "Wprowadź opis zadania:", initialvalue=zadanie.description if zadanie else "")
            termin = simpledialog.askstring("Termin zadania", "Wprowadź termin zadania (YYYY-MM-DD):", initialvalue=zadanie.due_date if zadanie else "")
            priorytet = simpledialog.askstring("Priorytet zadania", "Wprowadź priorytet zadania (Niski, Średni, Wysoki):", initialvalue=zadanie.priority if zadanie else "Średni")

            if self.conn is not None:
                try:
                    cur = self.conn.cursor()
                    if zadanie:
                        cur.execute(
                            "UPDATE tasks SET title = %s, description = %s, due_date = %s, priority = %s WHERE id = %s",
                            (tytul, opis, termin, priorytet, zadanie.id)
                        )
                        zadanie.title = tytul
                        zadanie.description = opis
                        zadanie.due_date = termin
                        zadanie.priority = priorytet
                    else:
                        cur.execute(
                            "INSERT INTO tasks (title, description, due_date, priority) VALUES (%s, %s, %s, %s)",
                            (tytul, opis, termin, priorytet)
                        )
                        self.conn.commit()
                        task_id = cur.lastrowid
                        nowe_zadanie = Zadanie(task_id, tytul, opis, termin, priorytet, False)
                        self.zadania.append(nowe_zadanie)
                    self.conn.commit()
                    self.ui.aktualizuj_liste_zadan(self.zadania)
                except mysql.connector.Error:
                    print("Wystąpił błąd podczas dodawania/edytowania zadania:")

    def usun_zadanie(self):
        wybrany_index = self.ui.lista_zadan.curselection()
        if wybrany_index:
            zadanie = self.zadania[wybrany_index[0]]
            if self.conn is not None:
                try:
                    cur = self.conn.cursor()
                    cur.execute("UPDATE tasks SET completed = 1 WHERE id = %s", (zadanie.id,))
                    self.conn.commit()
                    self.zadania = [z for z in self.zadania if z.id != zadanie.id]
                    self.ui.aktualizuj_liste_zadan(self.zadania)
                except mysql.connector.Error:
                    print("Wystąpił błąd podczas usuwania zadania:")

    def zakoncz_zadanie(self):
        wybrany_index = self.ui.lista_zadan.curselection()
        if wybrany_index:
            zadanie = self.zadania[wybrany_index[0]]
            zadanie.completed = True
            if self.conn is not None:
                try:
                    cur = self.conn.cursor()
                    cur.execute("UPDATE tasks SET completed = 1 WHERE id = %s", (zadanie.id,))
                    self.conn.commit()
                    self.zadania = [z for z in self.zadania if z.id != zadanie.id]
                    self.ui.aktualizuj_liste_zadan(self.zadania)
                except mysql.connector.Error:
                    print("Wystąpił błąd podczas oznaczania zadania jako zakończone:")
