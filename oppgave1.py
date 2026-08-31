import random
import secrets
import string
"""
Scenariet
Høgskolen skal ta imot nye studenter. Hver student trenger et brukernavn og et midlertidig passord. Dette skal
ikke gjøres manuelt av en saksbehandler, det skal genereres av et program.
Programmet ditt skal spørre om navn, la brukeren velge hvor sterkt passordet skal være, og skrive ut kontoen.
Det høres enkelt ut. Det interessante ligger i ett spørsmål: hvor kommer tilfeldigheten fra? Det er hele
poenget med oppgaven, og det er derfor random og secrets begge er med i temalista
"""




def generate_username(first_name, last_name): #her kan man fatkisk bruke random, fordi brukernavn er som regel alltid public
    first_name= "".join(ch for ch in first_name.lower() if ch.isalnum())
    last_name= "".join(ch for ch in last_name.lower() if ch.isalnum())
    number= "".join(secrets.choice(string.digits) for x in range(4))



    return first_name[:3] + last_name[:3] + number

test = [generate_username("Nicolas-,", "Cook") for _ in range(3)]

for x in test:
    print("brukernavn:", x)




def generate_password(length,strength):
    if not 8 <= length <= 20:
        raise ValueError ("Feil lengde, prøv igjen")
    if strength == 1:
        characters= string.ascii_lowercase + string.digits
        weak_pw = ''.join(random.choices(characters, k=length))
        return weak_pw
    elif strength == 2:
        characters= string.ascii_lowercase + string.digits + string.ascii_uppercase
        medium_pw= "".join(secrets.choice(characters) for _ in range(length))
        return medium_pw
    elif strength== 3:

        special = "!@#$%^&*"
        characters = string.ascii_lowercase + string.digits + string.ascii_uppercase + special
        required = [
            secrets.choice(string.ascii_lowercase),
            secrets.choice(string.ascii_uppercase),
            secrets.choice(string.digits),
            secrets.choice(special)
        ]

        required += [secrets.choice(characters) for _ in range(length - 4)]
        secrets.SystemRandom().shuffle(required)

        return ''.join(required)

    else:
        raise ValueError("Feil styrke, må være 1, 2, or 3.")




def main():
    first_name = input("Enter first name: ").strip()
    last_name = input("Enter last name: ").strip()

    print("\n1. Low")
    print("2. Medium")
    print("3. Strong")
    try:
        strength = int(input("Choose password strength: "))
        length = int(input("Enter password length (8-20): "))
        username = generate_username(first_name, last_name)
        password = generate_password(length, strength)
        print("\nGenerated account")
        print("Username:", username)
        print("Password:", password)
    except ValueError as exc:
        print("Error:", exc)



if __name__ == "__main__":
    main()




#testing
""""
print("weak", generate_password(10,1))
print("weak", generate_password(10,1))
print("medium",generate_password(10,2))
print("medium", generate_password(10,2))
print("strong",generate_password(10,3))
print("strong", generate_password(10,3))
"""