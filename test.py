import tkinter as tk
from tkinter import ttk

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("AI Asistan")
        self.geometry("400x300")
        
        self.frame = ttk.Frame(self, padding="10")
        self.frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        
        self.speak_button = ttk.Button(self.frame, text="Konuş", command=self.start_recording)
        self.speak_button.grid(row=0, column=0, pady=20)
        
        self.stop_button = ttk.Button(self.frame, text="Durdur", command=self.stop_recording, state="disabled")
        self.stop_button.grid(row=1, column=0)
        
        self.status_label = ttk.Label(self.frame, text="Hazır")
        self.status_label.grid(row=2, column=0, pady=20)
        
    def start_recording(self):
        self.status_label.config(text="Kayıt başladı. Konuşun...")
        self.speak_button.config(state="disabled")
        self.stop_button.config(state="normal")
        # Geçici olarak burada kayıda başladığını belirtiyoruz.
        print("Recording started...")

    def stop_recording(self):
        self.status_label.config(text="Kayıt durduruldu. İşleniyor...")
        self.speak_button.config(state="disabled")
        self.stop_button.config(state="disabled")
        # Geçici olarak burada kayıdı durdurduğunu belirtiyoruz.
        print("Recording stopped...")

    def run(self):
        self.mainloop()

if __name__ == "__main__":
    app = App()
    app.run()