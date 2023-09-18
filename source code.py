import smtplib
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox, filedialog
import getpass  # for masking password
import re

# Define carrier gateways
carrier_gateways = {
    "US": {
        "Verizon": "@vtext.com",
        "AT&T": "@txt.att.net",
        "T-Mobile": "@tmomail.net",
        "Sprint": "@messaging.sprintpcs.com",
    },
    "Canada": {
        "Rogers": "@pcs.rogers.com",
        "Bell": "@txt.bell.ca",
        "Telus": "@msg.telus.com",
    },
    "UK": {
        "O2": "@o2imail.co.uk",
        "Orange": "@orange.net",
        "T-Mobile": "@t-mobile.uk.net",
    },
    "Australia": {
        "Telstra": "@sms.1.telstra.com",
    },
    "Germany": {
        "T-Mobile": "@t-mobile-sms.de",
        "Vodafone": "@vodafone-sms.de",
    },
    "India": {
        "Airtel": "@airtelkk.com",
    },
    "France": {
        "Orange": "@orange.fr",
    },
    "South Africa": {
        "Vodacom": "@voda.co.za",
    },
    "Brazil": {
        "Claro": "@clarotorpedo.com.br",
    },
    "New Zealand": {
        "Vodafone": "@mtxt.co.nz",
    }
}

print('''

 __         _____  ___ ____  __          __    
/ _\  /\/\ /__   \/ _ \___ \/ _\  /\/\  / _\   
\ \  /    \  / /\/ /_)/ __) \ \  /    \ \ \    
_\ \/ /\/\ \/ / / ___/ / __/_\ \/ /\/\ \_\ \   
\__/\/    \/\/  \/    |_____\__/\/    \/\__/   
                                               

Coder Name: Aron-TN
Tool Name: SMTP2SMS
Version: v2''')


# Initialize first Tkinter window but withdraw it
root = tk.Tk()
root.title("SMS Sender")
root.withdraw()  # Hide the window

def destroy_window():
    root.destroy()

def get_phone_numbers():
    global phone_numbers
    while True:
        file_path = filedialog.askopenfilename(title="Select file with phone numbers",
                                               filetypes=[("Text files", "*.txt")])
        if not file_path:
            should_continue = messagebox.askyesno("Warning", "You need to select a text file. Would you like to try again?")
            if not should_continue:
                break
        else:
            with open(file_path, 'r') as f:
                phone_numbers = f.read().strip().split("\n")
            break


def update_carriers(*args):
    selected_country = country_var.get()
    if selected_country in carrier_gateways:
        carriers = [f"{carrier} ({gateway})" for carrier, gateway in carrier_gateways[selected_country].items()]
        carrier_combo['values'] = carriers

def clean_phone_number(phone_number):
    return re.sub("[^0-9]", "", phone_number)

# Show alert for country and carrier selection BEFORE main window is displayed
messagebox.showinfo("Notice", "We will show you a list of available countries. Please select your country and carrier.")

# Create Tkinter variables
country_var = tk.StringVar()
carrier_var = tk.StringVar()

# Create and place widgets
ttk.Label(root, text="Country:").grid(row=0, column=0)
country_combo = ttk.Combobox(root, textvariable=country_var, values=list(carrier_gateways.keys()))
country_combo.grid(row=0, column=1)
country_combo.bind("<<ComboboxSelected>>", update_carriers)

ttk.Label(root, text="Carrier:").grid(row=1, column=0)
carrier_combo = ttk.Combobox(root, textvariable=carrier_var, values=[])
carrier_combo.grid(row=1, column=1)

ttk.Button(root, text="OK", command=destroy_window).grid(row=2, columnspan=2)

root.deiconify()  # Show the window
root.mainloop()

print(f"Country : {str(country_var.get())}")
print(f"Carrier : {str(carrier_var.get())}")

# Initialize second Tkinter window for the MessageBox
second_root = tk.Tk()
second_root.withdraw()

# Show alert for phone number input
messagebox.showinfo("Notice", "We will open a file dialog for you. Please select your file containing the list of phone numbers.")

get_phone_numbers()

# Continue the rest in the terminal
selected_country = country_var.get()
selected_carrier = carrier_var.get()

if selected_country and selected_carrier and phone_numbers:
    selected_carrier_name = selected_carrier.split(' (')[0]
    phone_number_list = phone_numbers
    
    smtp_server = input("Enter the SMTP server: ")
    smtp_port = input("Enter the SMTP port (usually 587 or 465): ")
    smtp_user = input("Enter the SMTP username: ")
    smtp_password = getpass.getpass("Enter the SMTP password: ")

    try:
        if smtp_port == '465':
            server = smtplib.SMTP_SSL(smtp_server, int(smtp_port))
        else:
            server = smtplib.SMTP(smtp_server, int(smtp_port))
            server.starttls()

        server.login(smtp_user, smtp_password)
        message = input("Enter your message: ")
        
        for phone_number in phone_number_list:
            cleaned_phone_number = clean_phone_number(phone_number)
            recipient = f"{cleaned_phone_number}{carrier_gateways[selected_country][selected_carrier_name]}"
            server.sendmail(smtp_user, recipient, message)
            print(f"SMS sent successfully to {phone_number}.")
        server.quit()
    except Exception as e:
        print(f"An error occurred: {e}")

else:
    print("Invalid country, carrier, or phone numbers.")
