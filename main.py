import sys
import os
import email.utils
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), 'app')))

import tkinter as tk
from task_manager_app import ZarzadzanieZadaniami
from wyslanie import EmailSender


if __name__ == "__main__":
    smtp_server = "smtp.gmail.com"
    port = 587
    sender_email = "pythonprojektautomat@gmail.com"
    password = "nzpayfsabkktgxgo"

    # Tworzenie obiektu EmailSender
    email_sender = EmailSender(smtp_server, port, sender_email, password)
    root = tk.Tk()
    app = ZarzadzanieZadaniami(root)
    root.mainloop()
