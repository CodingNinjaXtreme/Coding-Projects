import json
import os

CONTACTS_FILE = "contacts.json"

def load_contacts():
    if os.path.exists(CONTACTS_FILE):
        with open(CONTACTS_FILE, "r") as f:
            return json.load(f)
    return []

def save_contacts(contacts):
    with open(CONTACTS_FILE, "w") as f:
        json.dump(contacts, f, indent=2)

def create_contact(name, email, phone):
    return {
        "name": name,
        "email": email,
        "phone": phone
    }

def display_contact(contact):
    print(f"Name: {contact['name']}")
    print(f"Email: {contact['email']}")
    print(f"Phone: {contact['phone']}")

def search_contact(contacts, name):
    for contact in contacts:
        if contact['name'].lower() == name.lower():
            return contact
    return None

def delete_contact(contacts, name):
    for i, contact in enumerate(contacts):
        if contact['name'].lower() == name.lower():
            del contacts[i]
            return True
    return False

def list_contacts(contacts):
    if not contacts:
        print("No contacts found.")
    else:
        for idx, contact in enumerate(contacts, 1):
            print(f"\nContact {idx}:")
            display_contact(contact)

def main():
    contacts = load_contacts()
    while True:
        print("\nContact List Manager")
        print("1. Add new contact")
        print("2. Search contact by name")
        print("3. List all contacts")
        print("4. Delete contact by name")
        print("5. Exit")
        choice = input("Choose an option (1-5): ")
        if choice == "1":
            name = input("Please enter the name of the contact you wish to create: ")
            email = input("Please enter the email of the contact: ")
            phone = input("Please enter the phone number of the contact: ")
            contact = create_contact(name, email, phone)
            contacts.append(contact)
            save_contacts(contacts)
            print("Contact created successfully!")
            display_contact(contact)
        elif choice == "2":
            name = input("Enter the name to search: ")
            result = search_contact(contacts, name)
            if result:
                print("Contact found:")
                display_contact(result)
            else:
                print("Contact not found.")
        elif choice == "3":
            list_contacts(contacts)
        elif choice == "4":
            name = input("Enter the name of the contact to delete: ")
            if delete_contact(contacts, name):
                save_contacts(contacts)
                print("Contact deleted successfully.")
            else:
                print("Contact not found.")
        elif choice == "5":
            print("Goodbye!")
            break
        else:
            print("Invalid option. Please try again.")

if __name__ == "__main__":
    main()