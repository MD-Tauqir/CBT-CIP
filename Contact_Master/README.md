# CBT-CIP
# TASK 2 CONTACT_MASTER
# Overview
# CONTACT_MASTER
Contact Master is a simple, yet powerful contact management system implemented in Python. It allows users to add, edit, search, delete, and export contacts in various formats. Additionally, it supports bulk importing of contacts from a CSV file.
# Table of Contents
* Features
* Installation
* Commands
* Project Structure
* Technologies Used
# Features
* **Add Contact:** Add new contacts with details like name, phone number, work, company, title, email, and groups.
* **Edit Contact:** Update existing contact information.
* **Delete Contact:** Remove a contact from the database.
* **Search Contact:** Search and display contact details.
* **Display Contacts:** View all contacts stored in the database.
* **Export to CSV:** Export the contact list to a CSV file.
* **Bulk Add Contacts:** Import multiple contacts from a CSV file.

# Installation
```bash
git clone https://github.com/MD-Tauqir/CBT-CIP.git
cd Contact_Master
python contactmaster.py
```
# Commands
* **Add Contact:** Follow the prompts to add a new contact.
* **Delete Contact:** Provide the name of the contact you want to delete.
* **Search Contact:** Enter the name of the contact you want to search for.
* **Display Contacts:** Lists all contacts.
* **Edit Contact:** Select a contact to update its details.
* **Export to CSV:** Saves all contacts to a CSV file named Contacts.csv.
* **Bulk Add Contacts:** Provide the path to a CSV file to import multiple contacts.

# Project Structure
```bash
Contact_Master/
│
├── contactmaster.py      # Main application file
├── Contacts.db          # SQLite database file
└── README.md            # Documentation
```

# Technologies Used
***Python:** Programming language used for the project.
***SQLite:** Database to store contacts.
***CSV:** Format for importing and exporting contacts.
