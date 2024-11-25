import mysql.connector
import time
import smtplib
from tkinter import simpledialog, messagebox
from task import Zadanie
from ui import ZarzadzanieZadaniamiUI
from email.mime.text import MIMEText
from email import utils  # This will now raise an ImportError
from wyslanie import EmailSender  # Zastąp 'email_sender' nazwą pliku, w którym znajduje się klasa


class ZarzadzanieZadaniami:

    def __init__(self, root):
        smtp_server = "smtp.example.com"  # Replace with your SMTP server
        port = 587  # Usually 587 for TLS
        sender_email = "your_email@example.com"  # Replace with your sender email
        password = "your_password"  # Replace with your email password

        self.email_sender = EmailSender(smtp_server, port, sender_email, password)
        # Połączenie z bazą danych MariaDB
        try:
            self.conn = mysql.connector.connect(
                database="bazadanych",
                user="adam",
                password="adam",
                host="192.168.1.16",
                port="3306"
            )
            messagebox.showinfo("Baza", "Połączono z Bazą")
        except mysql.connector.Error:
            messagebox.showinfo("Baza", "Wystąpił błąd podczas łączenia z bazą danych MariaDB")
            self.conn = None

        self.ui = ZarzadzanieZadaniamiUI(self.root, self)
        self.wczytaj_zadania()

    def wczytaj_zadania(self):
        if self.conn is not None:
            try:
                cur = self.conn.cursor()
                cur.execute("SELECT id, tytul, opis, data_realizacji, priorytet, ukonczone FROM zadania WHERE ukonczone = 0")
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
            priorytet = simpledialog.askstring("Priorytet zadania", "Wprowadź priorytet zadania (Niski, Średni, Wysoki):", initialvalue=zadanie.priority if zadanie else "Niski")

            if self.conn is not None:
                try:
                    cur = self.conn.cursor()
                    if zadanie:
                        cur.execute(
                            "UPDATE zadania SET tytul = %s, opis = %s, data_realizacji = %s, priorytet = %s WHERE id = %s",
                            (tytul, opis, termin, priorytet, zadanie.id)
                        )
                        zadanie.title = tytul
                        zadanie.description = opis
                        zadanie.due_date = termin
                        zadanie.priority = priorytet
                    else:
                        cur.execute(
                            "INSERT INTO zadania (tytul, opis, data_realizacji, priorytet) VALUES (%s, %s, %s, %s)",
                            (tytul, opis, termin, priorytet)
                        )
                        self.conn.commit()
                        task_id = cur.lastrowid
                        nowe_zadanie = Zadanie(task_id, tytul, opis, termin, priorytet, False)
                        self.zadania.append(nowe_zadanie)
                    self.conn.commit()
                    self.ui.aktualizuj_liste_zadan(self.zadania)
                except mysql.connector.Error as e:
                    messagebox.showinfo("Błąd!",e)

    def edytuj_zadanie(self):
        wybrany_index = self.ui.lista_zadan.selection()
        if wybrany_index:
            zadanie = self.zadania[int(wybrany_index[0])]  # Pobierz wybrane zadanie

            # Okno dialogowe do edycji szczegółów zadania
            tytul = simpledialog.askstring("Edycja tytułu", "Podaj nowy tytuł:", initialvalue=zadanie.title)
            if tytul is not None:
                opis = simpledialog.askstring("Edycja opisu", "Podaj nowy opis:", initialvalue=zadanie.description)
                if opis is not None:
                    data_realizacji = simpledialog.askstring("Edycja daty realizacji",
                                                             "Podaj nową datę realizacji (YYYY-MM-DD):",
                                                             initialvalue=zadanie.due_date)
                    if data_realizacji is not None:
                        priorytet = simpledialog.askstring("Edycja priorytetu", "Podaj nowy priorytet:",
                                                           initialvalue=zadanie.priority)
                        if priorytet is not None:
                            # Zaktualizuj zadanie w bazie danych
                            if self.conn is not None:
                                try:
                                    cur = self.conn.cursor()
                                    cur.execute(
                                        "UPDATE zadania SET tytul = %s, opis = %s, data_realizacji = %s, priorytet = %s WHERE id = %s",
                                        (tytul, opis, data_realizacji, priorytet, zadanie.id)
                                    )
                                    self.conn.commit()
                                    # Zaktualizuj obiekt zadania
                                    zadanie.title = tytul
                                    zadanie.description = opis
                                    zadanie.due_date = data_realizacji
                                    zadanie.priority = priorytet
                                    # Aktualizuj listę zadań w UI
                                    self.ui.aktualizuj_liste_zadan(self.zadania)
                                except mysql.connector.Error as e:
                                    messagebox.showerror("Błąd", f"Wystąpił błąd podczas aktualizacji zadania: {e}")

    def pokaz_szczegoly_zadania(self, zadanie):
        szczegoly = (
            f"Tytuł: {zadanie.title}\n"
            f"Opis: {zadanie.description}\n"
            f"Data realizacji: {zadanie.due_date}\n"
            f"Priorytet: {zadanie.priority}\n"
            f"Ukończone: {'Tak' if zadanie.completed else 'Nie'}"
        )
        messagebox.showinfo("Szczegóły zadania", szczegoly)

    def usun_zadanie(self):
        wybrany_index = self.ui.lista_zadan.selection()  # Change this line
        if wybrany_index:
            zadanie = self.zadania[int(wybrany_index[0])]
            if self.conn is not None:
                try:
                    cur = self.conn.cursor()
                    cur.execute("UPDATE zadania SET ukonczone = 1 WHERE id = %s", (zadanie.id,))
                    self.conn.commit()
                    self.zadania = [z for z in self.zadania if z.id != zadanie.id]
                    self.ui.aktualizuj_liste_zadan(self.zadania)
                except mysql.connector.Error as e:
                    messagebox.showerror("Błąd", f"Wystąpił błąd podczas usuwania zadania: {e}")

    def zakoncz_zadanie(self):
        wybrany_index = self.ui.lista_zadan.selection()
        if wybrany_index:
            zadanie = self.zadania[int(wybrany_index[0])]
            zadanie.completed = True
            if self.conn is not None:
                try:
                    cur = self.conn.cursor()
                    cur.execute("UPDATE zadania SET ukonczone = 1 WHERE id = %s", (zadanie.id,))
                    self.conn.commit()
                    self.zadania = [z for z in self.zadania if z.id != zadanie.id]
                    self.ui.aktualizuj_liste_zadan(self.zadania)
                except mysql.connector.Error as e:
                    messagebox.showerror("Błąd", f"Wystąpił błąd podczas oznaczania zadania jako zakończone: {e}")
                finally:
                    messagebox.showinfo("Wiadomość", "Zadanie zostało zakończone.")
                    # Wysłanie e-maila
                    self.email_sender.send_email(
                        "Zakończenie zadania",
                        f"Zadanie '{zadanie.title}' zostało wykonane o {time.strftime('%Y-%m-%d %H:%M:%S')}.",
                        "adam.korzepa98@gmail.com"
                    )

