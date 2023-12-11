import tkinter as tk
from tkinter.filedialog import asksaveasfile
from tkinter import ttk
from PIL import ImageTk, Image

from xpanther import XPantherIDE
import re

class XPantherGUI:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("XPanther")
        self.window.configure(bg="black")
        self.window.minsize(350, 250)
        self.window.maxsize(350, 250)

        label = tk.Label(self.window, text="Enter URL:", fg="white", bg="black", font=("Helvetica", 10))
        label.pack(pady=10)

        self.entry = tk.Entry(self.window, bg="black", fg="white", font=("Arial", 10), width=40, insertbackground="purple")
        self.entry.pack(pady=12)
        self.entry.focus_set()

        start = tk.Button(self.window, text="Start", bg="purple", fg="white", font=("Helvetica", 12), command=self.save_url)
        start.pack(pady=5)

        self.window.bind('<Return>', lambda event: self.save_url())

        self.url = ''

        options_label = tk.Label(self.window, text="Language:", fg="white", bg="black", font=("Helvetica", 10))
        options_label.pack(pady=5)

        self.selected_option = tk.StringVar(self.window)
        self.selected_option.set("Python")

        style = ttk.Style()
        style.configure("TCombobox", background="white", foreground="black")
        style.map("TCombobox", fieldbackground=[("readonly", "black")])

        options_menu = ttk.Combobox(self.window, textvariable=self.selected_option, values=["Python", "Java", "C#", "Ruby", "JavaScript", "Kotlin"], state='readonly')
        options_menu.pack(pady=5)

        self.advanced_var = tk.IntVar()
        advanced_checkbox = tk.Checkbutton(self.window, text="Show All", variable=self.advanced_var, fg="white",
                                           bg="black", selectcolor="black")
        advanced_checkbox.pack(pady=5)

        self.text_area = None
        self.result_window = None

    def launch(self):
        self.window.mainloop()
        if self.url:
            if not (result := XPantherIDE(self.url, advanced=self.advanced_var.get(), GUI=True, language=self.selected_option.get()).start()):
                result = 'Something went wrong...'
            else:
                result = ' '.join(result)
            self.show_results(result)
        else:
            return False

    def save_url(self):
        self.url = self.entry.get()
        self.window.destroy()

    def show_results(self, info):
        self.result_window = tk.Tk()
        self.result_window.title("Output")
        self.result_window.configure(bg="black")
        self.result_window.minsize(741, 410)
        self.result_window.maxsize(741, 410)

        frame = tk.Frame(self.result_window, bg="black")
        frame.grid(row=0, column=0, sticky=tk.NSEW)

        self.text_area = tk.Text(frame, wrap=tk.NONE, bg="black", fg="white", font=("Helvetica", 13), insertbackground='white')
        self.text_area.grid(row=0, column=0, sticky=tk.NSEW)
        self.text_area.focus_force()

        y_scrollbar = tk.Scrollbar(frame, bg="#1e1e1e", troughcolor="white")
        y_scrollbar.grid(row=0, column=1, sticky=tk.NS)
        self.text_area.config(yscrollcommand=y_scrollbar.set)
        y_scrollbar.config(command=self.text_area.yview)

        x_scrollbar = tk.Scrollbar(self.result_window, orient=tk.HORIZONTAL, bg="#1e1e1e", troughcolor="white")
        x_scrollbar.grid(row=1, column=0, sticky=tk.EW)
        self.text_area.config(xscrollcommand=x_scrollbar.set)
        x_scrollbar.config(command=self.text_area.xview)

        self.result_window.grid_rowconfigure(0, weight=1)
        self.result_window.grid_columnconfigure(0, weight=1)

        ansi_escape = re.compile(r'\033\[[0-9;]+m')
        stripped_output = ansi_escape.sub('', info)
        self.text_area.insert(tk.END, stripped_output)

        if info != 'Something went wrong...':
            self.result_window.protocol("WM_DELETE_WINDOW", self.save_file)
        self.result_window.mainloop()

    def save_file(self):
        file_path = asksaveasfile(defaultextension=".txt", filetypes=[("Text Files", "*.txt")])
        if file_path:
            with open(file_path.__getattribute__('name'), 'w', encoding='utf-8') as file:
                content = self.text_area.get("1.0", tk.END)
                file.write(content)
        self.result_window.destroy()

    @staticmethod
    def get_images(images, width=70, height=120):
        return [ImageTk.PhotoImage(Image.open(image).resize((width, height), Image.LANCZOS)) for image in images]


if __name__ == '__main__':
    XPantherGUI().launch()
