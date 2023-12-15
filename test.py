import tkinter as tk
from tkinter import ttk, StringVar, Label, Entry, Button
from PIL import Image, ImageTk
from datetime import datetime
import csv
import socket
import re

class MealTrackerApp:
    def __init__(self, root):
        self.setup_graphics(root)
        self.draw_table(root)

    def setup_graphics(self, root):
        root.geometry('800x600')
        root.resizable(False, False)
        root.configure(bg='#F1E5AC')
        root.title("My Mess")

        img = Image.open("Surver.png")
        new_width, new_height = 150, 150
        resized_img = img.resize((new_width, new_height))
        self.resized_img = ImageTk.PhotoImage(resized_img)

        self.profile_label = Label(root, image=self.resized_img, bg='#F1E5AC')
        self.profile_label.place(x=20, y=20)

        self.date_var = StringVar(value=self.get_current_date())
        self.morning_var = StringVar()
        self.afternoon_var = StringVar()
        self.night_var = StringVar()

        self.create_entry_labels(root)
        self.create_submit_button(root)

    def create_entry_labels(self, root):
        labels_info = [("Date:", 200, 25), ("Morning:", 200, 50), ("Afternoon:", 200, 80), ("Night:", 200, 110)]

        for label_text, x, y in labels_info:
            Label(root, text=label_text).place(x=x, y=y)
        
        Entry(root, textvariable=self.date_var, state='readonly').place(x=300, y=25)
        Entry(root, textvariable=self.morning_var).place(x=300, y=50)
        Entry(root, textvariable=self.afternoon_var).place(x=300, y=80)
        Entry(root, textvariable=self.night_var).place(x=300, y=110)

    def create_submit_button(self, root):
        Button(root, text="Submit", command=self.submit_data).place(x=300, y=140)

    def get_current_date(self):
        now = datetime.now()
        date_string = now.strftime("%Y-%m-%d")
        return date_string

    def submit_data(self):
        date = self.date_var.get()
        morning = self.morning_var.get()
        afternoon = self.afternoon_var.get()
        night = self.night_var.get()

        with open('data.csv', 'a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([date, morning, afternoon, night])

        self.update_table()
        self.clear_entry_widgets()
        self.date_var.set(self.get_current_date())
        print("Data submitted successfully.")
        
        self.str=f"Date: {date}, morning: { morning },afternoon: {afternoon}, night: {night}"
        self.cm=Communication()
        self.cm.send_menue(self.str)
        

    def clear_entry_widgets(self):
        self.morning_var.set('')
        self.afternoon_var.set('')
        self.night_var.set('')

    def draw_table(self, root):
        with open('data.csv', 'r') as file:
            reader = csv.DictReader(file)
            headers = reader.fieldnames
            self.user_data = list(reader)

        separator_frame = self.create_separator_frame(root)
        self.create_header_labels(separator_frame, headers)
        self.tree = self.create_treeview(separator_frame, headers)
        self.insert_data_into_table(self.tree)
        self.tree.pack(padx=5, pady=5)
        separator_frame.place(x=50, y=200)

    def create_separator_frame(self, root):
        separator_frame = ttk.Frame(root)
        ttk.Separator(separator_frame, orient=tk.HORIZONTAL).pack(fill='x', padx=5, pady=5)
        return separator_frame

    def create_header_labels(self, separator_frame, headers):
        headers_frame = ttk.Frame(separator_frame)
        headers_frame.pack(pady=5)

        for col, header in enumerate(headers):
            label = ttk.Label(headers_frame, text=header)
            label.grid(row=0, column=col, padx=10)

        ttk.Separator(separator_frame, orient=tk.HORIZONTAL).pack(fill='x', pady=5)

    def create_treeview(self, separator_frame, headers):
        tree = ttk.Treeview(separator_frame)
        tree["columns"] = headers

        for col in headers:
            tree.column(col, anchor=tk.W, width=100)
            tree.heading(col, text=col, anchor=tk.W)

        return tree

    def insert_data_into_table(self, tree):
        for row, data in enumerate(self.user_data):
            tree.insert("", row, values=tuple(data.values()))

    def update_table(self):
        self.tree.delete(*self.tree.get_children())
        with open('data.csv', 'r') as file:
            reader = csv.DictReader(file)
            self.user_data = list(reader)
            self.insert_data_into_table(self.tree)
class Communication():
    def send_menue(self,string):
        self.string=string
        ip = "127.0.0.1"
        port = 6644
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind((ip, port))
        server.listen(5)

        while True:
            client, address = server.accept()
            print(f"Connection Established - {address[0]}:{address[1]}")
            
            #string = client.recv(1024)
            #string = string.decode("utf-8")
            client.send(bytes(self.string, "utf-8"))
            client.close()
            break
    

root = tk.Tk()
app = MealTrackerApp(root)
root.mainloop()
