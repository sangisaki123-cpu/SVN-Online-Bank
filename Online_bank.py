##SVN ONLINE BANK

import csv
import os
import re

# Create file if not exists:
if not os.path.exists("customer.csv"):
    with open("customer.csv", "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([
            "account_number",
            "first_name",
            "last_name",
            "user_name",
            "phone_number",
            "email_address",
            "aadhar_number",
            "account_type",
            "balance",
            "password",
            "pin"
        ])

# Generate Account number
def generate_account_number():
    last_number = 1000
    with open("customer.csv", "r") as file:
        reader = csv.reader(file)
        next(reader)
        for row in reader:
            if row:  # Ensure row is not empty
                last_number = int(row[0])
    return last_number + 1

def signup():
    print("\n -----SIGN UP-----")
    while True:
        first_name = input("Enter your First name: ").strip()
        last_name = input("Enter your Last name: ").strip()
        
        if not first_name and not last_name:
            print("First name and Last name cannot be empty")
            continue
        elif not first_name:
            print("First name cannot be empty")
            continue
        elif not last_name:
            print("Last name cannot be empty")
            continue
        elif not first_name.isalpha():
            print("First name should contain only alphabets")
            continue
        elif not last_name.isalpha():
            print("Last name should contain only alphabets")
            continue
        
        user_name = first_name.lower() + last_name[0].lower()
        username_taken = False
        
        with open("customer.csv", "r", newline="") as file:
            reader = csv.DictReader(file)
            for customer in reader:
                existing_username = (customer.get("user_name") or "").strip().lower()
                if existing_username == user_name:
                    username_taken = True
                    break
                    
        if username_taken:
            print("Username already exists!")
            print("Please enter a different name.")
            continue
            
        full_name = first_name.title() + " " + last_name.title()
        print("Valid Name")
        print("Customer Name:", full_name)
        print("Your User Name:", user_name)
        break
        
    while True:
        phone_number = input("Enter your 10 digit phone number: ").strip()
        if len(phone_number) == 10 and phone_number.isdigit():
            print("Valid number")
            break
        else:
            print("Invalid phone number, try again")
    
    while True:
        email_address = input("Enter your email address: ").strip()
        email_pattern = r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$"
        if re.fullmatch(email_pattern, email_address): 
            print("Valid email")    
            break
        else:
            print("Invalid email. Please enter a valid email address.")
    
    while True:
        aadhar_number = input("Enter your 12 digit aadhar_number: ").strip()
        if len(aadhar_number) != 12 or not aadhar_number.isdigit():
            print("Invalid aadhar number")
            continue
        break

    while True:
        try:
            balance = int(input("Enter the deposited amount (Min 500): "))
            if balance < 500:
                print("Minimum Balance must be 500")
                continue
            break
        except ValueError:
            print("Please enter numbers only.")

    while True:
        print("\n Select account type")
        print("1. Savings")
        print("2. Current")
        print("3. Salary")

        option = input("Enter Your option: ").strip()
        if option == "1":
            account_type = "Savings"
            break
        elif option == "2":
            account_type = "Current"
            break
        elif option == "3":
            account_type = "Salary"
            break
        else:
            print("Invalid Account type")

    while True:
        password = input("Create your Password: ").strip()
        if len(password) < 6:
            print("Password must contain at least 6 characters")
            continue
        confirm_password = input("Confirm your Password: ").strip()
        if password != confirm_password:
            print("Password does not match")
            continue
        if not re.search(r"[A-Z]", password):
            print("Password must contain at least one uppercase letter.")
            continue
        if not re.search(r"[a-z]", password):
            print("Password must contain at least one lowercase letter.")
            continue
        if not re.search(r"[0-9]", password):
            print("Password must contain at least one number.")
            continue
        if not re.search(r"[@#$%^&*!]", password):
            print("Password must contain at least one special character.")
            continue
        break

    while True:
        pin = input("Create your 4 digit PIN: ").strip()
        if len(pin) != 4 or not pin.isdigit():
            print("PIN must contain exactly 4 digits")
            continue
        confirm_pin = input("Confirm your PIN: ").strip()
        if pin != confirm_pin:
            print("PIN does not match")
            continue
        break
    
    account_number = generate_account_number()

    with open("customer.csv", "a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([
            account_number, first_name, last_name, user_name,
            phone_number, email_address, aadhar_number,
            account_type, balance, password, pin
        ])
    print(f"\nAccount created successfully! Welcome {user_name}")  
    print("Your account number is:", account_number)


def save_transaction(account_number, first_name, transaction_type, amount, balance):
    file_exists = os.path.exists("transaction.csv")
    with open("transaction.csv", "a", newline="") as file:
        fieldnames = ["account_number", "first_name", "transaction_type", "amount", "balance"]
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        if not file_exists:
            writer.writeheader()

        writer.writerow({
            "account_number": account_number,
            "first_name": first_name,
            "transaction_type": transaction_type,
            "amount": amount,
            "balance": balance
        })

def update_customer_balance(account_number, new_balance):
    rows = []
    with open("customer.csv", "r", newline="") as file:
        reader = csv.DictReader(file)
        for row in reader:
            if row["account_number"] == str(account_number):
                row["balance"] = str(new_balance)
            rows.append(row)
            
    with open("customer.csv", "w", newline="") as file:
        fieldnames = [
            "account_number", "first_name", "last_name", "user_name",
            "phone_number", "email_address", "aadhar_number",
            "account_type", "balance", "password", "pin"
        ]
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)      
    
def login():
    found = False
    print("\n----LOGIN----")
    user_name = input("Enter your User Name: ").strip().lower()
    pin = input("Enter Your 4 digit PIN: ").strip()

    if len(pin) != 4 or not pin.isdigit():
        print("Invalid PIN format")
        return
    
    with open("customer.csv", "r", newline="") as file:
        reader = csv.DictReader(file)
        for customer in reader:
            csv_username = customer["user_name"].strip().lower()
            csv_pin = (customer.get("pin") or "").strip()

            if csv_username == user_name and csv_pin == pin:
                found = True
                print("Welcome", user_name)
                  
                balance = int(customer["balance"])
                account_number = customer["account_number"]
                first_name = customer["first_name"]
                
                while True:
                    print("\n1. Deposit")
                    print("2. Withdraw")
                    print("3. Balance Enquiry")
                    print("4. Transaction History")
                    print("5. Exit")

                    choice = input("Enter your choice: ").strip()

                    if choice == "1":
                        try:
                            amount = int(input("Enter deposit amount: "))
                            if amount <= 0:
                                print("Amount must be greater than zero")
                                continue
                            balance += amount
                            print("Amount deposited")
                            print("Balance:", balance)
                            update_customer_balance(account_number, balance)
                            save_transaction(account_number, first_name, "Deposit", amount, balance)
                        except ValueError:
                            print("Please enter numbers only.")

                    elif choice == "2":
                        try:
                            amount = int(input("Enter withdraw amount: "))
                            if amount <= 0:
                                print("Amount must be greater than zero")
                                continue
                            if amount > balance:
                                print("Insufficient balance")
                                continue
                            if balance - amount < 500:
                                print("Your account balance cannot go below 500")
                                continue

                            balance -= amount
                            print("Amount withdrawn")
                            print("Balance:", balance)

                            update_customer_balance(account_number, balance)

                            save_transaction(
                                account_number,
                                first_name,
                                "Withdraw",
                                amount,
                                balance
                            )

                        except ValueError:
                            print("Please enter numbers only")
                        
                    
                    elif choice == "3":
                        print("Balance:",balance)

                    elif choice == "4":
                        show_history(account_number)

                    elif choice == "5":
                        print("Exit successfully")
                        return
                    else:
                        print("Invalid choice")
                        return
                        
    if not found:
        print("Account Invalid, Please Try again")

def show_history(account_number):
    
    with open("transaction.csv","r") as file:
        reader = csv.DictReader(file)
        
        print("\n---Transaction History---\n")
        print("first_name\t\taccount_number\t\ttransaction_type\t\tamount\t\tbalance")
    
        for row in reader:
            if row ["account_number"] == str(account_number):
                print(f"{row['first_name']}\t\t{row['account_number']}\t\t{row['transaction_type']}\t\t{row['amount']}\t\t{row['balance']}")
                
            
##Main manu

print("Welcome to SVN Bank")

while True:
    print("\n1.Sign")
    print("2.Login")
    print ("3.Exit")

    choice = input("Enter choice:")

    if choice == "1":
        signup()

    elif choice == "2":
        login()

    elif choice == "3":
        print("Thank you")
        break
        

    else:
        print("Invalid choice")
        

        
