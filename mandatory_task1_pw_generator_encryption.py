# Password generator and its encryption

import secrets
import string
from cryptography.fernet import Fernet


class PasswordGenerator:

    def __init__(self):

        self.__password = ""
        self.__key = None
        self.__fernet = None


    def generate_password(self, length, lower, upper, digits, symbols):
        #checks password length
        if not 8 <= length <= 20:
            raise ValueError("Password length must be between 8 and 20")

        characters = "" #all signs program can choose from
        required = [] # all signs that HAVE to be included

        if lower == "y":
            characters += string.ascii_lowercase
            required.append(secrets.choice(string.ascii_lowercase))

        if upper == "y":
            characters += string.ascii_uppercase
            required.append(secrets.choice(string.ascii_uppercase))

        if digits == "y":
            characters += string.digits
            required.append(secrets.choice(string.digits))

        if symbols == "y":
            special = "!@#$%^&*"
            characters += special
            required.append(secrets.choice(special))

        if not characters: #ensures character strength of atleast 1
            raise ValueError("You must select at least one character type")

        #completes remaining password length
        required += [secrets.choice(characters) for _ in range(length - len(required))]

        #secret shuffle to avoid pattern of having same type of symbols in the same order
        secrets.SystemRandom().shuffle(required)

        self.__password = "".join(required) # turns list to string and saves it inside the object

        return self.__password


    def generate_key(self):

        #create fernet key
        self.__key = Fernet.generate_key()

        #save key that is generated
        self.__fernet = Fernet(self.__key)

        return self.__key


    def use_existing_key(self, entered_key):
        #encodes input key
        self.__key = entered_key.encode()

        #assigns new chosen key
        self.__fernet = Fernet(self.__key)

        return self.__key


    def encrypt_password(self):
        #encodes current password
        encrypted_password = self.__fernet.encrypt(self.__password.encode())

        return encrypted_password


    def decrypt_password(self, encrypted_password):

        decrypted_password = self.__fernet.decrypt(encrypted_password).decode()

        return decrypted_password


    def verify_password(self, encrypted_password):

        decrypted_password = self.decrypt_password(encrypted_password)

        return decrypted_password == self.__password #verify that decrypting returns the original password


#ensures correct user input
def ask_yes_no(question):

    while True:
        answer = input(question).strip().lower()

        if answer == "y" or answer == "n":
            return answer

        print("Invalid user input. Please enter 'y' or 'n'.")



def ask_length():

    while True:#ensuring password length is strong

        try:
            length = int(input("Enter your desired password length (8-20): "))

            if 8 <= length <= 20:
                return length

            print("Password length must be between 8 and 20.")

        except ValueError:
            print("Please enter a number.")


def choose_key(generator):

    while True:
        # allows the user to choose key
        print("\nKey options:")
        print("1. Generate Fernet key")
        print("2. Use your own Fernet key")

        choice = input("Choose key option: ").strip()

        if choice == "1":
            return generator.generate_key()

        elif choice == "2":

            entered_key = input("Enter existing Fernet key: ").strip()

            try:
                return generator.use_existing_key(entered_key)

            except ValueError:
                print("Invalid Fernet key. Please try again.")

        else:
            print("Invalid choice. Enter 1 or 2.")


def main():

    print("Welcome to your password generator")

    #initiating object
    generator = PasswordGenerator()
    length = ask_length()

    #charachter types
    while True:
        lower = ask_yes_no("Use lowercase? y/n: ")
        upper = ask_yes_no("Use uppercase? y/n: ")
        digits = ask_yes_no("Use digits? y/n: ")
        symbols = ask_yes_no("Use symbols? y/n: ")

        if "y" in (lower, upper, digits, symbols):
            break

        print("\n you must have atleast one character type. "
              "The more types, the stronger the password.")


    password = generator.generate_password(
        length,
        lower,
        upper,
        digits,
        symbols
    )

    print("\nGenerated password:", password)


    #user can choose to make new key, or use an existing one
    key = choose_key(generator)

    print("Key:", key)


    #encrypt password
    encrypted_password = generator.encrypt_password()

    print("Encrypted password:", encrypted_password)


    #decrypt password
    decrypted_password = generator.decrypt_password(encrypted_password)

    print("Decrypted password:", decrypted_password)


    #verification that key is working correctly
    if generator.verify_password(encrypted_password):
        print("ENCRYPTION and DECRYPTION VERIFIED")

    else:
        print("Verification failed")


if __name__ == "__main__":
    main()
