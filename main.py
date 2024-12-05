# Importing the tkinter library for GUI development
import tkinter as tk

# Importing additional tkinter modules for widgets and dialogs
from tkinter import ttk, messagebox

# Importing pickle module for data serialization
import pickle

# Importing datetime module for handling date and time
from datetime import datetime

# Base class for User (Inheritance)
class User:
    # Constructor to initialize user attributes
    def __init__(self, user_id, name, email, password):
        self.__user_id = user_id  # Private attribute for user ID
        self.__name = name        # Private attribute for user name
        self.__email = email      # Private attribute for user email
        self.__password = password  # Private attribute for user password

    # Method to retrieve user ID
    def get_user_id(self):
        return self.__user_id

    # Method to retrieve user name
    def get_name(self):
        return self.__name

    # Method to retrieve user email
    def get_email(self):
        return self.__email

    # Method to check if a given password matches the stored password
    def check_password(self, password):
        return self.__password == password

    # String representation of a User object
    def __str__(self):
        return f"User: {self.__name} (ID: {self.__user_id})"

# Customer class inherits from User (Inheritance)
class Customer(User):
    # Constructor to initialize customer-specific attributes
    def __init__(self, user_id, name, email, password, phone_number):
        super().__init__(user_id, name, email, password)  # Call to parent constructor
        self.__phone_number = phone_number  # Private attribute for customer phone number
        self.__reservations = []  # Aggregation: Customer has a list of reservations

    # Method to add a reservation to the customer's list
    def add_reservation(self, reservation):
        self.__reservations.append(reservation)

    # Method to retrieve the customer's phone number
    def get_phone_number(self):
        return self.__phone_number

    # Method to retrieve all reservations for the customer
    def get_reservations(self):
        return self.__reservations

    # String representation of a Customer object
    def __str__(self):
        return f"Customer: {self.get_name()} (ID: {self.get_user_id()})"

# Admin class inherits from User (Inheritance)
class Admin(User):
    # Constructor to initialize admin-specific attributes
    def __init__(self, user_id, name, email, password, role):
        super().__init__(user_id, name, email, password)  # Call to parent constructor
        self.__role = role  # Private attribute for admin role

    # Method to retrieve the admin's role
    def get_role(self):
        return self.__role

    # String representation of an Admin object
    def __str__(self):
        return f"Admin: {self.get_name()} (Role: {self.__role})"

# Class representing a Ticket
class Ticket:
    # Constructor to initialize ticket attributes
    def __init__(self, ticket_id, ticket_type, price, validity, description, limitations, discount=None):
        self.__ticket_id = ticket_id  # Private attribute for ticket ID
        self.__ticket_type = ticket_type  # Private attribute for ticket type
        self.__price = price  # Private attribute for ticket price
        self.__validity = validity  # Private attribute for ticket validity
        self.__description = description  # Private attribute for ticket description
        self.__limitations = limitations  # Private attribute for ticket limitations
        self.__discount = discount  # Private attribute for optional discount

    # Getter methods for ticket attributes
    def get_ticket_id(self):
        return self.__ticket_id

    def get_ticket_type(self):
        return self.__ticket_type

    def get_price(self):
        return self.__price

    def get_validity(self):
        return self.__validity

    def get_description(self):
        return self.__description

    def get_limitations(self):
        return self.__limitations

    def get_discount(self):
        return self.__discount

    # Method to update ticket price
    def set_price(self, new_price):
        self.__price = new_price

    # String representation of a Ticket object
    def __str__(self):
        return f"{self.__ticket_type} - {self.__price} DHS"

# Class representing a Reservation
class Reservation:
    # Constructor to initialize reservation attributes
    def __init__(self, reservation_id, customer, ticket, date):
        self.__reservation_id = reservation_id  # Private attribute for reservation ID
        self.__customer = customer  # Composition: Reservation has a Customer
        self.__ticket = ticket  # Composition: Reservation has a Ticket
        self.__date = date  # Private attribute for reservation date
        self.__payment = None  # Bidirectional Association: Reservation has a Payment

    # Method to associate a payment with the reservation
    def set_payment(self, payment):
        self.__payment = payment

    # Getter methods for reservation attributes
    def get_reservation_id(self):
        return self.__reservation_id

    def get_customer(self):
        return self.__customer

    def get_ticket(self):
        return self.__ticket

    def get_date(self):
        return self.__date

    def get_payment(self):
        return self.__payment

    # String representation of a Reservation object
    def __str__(self):
        return f"Reservation {self.__reservation_id}: {self.__ticket.get_ticket_type()} for {self.__customer.get_name()} on {self.__date}"

# Class representing a Payment
class Payment:
    # Constructor to initialize payment attributes
    def __init__(self, payment_id, amount, payment_method):
        self.__payment_id = payment_id  # Private attribute for payment ID
        self.__amount = amount  # Private attribute for payment amount
        self.__payment_method = payment_method  # Private attribute for payment method
        self.__date = datetime.now().strftime("%Y-%m-%d")  # Auto-generated payment date
        self.__reservation = None  # Bidirectional Association: Payment has a Reservation

    # Method to associate a reservation with the payment
    def set_reservation(self, reservation):
        self.__reservation = reservation

    # Getter methods for payment attributes
    def get_payment_id(self):
        return self.__payment_id

    def get_amount(self):
        return self.__amount

    def get_payment_method(self):
        return self.__payment_method

    def get_date(self):
        return self.__date

    def get_reservation(self):
        return self.__reservation

    # String representation of a Payment object
    def __str__(self):
        return f"Payment: {self.__payment_id} - Amount: {self.__amount} DHS, Method: {self.__payment_method}"

# Function to save data to a file using pickle
def save_data(filename, data):
    with open(filename, 'wb') as file:  # Open file in write-binary mode
        pickle.dump(data, file)  # Serialize and save data to the file

# Function to load data from a file using pickle
def load_data(filename):
    try:
        with open(filename, 'rb') as file:  # Open file in read-binary mode
            return pickle.load(file)  # Load and deserialize data from the file
    except FileNotFoundError:
        # If the file doesn't exist, create a default admin for admin data
        if filename == "admins.pkl":
            default_admin = Admin(1, "Admin", "admin@admin.com", "test1234", "Admin")
            save_data(filename, [default_admin])  # Save the default admin to the file
            return [default_admin]
        # Return an empty list for other data files
        return []


# Main Application class from tkinterto create the main application window
class AdventureLandApp(tk.Tk):
    # Constructor to initialize the main application window
    def __init__(self):
        super().__init__()  # Call the constructor of the parent Tk class
        self.title("Adventure Land Theme Park")  # Set the title of the application window
        self.geometry("800x700")  # Set the size of the application window (800x700 pixels)

        # Load data from serialized files using the load_data function
        self.customers = load_data("customers.pkl")  # Load customer data from file
        self.admins = load_data("admins.pkl")  # Load admin data from file
        self.tickets = load_data("tickets.pkl")  # Load ticket data from file
        self.reservations = load_data("reservations.pkl")  # Load reservation data from file
        self.payments = load_data("payments.pkl")  # Load payment data from file

        # Check if there are no tickets loaded, then initialize default tickets
        if not self.tickets:
            self.initialize_default_tickets()  # Initialize default tickets if none exist

        self.current_user = None  # Set current user to None initially (no user logged in)

        # Create the main menu of the application
        self.create_main_menu()  # Call method to create and display the main menu

    # Method to initialize default ticket data if no tickets exist
    def initialize_default_tickets(self):
        # Create a list of default tickets with predefined attributes
        default_tickets = [
            Ticket(1, "Single-Day Pass", 275, "1 Day", "Access to the park for one day", "Valid only on selected date",
                   None),
            Ticket(2, "Two-Day Pass", 480, "2 Days", "Access to the park for two consecutive days",
                   "Cannot be split over multiple trips", "10% discount for online purchase"),
            Ticket(3, "Annual Membership", 1840, "1 Year", "Unlimited access for one year",
                   "Must be used by the same person", "15% discount on renewal"),
            Ticket(4, "Child Ticket", 185, "1 Day", "Discounted ticket for children (ages 3-12)",
                   "Valid only on selected date, must be accompanied by an adult", None),
            Ticket(5, "Group Ticket", 220, "1 Day", "Special rate for groups of 10 or more",
                   "Must be booked in advance", "20% off for groups of 20 or more"),
            Ticket(6, "VIP Experience Pass", 550, "1 Day", "Includes expedited access and reserved seating for shows",
                   "Limited availability, must be purchased", None)
        ]
        # Add the default tickets to the tickets list
        self.tickets.extend(default_tickets)  # Append the default tickets to the existing ticket list
        # Save the updated tickets list to the file "tickets.pkl"
        save_data("tickets.pkl", self.tickets)  # Call save_data function to serialize and save the updated tickets list

    # Method to create and display the main menu of the application
    def create_main_menu(self):
        self.clear_window()  # Clear the window before creating a new layout

        # Create a frame for the main menu
        main_frame = ttk.Frame(self)  # Create a ttk.Frame to hold the menu content
        main_frame.pack(expand=True, fill='both', padx=20, pady=20)  # Pack the frame with padding and expansion

        # Create a title label for the main menu
        title_label = ttk.Label(main_frame, text="Adventure Land Theme Park",
                                font=("Arial", 24, "bold"))  # Create a label with bold title
        title_label.pack(pady=20)  # Pack the title label with vertical padding

        # Create a frame to hold the buttons
        button_frame = ttk.Frame(main_frame)  # Create a frame for the buttons
        button_frame.pack(pady=20)  # Pack the button frame with vertical padding

        # Create and pack main menu buttons with corresponding commands
        ttk.Button(button_frame, text="Customer Login", command=self.show_login_page).pack(pady=5,
                                                                                           fill='x')  # Button to show login page
        ttk.Button(button_frame, text="Register New Account", command=self.show_register_page).pack(pady=5,
                                                                                                    fill='x')  # Button to show registration page
        ttk.Button(button_frame, text="Admin Login", command=self.show_admin_login).pack(pady=5,
                                                                                         fill='x')  # Button to show admin login
        ttk.Button(button_frame, text="View Ticket Information", command=self.show_ticket_info).pack(pady=5,
                                                                                                     fill='x')  # Button to show ticket info
        ttk.Button(button_frame, text="Exit", command=self.quit).pack(pady=5,
                                                                      fill='x')  # Button to exit the application

    # Method to display the customer login page
    def show_login_page(self):
        self.clear_window()  # Clear the window before displaying the login page

        # Create a frame for the login page
        login_frame = ttk.Frame(self)  # Create a ttk.Frame to hold the login form
        login_frame.pack(expand=True, padx=20, pady=20)  # Pack the login frame with padding

        # Create and display a label for the login page title
        ttk.Label(login_frame, text="Customer Login", font=("Arial", 18, "bold")).pack(pady=10)  # Title with bold text

        # Email field label and input box
        ttk.Label(login_frame, text="Email:").pack()  # Create a label for the email field
        email_entry = ttk.Entry(login_frame, width=30)  # Create an entry box for email input
        email_entry.pack(pady=5)  # Pack the email entry box with vertical padding

        # Password field label and input box
        ttk.Label(login_frame, text="Password:").pack()  # Create a label for the password field
        password_entry = ttk.Entry(login_frame, show="*",
                                   width=30)  # Create a password entry box, with hidden characters
        password_entry.pack(pady=5)  # Pack the password entry box with vertical padding

        # Login button that processes the login when clicked
        ttk.Button(login_frame, text="Login",
                   command=lambda: self.process_login(email_entry.get(), password_entry.get())).pack(
            pady=10)  # Button to trigger login process

        # Back button to return to the main menu
        ttk.Button(login_frame, text="Back to Main Menu",
                   command=self.create_main_menu).pack(pady=5)  # Button to go back to the main menu

    # Method to display the registration page for creating a new account
    def show_register_page(self):
        self.clear_window()  # Clear the window before displaying the registration page

        # Create a frame for the registration form
        register_frame = ttk.Frame(self)  # Create a ttk.Frame to hold the registration form
        register_frame.pack(expand=True, padx=20, pady=20)  # Pack the registration frame with padding

        # Create and display a label for the registration page title
        ttk.Label(register_frame, text="Register New Account", font=("Arial", 18, "bold")).pack(
            pady=10)  # Title with bold text

        # Create a dictionary to hold the registration fields
        fields = {}  # Initialize an empty dictionary to store field entries

        # Loop through a list of required fields and create labels and input boxes for each
        for field in ["Name", "Email", "Password", "Phone Number"]:
            ttk.Label(register_frame, text=f"{field}:").pack()  # Label for each field (e.g., Name, Email)
            entry = ttk.Entry(register_frame, width=30)  # Create an entry box for user input
            entry.pack(pady=5)  # Pack the entry box with vertical padding
            fields[field.lower().replace(" ", "_")] = entry  # Add the entry box to the dictionary with a formatted key

        # Register button that triggers the registration process when clicked
        ttk.Button(register_frame, text="Register",
                   command=lambda: self.process_registration(
                       fields["name"].get(),  # Get the value from the "Name" entry field
                       fields["email"].get(),  # Get the value from the "Email" entry field
                       fields["password"].get(),  # Get the value from the "Password" entry field
                       fields["phone_number"].get()  # Get the value from the "Phone Number" entry field
                   )).pack(pady=10)  # Button that triggers registration with entered details

        # Back button to return to the main menu
        ttk.Button(register_frame, text="Back to Main Menu",
                   command=self.create_main_menu).pack(pady=5)  # Button to navigate back to the main menu

    # Method to display the admin login page
    def show_admin_login(self):
        self.clear_window()  # Clear the window before displaying the admin login page

        # Create a frame for the admin login form
        admin_frame = ttk.Frame(self)  # Create a ttk.Frame to hold the admin login form
        admin_frame.pack(expand=True, padx=20, pady=20)  # Pack the admin frame with padding

        # Create and display a label for the admin login page title
        ttk.Label(admin_frame, text="Admin Login", font=("Arial", 18, "bold")).pack(pady=10)  # Title with bold text

        # Admin email field label and input box
        ttk.Label(admin_frame, text="Email:").pack()  # Create a label for the email field
        email_entry = ttk.Entry(admin_frame, width=30)  # Create an entry box for the admin email input
        email_entry.pack(pady=5)  # Pack the email entry box with vertical padding

        # Admin password field label and input box
        ttk.Label(admin_frame, text="Password:").pack()  # Create a label for the password field
        password_entry = ttk.Entry(admin_frame, show="*",
                                   width=30)  # Create a password entry box, with hidden characters
        password_entry.pack(pady=5)  # Pack the password entry box with vertical padding

        # Login button that processes the admin login when clicked
        ttk.Button(admin_frame, text="Login",
                   command=lambda: self.process_admin_login(email_entry.get(), password_entry.get())).pack(
            pady=10)  # Button to trigger admin login

        # Back button to return to the main menu
        ttk.Button(admin_frame, text="Back to Main Menu",
                   command=self.create_main_menu).pack(pady=5)  # Button to go back to the main menu

    # Method to display ticket information for available tickets
    def show_ticket_info(self):
        self.clear_window()  # Clear the window before displaying ticket information

        # Create a frame to display ticket details
        ticket_frame = ttk.Frame(self)  # Create a ttk.Frame to hold the ticket display
        ticket_frame.pack(expand=True, padx=20, pady=20)  # Pack the ticket frame with padding

        # Create and display a label for the "Available Tickets" title
        ttk.Label(ticket_frame, text="Available Tickets", font=("Arial", 18, "bold")).pack(
            pady=10)  # Title with bold text

        # Loop through all tickets and display each one
        for ticket in self.tickets:
            ticket_info = ttk.Frame(ticket_frame, relief="solid",
                                    borderwidth=1)  # Create a frame for each ticket with solid border
            ticket_info.pack(pady=10, padx=20, fill='x')  # Pack the ticket info frame with padding and horizontal fill

            # Display ticket details (type, price, validity, description, limitations)
            ttk.Label(ticket_info, text=ticket.get_ticket_type(), font=("Arial", 12, "bold")).pack(
                pady=5)  # Ticket type as bold text
            ttk.Label(ticket_info, text=f"Price: ${ticket.get_price()}").pack()  # Display the ticket price
            ttk.Label(ticket_info, text=f"Validity: {ticket.get_validity()}").pack()  # Display the ticket validity
            ttk.Label(ticket_info,
                      text=f"Description: {ticket.get_description()}").pack()  # Display the ticket description
            ttk.Label(ticket_info,
                      text=f"Limitations: {ticket.get_limitations()}").pack()  # Display any ticket limitations

        # Back button to return to the main menu
        ttk.Button(ticket_frame, text="Back to Main Menu",
                   command=self.create_main_menu).pack(pady=20)  # Button to navigate back to the main menu

    # Method to process customer login
    def process_login(self, email, password):
        # Loop through all customers to find a match based on email and password
        for customer in self.customers:
            if customer.get_email() == email and customer.check_password(password):  # Check if email and password match
                self.current_user = customer  # Set the current user as the matched customer
                self.show_customer_dashboard()  # Show the customer dashboard after successful login
                return  # Exit the method after successful login

        # Show an error message if no matching customer is found
        messagebox.showerror("Login Failed", "Invalid email or password")  # Display error message box

    # Method to process admin login
    def process_admin_login(self, email, password):
        # Loop through all admins to find a match based on email and password
        for admin in self.admins:
            if admin.get_email() == email and admin.check_password(password):  # Check if email and password match
                self.current_user = admin  # Set the current user as the matched admin
                self.show_admin_dashboard()  # Show the admin dashboard after successful login
                return  # Exit the method after successful login

        # Show an error message if no matching admin is found
        messagebox.showerror("Login Failed", "Invalid admin credentials")  # Display error message box

    # Method to process customer registration
    def process_registration(self, name, email, password, phone):
        # Validate if all fields are filled
        if not all([name, email, password, phone]):  # Check if any field is empty
            messagebox.showerror("Registration Error",
                                 "All fields are required")  # Show error message if any field is empty
            return  # Exit the method if validation fails

        # Validate email format
        if not self.validate_email(email):  # Check if email format is valid
            messagebox.showerror("Registration Error", "Invalid email format")  # Show error message for invalid email
            return  # Exit the method if validation fails

        # Validate phone number format
        if not self.validate_phone(phone):  # Check if phone number format is valid
            messagebox.showerror("Registration Error",
                                 "Invalid phone number format")  # Show error message for invalid phone
            return  # Exit the method if validation fails

        # Create new customer object
        new_customer = Customer(
            len(self.customers) + 1,  # Set a unique customer ID
            name,  # Customer's name
            email,  # Customer's email
            password,  # Customer's password
            phone  # Customer's phone number
        )

        # Add the new customer to the customers list and save the data
        self.customers.append(new_customer)  # Add the new customer to the list
        save_data("customers.pkl", self.customers)  # Save the updated customers list

        # Show success message and redirect to login page
        messagebox.showinfo("Success",
                            "Registration successful! Please login.")  # Inform user of successful registration
        self.show_login_page()  # Show the login page after registration

    # Method to validate the email format
    def validate_email(self, email):
        # Check if the email contains "@" and "."
        return "@" in email and "." in email  # Return True if both "@" and "." are present in the email, otherwise False

    # Method to validate the phone number format
    def validate_phone(self, phone):
        # Check if the phone number contains only digits and has a length of 10
        return phone.isdigit() and len(
            phone) == 10  # Return True if the phone number is numeric and exactly 10 characters long

    # Method to show the customer dashboard after successful login
    def show_customer_dashboard(self):
        self.clear_window()  # Clear the current window to set up the new screen

        # Create frame for the dashboard
        dashboard_frame = ttk.Frame(self)
        dashboard_frame.pack(expand=True, padx=20, pady=20)  # Pack the frame with padding

        # Display a welcome message with the customer's name
        ttk.Label(dashboard_frame,
                  text=f"Welcome, {self.current_user.get_name()}",  # Display the customer's name
                  font=("Arial", 18, "bold")).pack(pady=10)  # Bold text for the welcome message with padding

        # Create frame for the customer options
        options_frame = ttk.Frame(dashboard_frame)
        options_frame.pack(pady=20)  # Pack the options frame with padding

        # Buttons for customer options
        ttk.Button(options_frame, text="Purchase Tickets",
                   command=self.show_ticket_purchase).pack(pady=5, fill='x')  # Button to show ticket purchase page
        ttk.Button(options_frame, text="View My Reservations",
                   command=self.show_reservations).pack(pady=5, fill='x')  # Button to show reservations page
        ttk.Button(options_frame, text="Edit Profile",
                   command=self.show_edit_profile).pack(pady=5, fill='x')  # Button to edit customer profile
        ttk.Button(options_frame, text="Logout",
                   command=self.logout).pack(pady=5, fill='x')  # Button to log out the customer

    # Method to show the admin dashboard after successful login
    def show_admin_dashboard(self):
        self.clear_window()  # Clear the current window to set up the new screen

        # Create frame for the dashboard
        dashboard_frame = ttk.Frame(self)
        dashboard_frame.pack(expand=True, padx=20, pady=20)  # Pack the frame with padding

        # Display the "Admin Dashboard" title
        ttk.Label(dashboard_frame,
                  text="Admin Dashboard",  # Admin dashboard title
                  font=("Arial", 18, "bold")).pack(pady=10)  # Bold font for the title with padding

        # Create frame for the admin options
        options_frame = ttk.Frame(dashboard_frame)
        options_frame.pack(pady=20)  # Pack the options frame with padding

        # Buttons for admin options
        ttk.Button(options_frame, text="View Sales Report",
                   command=self.show_sales_report).pack(pady=5, fill='x')  # Button to view the sales report
        ttk.Button(options_frame, text="Manage Tickets",
                   command=self.show_ticket_management).pack(pady=5, fill='x')  # Button to manage tickets
        ttk.Button(options_frame, text="Manage Users",
                   command=self.show_user_management).pack(pady=5, fill='x')  # Button to manage users
        ttk.Button(options_frame, text="Logout",
                   command=self.logout).pack(pady=5, fill='x')  # Button to log out the admin

    # Method to show the ticket purchase page
    def show_ticket_purchase(self):
        self.clear_window()  # Clear the current window to set up the new screen

        # Create frame for the ticket purchase page
        purchase_frame = ttk.Frame(self)
        purchase_frame.pack(expand=True, padx=20, pady=20)  # Pack the frame with padding

        # Display the "Purchase Tickets" title
        ttk.Label(purchase_frame, text="Purchase Tickets",
                  font=("Arial", 18, "bold")).pack(pady=10)  # Bold font for the title with padding

        # Create a frame to display selected ticket information
        ticket_info_frame = ttk.Frame(purchase_frame)
        ticket_info_frame.pack(pady=10, fill='x')  # Pack the frame with padding and stretch it horizontally

        # Update ticket information when a ticket is selected
        def update_ticket_info(*args):
            # Clear previous ticket info
            for widget in ticket_info_frame.winfo_children():
                widget.destroy()

            # Get the selected ticket based on the dropdown selection
            selected_ticket_str = ticket_var.get()
            selected_ticket = next((t for t in self.tickets if str(t) == selected_ticket_str), None)

            if selected_ticket:  # If a ticket is selected, display its details
                ttk.Label(ticket_info_frame, text=selected_ticket.get_ticket_type(),
                          font=("Arial", 12, "bold")).pack(pady=5)
                ttk.Label(ticket_info_frame, text=f"Price: ${selected_ticket.get_price()}").pack()
                ttk.Label(ticket_info_frame, text=f"Validity: {selected_ticket.get_validity()}").pack()
                ttk.Label(ticket_info_frame, text=f"Description: {selected_ticket.get_description()}").pack()
                ttk.Label(ticket_info_frame, text=f"Limitations: {selected_ticket.get_limitations()}").pack()
                if selected_ticket.get_discount():  # If a discount is available, display it
                    ttk.Label(ticket_info_frame, text=f"Discount: {selected_ticket.get_discount()}").pack()

        # Dropdown to select the ticket
        ticket_var = tk.StringVar()
        ticket_var.trace('w', update_ticket_info)  # Bind the function to update info when the selection changes
        ticket_dropdown = ttk.Combobox(purchase_frame,
                                       textvariable=ticket_var,
                                       values=[str(ticket) for ticket in self.tickets])  # List all ticket types
        ticket_dropdown.pack(pady=10)  # Pack the dropdown with padding

        # Input field for the visit date
        ttk.Label(purchase_frame, text="Visit Date (YYYY-MM-DD):").pack()  # Label for the date input
        date_entry = ttk.Entry(purchase_frame)  # Entry field for the date
        date_entry.pack(pady=5)  # Pack the entry with padding

        # Radio buttons for payment method selection
        payment_var = tk.StringVar()  # Variable to store the selected payment method
        ttk.Label(purchase_frame, text="Payment Method:").pack()  # Label for payment method
        ttk.Radiobutton(purchase_frame, text="Credit Card",
                        variable=payment_var, value="Credit Card").pack()  # Credit card option
        ttk.Radiobutton(purchase_frame, text="Debit Card",
                        variable=payment_var, value="Debit Card").pack()  # Debit card option

        # Button to complete the ticket purchase
        ttk.Button(purchase_frame, text="Complete Purchase",
                   command=lambda: self.process_purchase(
                       ticket_var.get(),
                       date_entry.get(),
                       payment_var.get()
                   )).pack(pady=10)  # Trigger the process_purchase method with entered data

        # Button to go back to the customer dashboard
        ttk.Button(purchase_frame, text="Back to Dashboard",
                   command=self.show_customer_dashboard).pack()  # Go back to the dashboard page

    # Method to process ticket purchase
    def process_purchase(self, ticket_str, date, payment_method):
        # Check if all fields are filled
        if not all([ticket_str, date, payment_method]):
            messagebox.showerror("Purchase Error", "All fields are required")  # Display error if any field is missing
            return

        # Validate date format
        try:
            datetime.strptime(date, "%Y-%m-%d")  # Attempt to convert date to datetime object
        except ValueError:
            messagebox.showerror("Purchase Error", "Invalid date format")  # Display error if date format is incorrect
            return

        # Find the selected ticket
        ticket = next((t for t in self.tickets if str(t) == ticket_str), None)
        if not ticket:  # If ticket is not found, display error
            messagebox.showerror("Purchase Error", "Invalid ticket selection")
            return

        # Create a reservation object with the selected details
        reservation = Reservation(
            len(self.reservations) + 1,  # Reservation ID
            self.current_user,  # Associated customer
            ticket,  # Selected ticket
            date  # Selected date
        )

        # Create a payment object for the reservation
        payment = Payment(
            len(self.payments) + 1,  # Payment ID
            ticket.get_price(),  # Ticket price
            payment_method  # Selected payment method
        )

        # Link the reservation and payment
        reservation.set_payment(payment)  # Attach the payment to the reservation
        payment.set_reservation(reservation)  # Attach the reservation to the payment

        # Save the reservation and payment to the respective lists
        self.reservations.append(reservation)
        self.payments.append(payment)
        self.current_user.add_reservation(reservation)  # Add the reservation to the customer's profile

        # Save all data to storage files
        save_data("reservations.pkl", self.reservations)
        save_data("payments.pkl", self.payments)
        save_data("customers.pkl", self.customers)

        # Show success message and return to customer dashboard
        messagebox.showinfo("Success", "Ticket purchased successfully!")
        self.show_customer_dashboard()  # Display the dashboard after successful purchase

    # Method to show the sales report to admin
    def show_sales_report(self):
        self.clear_window()  # Clear the current window

        # Create a frame to hold the report
        report_frame = ttk.Frame(self)
        report_frame.pack(expand=True, padx=20, pady=20)

        # Add title to the report
        ttk.Label(report_frame, text="Sales Report",
                  font=("Arial", 18, "bold")).pack(pady=10)

        # Calculate statistics
        today = datetime.now().date()  # Get today's date
        today_sales = sum(1 for payment in self.payments
                          if datetime.strptime(payment.get_date(),
                                               "%Y-%m-%d").date() == today)  # Count payments made today
        total_revenue = sum(
            payment.get_amount() for payment in self.payments)  # Calculate total revenue from all payments

        # Display statistics
        ttk.Label(report_frame,
                  text=f"Tickets Sold Today: {today_sales}").pack(pady=5)  # Show number of tickets sold today
        ttk.Label(report_frame,
                  text=f"Total Revenue: ${total_revenue:.2f}").pack(pady=5)  # Show total revenue in formatted currency

        # Back button to return to the admin dashboard
        ttk.Button(report_frame, text="Back to Dashboard",
                   command=self.show_admin_dashboard).pack(pady=20)

    # Method to show the ticket management page to admin
    def show_ticket_management(self):
        self.clear_window()  # Clear the current window

        # Create a frame to manage tickets
        management_frame = ttk.Frame(self)
        management_frame.pack(expand=True, padx=20, pady=20)

        # Add a title for the ticket management section
        ttk.Label(management_frame, text="Ticket Management",
                  font=("Arial", 18, "bold")).pack(pady=10)

        # List all tickets for management
        for ticket in self.tickets:
            ticket_frame = ttk.Frame(management_frame)  # Create a frame for each ticket
            ticket_frame.pack(pady=5, fill='x')  # Pack the frame with padding and fill horizontally

            ttk.Label(ticket_frame, text=str(ticket)).pack(side='left')  # Display ticket information on the left

            # Create an entry field to update the ticket price
            price_var = tk.StringVar(value=str(ticket.get_price()))  # Bind the current price to the entry field
            price_entry = ttk.Entry(ticket_frame, textvariable=price_var, width=10)  # Create entry box for price
            price_entry.pack(side='right', padx=5)  # Pack entry field on the right side with padding

            # Button to update the ticket price
            ttk.Button(ticket_frame, text="Update Price",
                       command=lambda t=ticket, p=price_var: self.update_ticket_price(t, p.get())).pack(
                side='right')  # Button for updating the price

        # Back button to return to the admin dashboard
        ttk.Button(management_frame, text="Back to Dashboard",
                   command=self.show_admin_dashboard).pack(pady=20)

    # Method to update the price of a ticket
    def update_ticket_price(self, ticket, new_price):
        try:
            price = float(new_price)  # Attempt to convert the new price to a float
            if price <= 0:  # Check if the price is valid (greater than 0)
                raise ValueError  # Raise an error if the price is invalid
            ticket.set_price(price)  # Set the new price for the ticket
            save_data("tickets.pkl", self.tickets)  # Save the updated tickets data to file
            messagebox.showinfo("Success", "Ticket price updated successfully!")  # Show success message
        except ValueError:  # Handle any value errors (e.g., non-numeric input or invalid price)
            messagebox.showerror("Error", "Invalid price value")  # Show error message if price is invalid

    # Method to display the user management interface for admins
    def show_user_management(self):
        self.clear_window()  # Clear the current window

        management_frame = ttk.Frame(self)  # Create a frame for user management
        management_frame.pack(expand=True, padx=20, pady=20)

        ttk.Label(management_frame, text="User Management",  # Title label
                  font=("Arial", 18, "bold")).pack(pady=10)

        # Loop through all customers and display them with a delete option
        for customer in self.customers:
            user_frame = ttk.Frame(management_frame)  # Create a frame for each user
            user_frame.pack(pady=5, fill='x')

            ttk.Label(user_frame, text=str(customer)).pack(side='left')  # Show user details
            ttk.Button(user_frame, text="Delete",  # Add a delete button for each user
                       command=lambda c=customer: self.delete_user(c)).pack(side='right')  # Delete user when clicked

        # Back button to return to the admin dashboard
        ttk.Button(management_frame, text="Back to Dashboard",
                   command=self.show_admin_dashboard).pack(pady=20)

    # Method to delete a user from the system
    def delete_user(self, customer):
        # Show a confirmation message before deleting
        if messagebox.askyesno("Confirm Delete",
                               f"Are you sure you want to delete user {customer.get_name()}?"):
            self.customers.remove(customer)  # Remove the customer from the list
            save_data("customers.pkl", self.customers)  # Save the updated customer list
            messagebox.showinfo("Success", "User deleted successfully!")  # Show success message
            self.show_user_management()  # Refresh the user management interface

    # Method to display the user's reservations
    def show_reservations(self):
        self.clear_window()  # Clear the window for the reservations page

        # Create frame to hold the reservation details
        reservations_frame = ttk.Frame(self)
        reservations_frame.pack(expand=True, padx=20, pady=20)

        ttk.Label(reservations_frame, text="My Reservations",
                  font=("Arial", 18, "bold")).pack(pady=10)

        # Loop through the current user's reservations and display them
        for reservation in self.current_user.get_reservations():
            reservation_frame = ttk.Frame(reservations_frame)
            reservation_frame.pack(pady=5, fill='x')

            ttk.Label(reservation_frame, text=str(reservation)).pack(side='left')

            # Button to cancel the reservation
            ttk.Button(reservation_frame, text="Cancel",
                       command=lambda r=reservation: self.cancel_reservation(r)).pack(side='right')

        # Button to go back to the dashboard
        ttk.Button(reservations_frame, text="Back to Dashboard",
                   command=self.show_customer_dashboard).pack(pady=20)

    # Method to cancel a reservation
    def cancel_reservation(self, reservation):
        # Confirm the cancellation with the user
        if messagebox.askyesno("Confirm Cancellation",
                               "Are you sure you want to cancel this reservation?"):
            # Remove the reservation from the main list and the user's list
            self.reservations.remove(reservation)
            self.current_user.get_reservations().remove(reservation)

            # Save updated data to files
            save_data("reservations.pkl", self.reservations)
            save_data("customers.pkl", self.customers)

            # Inform the user that the cancellation was successful
            messagebox.showinfo("Success", "Reservation cancelled successfully!")

            # Show updated list of reservations
            self.show_reservations()

    # Method to show the edit profile page
    def show_edit_profile(self):
        # Clear the current window to prepare for the edit profile page
        self.clear_window()

        # Create a frame for the profile editing section
        profile_frame = ttk.Frame(self)
        profile_frame.pack(expand=True, padx=20, pady=20)  # Add the frame to the window with padding

        # Label for the title of the page
        ttk.Label(profile_frame, text="Edit Profile",
                  font=("Arial", 18, "bold")).pack(pady=10)  # Display title with bold and larger font

        # Create and display the 'Name' field
        ttk.Label(profile_frame, text="Name:").pack()  # Display label 'Name'
        name_entry = ttk.Entry(profile_frame)  # Create an entry box for the name
        name_entry.insert(0, self.current_user.get_name())  # Pre-fill the entry box with the current user's name
        name_entry.pack(pady=5)  # Pack the entry box with padding

        # Create and display the 'Email' field
        ttk.Label(profile_frame, text="Email:").pack()  # Display label 'Email'
        email_entry = ttk.Entry(profile_frame)  # Create an entry box for the email
        email_entry.insert(0, self.current_user.get_email())  # Pre-fill the entry box with the current user's email
        email_entry.pack(pady=5)  # Pack the entry box with padding

        # Create and display the 'Phone' field
        ttk.Label(profile_frame, text="Phone:").pack()  # Display label 'Phone'
        phone_entry = ttk.Entry(profile_frame)  # Create an entry box for the phone number
        phone_entry.insert(0,
                           self.current_user.get_phone_number())  # Pre-fill the entry box with the current user's phone number
        phone_entry.pack(pady=5)  # Pack the entry box with padding

        # Create and display the 'Save Changes' button
        ttk.Button(profile_frame, text="Save Changes",  # Button to save changes
                   command=lambda: self.save_profile_changes(  # Call save_profile_changes with current inputs
                       name_entry.get(),  # Get the name entered by the user
                       email_entry.get(),  # Get the email entered by the user
                       phone_entry.get()  # Get the phone number entered by the user
                   )).pack(pady=10)  # Pack the button with padding

        # Create and display the 'Back to Dashboard' button
        ttk.Button(profile_frame, text="Back to Dashboard",
                   command=self.show_customer_dashboard).pack()  # Button to go back to the dashboard

    # Method to save changes to the user's profile
    def save_profile_changes(self, name, email, phone):
        # Check if the provided email format is valid using the validate_email method
        if not self.validate_email(email):
            # Show an error message if the email is invalid
            messagebox.showerror("Error", "Invalid email format")
            return  # Exit the method if the email is invalid

        # Check if the provided phone number format is valid using the validate_phone method
        if not self.validate_phone(phone):
            # Show an error message if the phone number is invalid
            messagebox.showerror("Error", "Invalid phone number format")
            return  # Exit the method if the phone number is invalid

        # Update the current user's information with the new values
        self.current_user._User__name = name  # Update the user's name
        self.current_user._User__email = email  # Update the user's email
        self.current_user._Customer__phone_number = phone  # Update the user's phone number

        # Save the updated list of customers to a file using the save_data function
        save_data("customers.pkl", self.customers)

        # Display a success message to the user
        messagebox.showinfo("Success", "Profile updated successfully!")

        # Return to the customer dashboard after updating the profile
        self.show_customer_dashboard()

    # Method to log out the current user
    def logout(self):
        # Set the current_user to None, effectively logging out the user
        self.current_user = None

        # Call the method to display the main menu after logout
        self.create_main_menu()

    # Method to clear all widgets from the window
    def clear_window(self):
        # Loop through each widget in the window and destroy it
        for widget in self.winfo_children():
            widget.destroy()


# Check if the script is being run directly
if __name__ == "__main__":
    # Create an instance of the AdventureLandApp class
    app = AdventureLandApp()
    # Start the Tkinter event loop to run the application
    app.mainloop()

