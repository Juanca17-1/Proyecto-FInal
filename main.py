from views.main_window import PetFinderApp
import tkinter as tk

if __name__ == "__main__":
    root = tk.Tk()
    app = PetFinderApp(root)
    root.mainloop()