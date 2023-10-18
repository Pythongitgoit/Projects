from collections import UserDict


def user_error(func):
    def inner(*args):
        try:
            return func(*args)
        except IndexError:
            return "Not enough params."
        except KeyError:
            return "Unknown record_id."
        except ValueError:
            return "Error: Invalid value format. Please enter valid data."

    return inner


class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)


class Name(Field):
    pass


class Phone(Field):
    def __init__(self, value):
        if len(value) != 10 or not value.isdigit():
            raise ValueError("Incorrect phone number format")
        super().__init__(value)


class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []

    def add_phone(self, phone):
        if len(self.phones) < 2:
            phone_item = Phone(phone)
            self.phones.append(phone_item)
        else:
            raise ValueError("A contact can have at most 2 phones")

    def remove_phone(self, phone):
        self.phones = [p for p in self.phones if p.value != phone]

    def edit_phone(self, old_phone, new_phone):
        if len(new_phone) != 10 or not new_phone.isdigit():
            raise ValueError("Incorrect phone number format")

        found = False

        for phone_item in self.phones:
            if phone_item.value == old_phone:
                phone_item.value = new_phone
                found = True

        if not found:
            raise ValueError("The Number Does Not Exist")

    def find_phone(self, phone):
        for phone_item in self.phones:
            if phone_item.value == phone:
                return phone_item
        return None

    def __str__(self):
        phone_str = "; ".join(str(p) for p in self.phones)
        return f"Contact name: {self.name.value}, phones: {phone_str}"


class AddressBook(UserDict):
    def add_record(self, record):
        self.data[record.name.value] = record

    def find(self, name):
        return self.data.get(name)

    def delete(self, name):
        if name in self.data:
            del self.data[name]

    def show_all_contacts(self):
        for record in self.values():
            print(record)

    def add_contact(self, name, phone1, phone2=None):
        if name:
            if name in self.data:
                print(
                    f"A contact with the name '{name}' already exists. Choose a different name or use 'edit'."
                )
                return

            if len(phone1) != 10 or not phone1.isdigit():
                print(
                    "Error: Incorrect phone for phone1. Please enter a 10-digit phone number."
                )
                return
            if phone2 and (len(phone2) != 10 or not phone2.isdigit()):
                print(
                    "Error: Incorrect phone for phone2. Please enter a 10-digit phone number."
                )

                return

            record = Record(name)
            record.add_phone(phone1)

            if phone2:
                record.add_phone(phone2)

            self.add_record(record)
            print(f"Contact '{name}' added.")
        else:
            print("Error: Invalid contact name.")

    def find_contact(self, name):
        found_record = self.find(name)
        if found_record:
            print(found_record)
        else:
            print(f"Contact '{name}' not found.")

    def delete_contact(self, name):
        if name in self.data:
            del self.data[name]
            print(f"Contact '{name}' deleted.")
        else:
            print(f"Contact '{name}' not found.")


def parse_command(command):
    parts = command.split()
    if len(parts) < 1:
        print("Invalid command. Please enter a valid command.")
        return None, []
    action = parts[0]
    args = parts[1:]
    return action, args


@user_error
def main():
    book = AddressBook()

    while True:
        user_input = input(
            "Enter a command (add/show(2)/find/edit/delete/exit(e)): "
        ).strip()

        if user_input == "exit" or user_input == "e":
            print("Goodbye!")
            break

        action, args = parse_command(user_input)

        if action == "add":
            if len(args) >= 2:
                name = args[0]
                phone1 = args[1]
                phone2 = args[2] if len(args) >= 3 else None
                book.add_contact(name, phone1, phone2)
            else:
                print("Invalid arguments for 'add' command.")

        elif action == "show" or action == "2":
            book.show_all_contacts()

        elif action == "edit":
            if len(args) == 3:
                name = args[0]
                old_phone = args[1]
                new_phone = args[2]

                record = book.find(name)

                if record:
                    try:
                        record.edit_phone(old_phone, new_phone)
                        print(f"Phone number for '{name}' edited successfully.")
                    except ValueError as e:
                        print(str(e))
                else:
                    print(f"Contact '{name}' not found.")
            else:
                print("Invalid arguments for 'edit' command.")

        elif action == "find":
            if len(args) == 1:
                name = args[0]
                book.find_contact(name)
            else:
                print("Invalid arguments for 'find' command.")

        elif action == "delete":
            if len(args) == 1:
                name = args[0]
                book.delete_contact(name)
            else:
                print("Invalid arguments for 'delete' command.")

        else:
            print("Unknown command. Try again.")


if __name__ == "__main__":
    main()
