import tkinter as tk
from tkinter import ttk

class ZarzadzanieZadaniamiUI:
    def __init__(self, root, kontroler):
        self.root = root
        self.kontroler = kontroler
        self.root.title("Zarządzanie Zadaniami")
        self.root.geometry("600x400")
        self.root.configure(bg='#f0f0f0')  # Ustawienie koloru tła

        # Inicjalizacja stylu
        style = ttk.Style()
        style.theme_use('clam')  # Użycie motywu 'clam'

        self.lista_zadan = tk.Listbox(root, width=50, height=20)
        self.lista_zadan.pack(side=tk.LEFT, fill=tk.BOTH, padx=10, pady=10)

        button_frame = tk.Frame(root, bg='#f0f0f0')  # Dodanie tła do ramki
        button_frame.pack(side=tk.RIGHT, fill=tk.Y, padx=10, pady=10)

        dodaj_przycisk = ttk.Button(button_frame, text="Dodaj Zadanie", command=lambda: self.kontroler.dodaj_lub_edytuj_zadanie())
        dodaj_przycisk.pack(fill=tk.X, pady=5)

        edytuj_przycisk = ttk.Button(button_frame, text="Edytuj Zadanie", command=self.kontroler.edytuj_zadanie)
        edytuj_przycisk.pack(fill=tk.X, pady=5)

        usun_przycisk = ttk.Button(button_frame, text="Usuń Zadanie", command=self.kontroler.usun_zadanie)
        usun_przycisk.pack(fill=tk.X, pady=5)

        zakoncz_przycisk = ttk.Button(button_frame, text="Zakończ Zadanie", command=self.kontroler.zakoncz_zadanie)
        zakoncz_przycisk.pack(fill=tk.X, pady=5)

        # Dodaj przycisk do wyświetlania szczegółów zadania
        szczegoly_przycisk = ttk.Button(button_frame, text="Pokaż Szczegóły", command=self.pokaz_szczegoly)
        szczegoly_przycisk.pack(fill=tk.X, pady=5)

    def aktualizuj_liste_zadan(self, zadania):
        self.lista_zadan.delete(0, tk.END)
        for zadanie in zadania:
            self.lista_zadan.insert(tk.END, zadanie.title)

    def pokaz_szczegoly(self):
        wybrany_index = self.lista_zadan.curselection()
        if wybrany_index:
            zadanie = self.kontroler.zadania[wybrany_index[0]]  # Wyciągnij pierwszy indeks
            self.kontroler.pokaz_szczegoly_zadania(zadanie)

