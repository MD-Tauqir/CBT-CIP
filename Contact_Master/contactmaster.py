import sqlite3
import csv
import os

class ContactVault:
    def __init__(self, db_filename='Contacts.db', csv_filename='Contacts.csv'):
        self.db_filename = db_filename
        self.csv_filename = csv_filename
        self.conn = sqlite3.connect(self.db_filename)
        self.create_table()

    def create_table(self):
        """Create the contacts table if not already present."""
        with self.conn:
            self.conn.execute('''
                CREATE TABLE IF NOT EXISTS contacts (
                    name TEXT PRIMARY KEY,
                    phone_number TEXT,
                    work TEXT,
                    company TEXT,
                    title TEXT,
                    email TEXT,
                    groups TEXT
                )
            ''')

    def build_insert_query(self, name, phone_number, work, company, title, email, groups):
        """Build the SQL insert query with only the fields that have values."""
        columns = ['name']
        values = [name]
        if phone_number:
            columns.append('phone_number')
            values.append(phone_number)
        if work:
            columns.append('work')
            values.append(work)
        if company:
            columns.append('company')
            values.append(company)
        if title:
            columns.append('title')
            values.append(title)
        if email:
            columns.append('email')
            values.append(email)
        if groups:
            columns.append('groups')
            values.append(','.join(groups))

        columns_str = ', '.join(columns)
        placeholders = ', '.join(['?'] * len(values))
        query = f'INSERT OR REPLACE INTO contacts ({columns_str}) VALUES ({placeholders})'
        return query, values

    def add_contact(self, name, phone_number=None, work=None, company=None, title=None, email=None, groups=None):
        """Add a new contact or update an existing one with a confirmation."""
        if not name:
            print("Error: Contact name is required.")
            return
        
        # Check if the contact already exists
        cursor = self.conn.execute('SELECT * FROM contacts WHERE name = ?', (name,))
        existing_contact = cursor.fetchone()
        
        if existing_contact:
            print(f"A contact with the name '{name}' already exists.")
            overwrite = input("Do you want to overwrite the existing contact? (y/n): ").strip().lower()
            if overwrite != 'y':
                print("Contact not added/updated.")
                return

        # Proceed to add/update the contact
        query, values = self.build_insert_query(name, phone_number, work, company, title, email, groups)
        with self.conn:
            self.conn.execute(query, values)
        print(f"Contact added/updated: {name}")

    def delete_contact(self, name):
        """Delete a contact if it exists."""
        with self.conn:
            cursor = self.conn.execute('DELETE FROM contacts WHERE name = ?', (name,))
            if cursor.rowcount > 0:
                print(f"Contact deleted: {name}")
            else:
                print(f"Error: Contact not found: {name}")

    def search_contact(self, name):
        """Search for a contact and display it."""
        cursor = self.conn.execute('SELECT * FROM contacts WHERE name = ?', (name,))
        contact = cursor.fetchone()
        if contact:
            print(f"Contact found: {name}")
            keys = ['name', 'phone_number', 'work', 'company', 'title', 'email', 'groups']
            for key, value in zip(keys, contact):
                if value:
                    print(f"{key.replace('_', ' ').capitalize()}: {value}")
        else:
            print(f"Error: Contact not found: {name}")

    def display_contacts(self):
        """Display all contacts."""
        cursor = self.conn.execute('SELECT * FROM contacts')
        contacts = cursor.fetchall()
        if not contacts:
            print("No contacts available.")
        else:
            print("\nContact List:")
            for contact in contacts:
                print("-" * 20)
                print(f"Name: {contact[0]}")  # Assuming 'name' is the first column
                keys = ['phone_number', 'work', 'company', 'title', 'email', 'groups']
                for key, value in zip(keys, contact[1:]):  # Start from index 1
                    if value:
                        print(f"{key.replace('_', ' ').capitalize()}: {value}")
                print("-" * 20)

    def edit_contact(self, name):
        """Edit an existing contact."""
        cursor = self.conn.execute('SELECT * FROM contacts WHERE name = ?', (name,))
        contact = cursor.fetchone()
        if contact:
            print(f"Editing contact: {name}")
            
            phone_number = input(f"Enter new phone number (current: {contact[1]}): ") or contact[1]
            work = input(f"Enter new work (current: {contact[2]}): ") or contact[2]
            company = input(f"Enter new company (current: {contact[3]}): ") or contact[3]
            title = input(f"Enter new title (current: {contact[4]}): ") or contact[4]
            email = input(f"Enter new email (current: {contact[5]}): ") or contact[5]
            groups = input(f"Enter new groups (comma-separated, current: {contact[6]}): ")
            groups = [group.strip() for group in groups.split(',')] if groups else contact[6].split(',')
            
            self.add_contact(name, phone_number, work, company, title, email, groups)
            print(f"Contact updated: {name}")
        else:
            print(f"Error: Contact not found: {name}")

    def export_to_csv(self):
        """Export contacts to a CSV file."""
        cursor = self.conn.execute('SELECT * FROM contacts')
        contacts = cursor.fetchall()

        try:
            with open(self.csv_filename, 'w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(['Name', 'Phone Number', 'Work', 'Company', 'Title', 'Email', 'Groups'])
                for contact in contacts:
                    writer.writerow(contact)
            print(f"Contacts exported to CSV: {self.csv_filename}")
        except IOError as e:
            print(f"Error: Unable to write to file {self.csv_filename}: {e}")

    def bulk_add_contacts(self, csv_file):
        """Add multiple contacts from a CSV file."""
        try:
            with open(csv_file, 'r') as file:
                reader = csv.reader(file)
                next(reader)  # Skip the header row
                for row in reader:
                    if len(row) < 1:
                        continue  # Skip any empty rows
                    name, phone_number, work, company, title, email, groups = row[0], row[1], row[2], row[3], row[4], row[5], row[6]
                    groups = [group.strip() for group in groups.split(',')] if groups else []
                    self.add_contact(name, phone_number, work, company, title, email, groups)
            print(f"Bulk contacts added from {csv_file}.")
        except FileNotFoundError:
            print(f"Error: File {csv_file} not found.")
        except Exception as e:
            print(f"Error processing file {csv_file}: {e}")

    def __del__(self):
        """Close the database connection on deletion of the object."""
        self.conn.close()

def main():
    cm = ContactVault()
    
    while True:
        print("\nContactVault Menu:")
        print("1. Add Contact")
        print("2. Delete Contact")
        print("3. Search Contact")
        print("4. Display Contacts")
        print("5. Edit Contact")
        print("6. Export to CSV")
        print("7. Bulk Add Contacts")
        print("8. Exit")
        
        choice = input("Enter your choice (1-8): ")
        
        if choice == '1':
            name = input("Enter contact name: ")
            phone_number = input("Enter phone number: ")
            work = input("Enter work (optional): ")
            company = input("Enter company (optional): ")
            title = input("Enter title (optional): ")
            email = input("Enter email (optional): ")
            groups = input("Enter groups (optional, comma-separated): ")
            groups = [group.strip() for group in groups.split(',')] if groups else []
            cm.add_contact(name, phone_number, work, company, title, email, groups)
        elif choice == '2':
            name = input("Enter contact name to delete: ")
            cm.delete_contact(name)
        elif choice == '3':
            name = input("Enter contact name to search: ")
            cm.search_contact(name)
        elif choice == '4':
            cm.display_contacts()
        elif choice == '5':
            name = input("Enter contact name to edit: ")
            cm.edit_contact(name)
        elif choice == '6':
            cm.export_to_csv()
        elif choice == '7':
            csv_file = input("Enter the CSV file path for bulk add: ")
            cm.bulk_add_contacts(csv_file)
        elif choice == '8':
            print("Exiting ContactVault.")
            break
        else:
            print("Invalid choice. Please enter a number between 1 and 8.")

if __name__ == "__main__":
    main()
