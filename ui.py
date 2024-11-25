import tkinter as tk
from tkinter import ttk

class ZarzadzanieZadaniamiUI:
    def __init__(self, root, kontroler):
        self.root = root
        self.kontroler = kontroler
        self.root.title("Zarządzanie Zadaniami")
        self.root.geometry("800x600")
        self.root.configure(bg='#F0F0F0')  # Jasno-szare tło (prawie białe)

        # Inicjalizacja stylu
        self.style = ttk.Style()
        self.style.theme_use('clam')

        # Ustawienie stylu dla ramki (TFrame) z odpowiednim kolorem tła
        self.style.configure("TFrame", background='#F0F0F0')  # Ustawienie tła ramki

        # Nowoczesny, minimalistyczny styl przycisków z zaokrąglonymi krawędziami
        self.style.configure("TButton",
                             background='#E0E0E0',
                             foreground='#333333',
                             borderwidth=10,
                             relief="groove",
                             padding=10,
                             font=("Helvetica", 12, "bold"))

        # Zaokrąglone przyciski i zmiana koloru przy interakcji
        self.style.map("TButton",
                       background=[('active', '#CCCCCC')],  # Zmiana na jaśniejszy szary przy wciśnięciu
                       relief=[('active', 'flat')])

        # Listbox (nowoczesny styl)
        self.style.configure("Treeview",
                             borderwidth=0,
                             relief="groove",
                             background='#FFFFFF',  # Białe tło listy
                             foreground='#333333',  # Ciemnoszary tekst
                             rowheight=25,
                             fieldbackground='#FFFFFF',
                             font=("Helvetica", 10))
        self.style.map('Treeview', background=[('selected', '#E0E0E0')],  # Wybrany element zmienia kolor
                       foreground=[('selected', '#000000')])  # Ciemniejszy tekst na wybranych

        # Drzewo do wyświetlania listy zadań zamiast Listboxa
        columns = ('title',)
        self.lista_zadan = ttk.Treeview(root, columns=columns, show='tree')
        self.lista_zadan.heading('title', text='Lista Zadań')
        self.lista_zadan.pack(side=tk.LEFT, fill=tk.BOTH, padx=10, pady=10, expand=True)

        # Ramka na przyciski z jednolitym tłem (#F0F0F0)
        button_frame = ttk.Frame(root, style="TFrame")  # Ramka korzysta ze stylu "TFrame"
        button_frame.pack(side=tk.RIGHT, fill=tk.Y, padx=20, pady=20)

        # Nowoczesne przyciski
        dodaj_przycisk = ttk.Button(button_frame, text="Dodaj Zadanie", command=lambda: self.kontroler.dodaj_lub_edytuj_zadanie())
        dodaj_przycisk.pack(fill=tk.X, pady=10)

        edytuj_przycisk = ttk.Button(button_frame, text="Edytuj Zadanie", command=self.kontroler.edytuj_zadanie)
        edytuj_przycisk.pack(fill=tk.X, pady=10)

        usun_przycisk = ttk.Button(button_frame, text="Usuń Zadanie", command=self.kontroler.usun_zadanie)
        usun_przycisk.pack(fill=tk.X, pady=10)

        zakoncz_przycisk = ttk.Button(button_frame, text="Zakończ Zadanie", command=self.kontroler.zakoncz_zadanie)
        zakoncz_przycisk.pack(fill=tk.X, pady=10)

        szczegoly_przycisk = ttk.Button(button_frame, text="Pokaż Szczegóły", command=self.pokaz_szczegoly)
        szczegoly_przycisk.pack(fill=tk.X, pady=10)

    def aktualizuj_liste_zadan(self, zadania):
        for item in self.lista_zadan.get_children():
            self.lista_zadan.delete(item)  # Usuwanie poprzednich elementów
        for index, zadanie in enumerate(zadania):
            self.lista_zadan.insert('', 'end', iid=index, text=zadanie.title)

    def pokaz_szczegoly(self):
        wybrany_index = self.lista_zadan.selection()
        if wybrany_index:
            zadanie = self.kontroler.zadania[int(wybrany_index[0])]  # Pobierz wybrany element
            self.kontroler.pokaz_szczegoly_zadania(zadanie)
