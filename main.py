import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), 'app')))

import tkinter as tk
from task_manager_app import ZarzadzanieZadaniami

if __name__ == "__main__":
    root = tk.Tk()
    app = ZarzadzanieZadaniami(root)
    root.mainloop()
