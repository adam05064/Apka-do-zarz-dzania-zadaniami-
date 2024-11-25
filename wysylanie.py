import os
import shutil
import time
import smtplib



class EmailSender:
    def __init__(self, smtp_server, port, sender_email, password):
        self.smtp_server = smtp_server
        self.port = port
        self.sender_email = sender_email
        self.password = password

    def send_email(self, subject, body, recipient_email):
        msg = MIMEText(body)
        msg['Subject'] = subject
        msg['From'] = self.sender_email
        msg['To'] = recipient_email

        try:
            with smtplib.SMTP(self.smtp_server, self.port) as server:
                server.starttls()
                server.login(self.sender_email, self.password)
                server.sendmail(self.sender_email, recipient_email, msg.as_string())
            print("Wiadomość została wysłana pomyślnie!")
        except Exception as e:
            print(f"Błąd podczas wysyłania e-maila: {e}")

if __name__ == "__main__":
    # Konfiguracja serwera e-mail
    smtp_server = "smtp.gmail.com"
    port = 587
    sender_email = "pythonprojektautomat@gmail.com"
    password = "nzpayfsabkktgxgo"

    # Tworzenie obiektu EmailSender
    email_sender = EmailSender(smtp_server, port, sender_email, password)

    # Ścieżki do katalogów
    source = "C:\\Kopia"
    destination = "C:\\Kopia2"

    # Wykonywanie kopii zapasowej
    backup(source, destination, email_sender)
