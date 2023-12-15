from tkinter import *
from tkinter import messagebox
from tkinter import ttk
from back_end import Network, File_task
from datetime import datetime
from datetime import datetime
import cv2
from pyzbar.pyzbar import decode
from PIL import Image, ImageTk
import json

class SigninGraphics:
    def S_graphics(self, root):
        self.root = root
        root.title("My Mess")
        root.geometry("700x700")
        root.configure(bg='white')
        root.resizable(False, False)

        Label(root, text="My Mess Registration", font="arial 25").pack(pady=50)

        img = PhotoImage(file="photo/icon.png")
        resized_img = img.subsample(3, 3)  # Adjust the subsample factor as needed
        profile_label = Label(root, image=resized_img, bg='white')
        profile_label.place(x=250, y=100)  # Adjust the position as needed

        Label(text="Name", font=("arial", 24)).place(x=100, y=300)
        Label(text="E-mail", font=("Arial", 23)).place(x=100, y=350)
        Label(text="Phone", font=("Arial", 23)).place(x=100, y=400)

        self.name_entry = Entry(root, width=30, font=("Arial", 20))
        self.email_entry = Entry(root, width=30, font=("Arial", 20))
        self.phone_entry = Entry(root, width=30, font=("Arial", 20))

        self.name_entry.place(x=200, y=300)
        self.email_entry.place(x=200, y=350)
        self.phone_entry.place(x=200, y=400)

        Button(text="Send OTP", font=("Arial", 10), width=11, height=2, command=self.send_otp).place(x=250, y=450)

        root.mainloop()

    def send_otp(self):
        email = self.email_entry.get()
        name = self.name_entry.get()

        be = Network()

        self.otp = be.OTP(email, name)

        Label(text="Enter OTP", font=("Arial", 23)).place(x=100, y=500)

        global otpEntry
        otpEntry = Entry(self.root, width=20, bd=2, font=("Arial", 20))
        otpEntry.place(x=250, y=500)
        Button(text="Submit", font=("Arial", 20), width=9, height=1, command=self.next_page).place(x=250, y=550)

    def next_page(self):
        entered_otp = otpEntry.get()  # Get the OTP entered by the user
        print("Entered OTP is", entered_otp)

        if entered_otp == self.otp:
            name = self.name_entry.get()
            email = self.email_entry.get()
            phone = self.phone_entry.get()

            files = File_task()
            files.enter_Signin_Data(name, email, phone)  # Save the user's data to a JSON file
            #files.setup__data()
            self.root.destroy()

            # Create a new Toplevel window
            self.main_root = Toplevel()
            Main_Window(self.main_root)

            # Perform the actions you want when the OTP is correct
        else:
            print("OTP is incorrect. Please try again.")
            # Handle the case when the OTP is incorrect
            Label(text="Incorrect OTP, try again", font=("Arial", 23)).place(x=100, y=500)


class Main_Window:
    def __init__(self, root):
        self.root = root
        self.icon(self.root)
       
        return None

    def icon(self, root):
        root.geometry('600x600')
        root.resizable(False, False)
        root.configure(bg='#DAF7A6')
        root.title("My Mess")

        

        # Load the image
        self.img = PhotoImage(file="photo/profile.png")
        self.qr = PhotoImage(file="photo/qr.png")
        self.search = PhotoImage(file="photo/search.png")
        # Resize the image
        new_width = 60  # Set the desired width
        new_height = 60  # Set the desired height

        # Create a Label with the resized image
        self.resized_img = self.img.subsample(self.img.width() // new_width, self.img.height() // new_height)
        self.profile_label = Label(root, image=self.resized_img, bg='#DAF7A6')
        self.profile_label.place(x=20, y=20)

        # qr image
        new_width = 70  # Set the desired width
        new_height = 70  # Set the desired height
        self.resized_qr = self.qr.subsample(self.qr.width() // new_width, self.qr.height() // new_height)
        self.qr_label = Label(root, image=self.resized_qr, bg="#DAF7A6")
        self.qr_label.place(x=500, y=20)
        # search icon
        new_width = 40  # Set the desired width
        new_height = 40  # Set the desired height
        self.resized_search = self.search.subsample(self.search.width() // new_width,self.search.height() // new_height)
        self.search_label = Label(root, image=self.resized_search,bg="#DAF7A6")
        self.search_label.place(x=55, y=130)
        self.searchbar = Entry(root, width=30, bd=0, font=("Arial", 20))
        self.searchbar.place(x=100, y=130)

        ## display date
        self.date_label = Label(root, text="", font=("Helvetica", 12))
        self.current_date = datetime.now().strftime("%Y-%m-%d")
        self.date_label.pack()

        self.date_label.config(text=self.current_date)
        self.date_label.place(x=55, y=190)

        # Function to handle the button click event
        def click(event):
            print("Button clicked")
            Profile()

        def qrclicked(event):
            self.qr_window = Toplevel()
            QRCodeScanner(self.qr_window)
            self.qr_window.mainloop()

        # Bind the click event to the label
        self.qr_label.bind("<Button-1>", qrclicked)
        self.profile_label.bind("<Button-1>", click)
        self.draw_table(root)
        
    
        
        
        
    def draw_table(self, root):
        import tkinter as tk
        from tkinter import ttk

        with open('userdetails.json', 'r') as file:
            self.user_data = json.load(file)

        # Create a Frame for the separator lines and table
        separator_frame = ttk.Frame(root)
        separator_frame.grid(row=0, column=0, pady=230)

        # Add a separator line above the headers
        ttk.Separator(separator_frame, orient=tk.HORIZONTAL).pack(fill='x', padx=0)

        # Create and place labels for headers

        # Add a separator line below the headers
        ttk.Separator(separator_frame, orient=tk.HORIZONTAL).pack(fill='x', pady=0)

        # Create and place a Treeview widget for the table
        tree = ttk.Treeview(separator_frame)
        tree["columns"] = ("Date", "Number of Scans")
        tree.column("#0", width=0, stretch=tk.NO)  # Placeholder column
        tree.column("Date", anchor=tk.W, width=260)
        tree.column("Number of Scans", anchor=tk.W, width=250)

        tree.heading("#0", text="", anchor=tk.W)
        tree.heading("Date", text="Date", anchor=tk.W)
        tree.heading("Number of Scans", text="Number of Scans", anchor=tk.W)

        # Insert data into the table
        for i in range(len(self.user_data["date"])):
            date_value = self.user_data["date"][i]
            scan_value = self.user_data["number of scan"][i]
            tree.insert("", i, values=(date_value, scan_value))

        # Pack the Treeview widget
        tree.pack(padx=0, pady=0)
        separator_frame.place(x=50, y=250)
        # Run the Tkinter event loop
class Profile:
    def __init__(self):
        with open('userdetails.json', 'r') as file:
            self.user_data = json.load(file)
            
        self.name=self.user_data["Name"]
        self.Email=self.user_data["Email"]
        self.Phone=self.user_data["Phone"]
        
        self.u_profile=Tk()
        self.u_profile.geometry("400x600")
        self.u_profile.resizable(False, False)
        
        self.u_profile.title("Profile")
        
        self.p_name=Label(self.u_profile,text=f"Name:  {self.name}",font=("Arial", 16)).place(x=5,y=100)
        self.p_Email=Label(self.u_profile,text=f"Email:  {self.Email}",font=("Arial",16)).place(x=5,y=150)
        self.p_Phone=Label(self.u_profile,text=f"Phone:  {self.Phone}",font=("Arial",16)).place(x=5,y=200)
        self.u_profile.mainloop()
        

        

        


class QRCodeScanner:
    def __init__(self, root):
        self.root = root
        self.root.title("QR Code Scanner")
        self.root.geometry("800x600")
        
        self.create_widgets()
        self.capture = cv2.VideoCapture(0)
        self.capture.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        self.capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
        
        self.scanning = False

    def create_widgets(self):
        self.frame = LabelFrame(self.root, text="QR Code Scanner")
        self.frame.pack(padx=10, pady=10, fill=BOTH, expand=True)

        self.label = Label(self.frame)
        self.label.pack(fill=BOTH, expand=True)

        self.scan_button = Button(self.frame, text="Start Scanning", command=self.toggle_scanning)
        self.scan_button.pack(pady=10)

    def toggle_scanning(self):
        self.scanning = not self.scanning
        if self.scanning:
            self.scan_button.config(text="Stop Scanning")
            self.start_scanning()
        else:
            self.scan_button.config(text="Start Scanning")

    def start_scanning(self):
        while self.scanning:
            success, frame = self.capture.read()

            for barcode in decode(frame):
                barcode_data = barcode.data.decode('utf-8')
                
                print(barcode_data)
                self.show_scanned_result(barcode_data)
                
                current_date_time = datetime.now()
                self.date = current_date_time.strftime("%Y-%m-%d %H:%M:%S")
                
                self.ft=File_task()
                self.ft.enter_scaned_data("tava pulav",self.date)
                
                
                   
            # Update the label with the camera frame
            self.update_label(frame)   
             
            self.root.update_idletasks()
            self.root.update()

    def update_label(self, frame):
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        image = Image.fromarray(frame)
        photo = ImageTk.PhotoImage(image=image)
        self.label.config(image=photo)
        self.label.image = photo

    def show_scanned_result(self, data):
        messagebox.showinfo("QR Code Scanned", f"Data: {data}")

    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    root = Tk()
    try:
        with open("userdetails.json", 'r') as json_file:
            data = json.load(json_file)
        is_empty = not bool(data)
    except (FileNotFoundError, json.JSONDecodeError):
        is_empty = True

    if is_empty:
        sp = SigninGraphics()
        sp.S_graphics(root)
    else:
        mw = Main_Window(root)
    root.mainloop()
