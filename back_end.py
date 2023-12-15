import random as rd
from email.message import EmailMessage
import smtplib
import ssl
import json
import socket
import re
import csv
class Network:
    
    def OTP(self,email_receiver, receiver_name):
        email_sender="pawarmkarthikaya@gmail.com"
        email_pass="jnxa bnrd jrpk mkyd"
        subject="OTP"
        
        otp=self.genOTP()
        body="Dear" + receiver_name + "\n Thanks for regestring with our app, hope our survices finde you well. User Name =" + receiver_name + "\n E-mail ="+ receiver_name +  "OTP: "+otp 
         
        em=EmailMessage()
        em["From"]=email_sender
        em["To"]=email_receiver
        em["Subject"]=subject
        em.set_content(body)
        
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
            smtp.login(email_sender, email_pass)
            smtp.sendmail(email_sender, email_receiver, em.as_string())
        
        return otp
             
        
    def genOTP(self):
        otp=str(rd.randint(100000,999999))
        return otp
    
    def recive_menue(self):
        ip = "127.0.0.1"
        port = 6644

        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect((ip, port))

        # Receive data from the server
        buffer = client.recv(1024)
        buffer = buffer.decode("utf-8")
        self.date_match = re.search(r"Date: (.+?),", buffer)
        self.morning_match = re.search(r"morning: (.+?),", buffer)
        self.afternoon_match = re.search(r"afternoon: (.+?),", buffer)
        self.night_match = re.search(r"night: (.+)$", buffer)
        self.adadd_menue(self.date_match,self.morning_match,self.afternoon_match,self.night_match)
        # Close the client socket
        client.close()
    
    
class File_task:
    def enter_Signin_Data(self,name, email, phone):
        user_data={
            "Name":name,
            "Email":email,
            "Phone":phone,
            "date": [],
            "number of scan": []
            
        }
        
        with open("userdetails.json","w") as file:
            json.dump(user_data, file)
        file.close()

    
    def setup__data(self):
        # Load existing data from the JSON file
        with open('userdetails.json', 'r') as file:
            user_data = json.load(file)

        # Add new data
        new_data = {
            "date": [],
            "number of scan": []
            
        }

        # Update the user_data dictionary with the new data
        user_data.update(new_data)

        # Save the updated data back to the JSON file
        with open('userdetails.json', 'w') as file:
            json.dump(user_data, file, indent=2)

    def  enter_scaned_data(self,menue,current_date):
        
        with open('userdetails.json', 'r') as file:
            user_data = json.load(file)
        
        if "date" not in user_data:
            user_data["date"] = []
               
        new_scan_data = {
            "date": current_date,
            "number of scan": 1  # Replace with the actual number of scans
            }
            
        user_data["date"].append(current_date)
        user_data["number of scan"].append(new_scan_data["number of scan"])

            # Save the updated data back to the JSON file
        with open('userdetails.json', 'w') as file:
            json.dump(user_data, file, indent=2)
            
    def add_menue(self,date,morning,afternoon,night ):
        self.date=date
        self.morning=morning
        self.afternoon=afternoon
        self.night=night
        
        csv_file = 'menue.csv'
        
        with open(csv_file, 'w', newline='') as file:
            self.writer = csv.writer(file)

    # Write header
        self.writer.writerow(['date', 'morning', 'afternoon', 'night'])

    # Write data
        self.writer.writerow([self.date, self.morning, self.afternoon, self.night])


        

        


        