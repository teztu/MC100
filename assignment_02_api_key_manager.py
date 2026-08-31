"""
Scenariet

En virksomhet har flere applikasjoner som trenger en unik identifikator og en sikker API-token.
Dette skal ikke håndteres manuelt, men administreres gjennom et Python-program.

Når en ny applikasjon opprettes, skal programmet generere en unik UUID ved hjelp av uuid.uuid4()
og en sikker API-token ved hjelp av secrets.token_hex(32).

Applikasjonene lagres i en dictionary der UUID-en brukes som unik identifikator.
Hver UUID er knyttet til informasjon om applikasjonen, som navn og API-token.

Programmet skal la brukeren:
- Opprette en ny applikasjon
- Generere en ny API-token for en eksisterende applikasjon
- Søke etter en applikasjon ved hjelp av UUID
- Vise alle registrerte applikasjoner
- Avslutte programmet

Når en ny API-token genereres, skal den gamle tokenen erstattes.
Hvis en UUID ikke finnes, skal programmet gi en passende feilmelding.

API-tokenen er sensitiv informasjon og bør derfor ikke vises i sin helhet når alle
applikasjoner listes. Kun deler av tokenen skal være synlig.

Poenget med oppgaven er å øve på:
- secrets
- uuid
- dictionaries
- nested dictionaries
- functions
- loops
- sikker håndtering av API-tokens
"""

import secrets
import uuid

applications={}


def create_application(name):
    app_id= str(uuid.uuid4())
    token= secrets.token_hex(32)
    applications[app_id] = {}

    applications[app_id]["name"] = name
    applications[app_id]["token"] = token

    return app_id, token
def new_token_generation(app_id):
    application = applications.get(app_id)  # henter verdien fra dict med .get
    if application is not None:
        new_token = secrets.token_hex(32)  # generer ny token
        applications[app_id]["token"] = new_token  # erstatter gammel token med ny
        print("New token is successfully created")
        return new_token


    else:
        print("Application not found")
        return None

def search_application(app_id):
    return applications.get(app_id) #forventet resultat er innholdet til UUID application, får None om den er tom

def hide_api_token(token):
    pass
def display_application():
    if not applications:
        print("No applications available.")
        return
    for app_id, data in applications.items():
        print(f"\nName: {data['name']}")
        print(f"UUID: {app_id}")
        hide_token = data["token"][:4] + "*" * (len(data["token"]) - 8) + data["token"][-4:]

        print(f"TOKEN: {hide_token}")


def main():
    while True:
        print("\n--- API Key and Identifier Manager ---")
        print("1. Create Application")
        print("2. Generate New API Token")
        print("3. Search Application")
        print("4. Display Applications")
        print("5. Exit")


        choice = input("Enter choice " ).strip()
        if choice=="1":
            name=input("Enter a new application name")

            app_id, token= create_application(name) #henter verdiene fra funksjonen
            print("Application has been created")
            print(f'UUID is: {app_id} \nAPI-Token is: {token}')
        elif choice=="2":
            app_id = input ("Enter application UUID: ")
            new_token=new_token_generation(app_id)
            if new_token is not None:
                print("Successfully created new API_Token")
            else:
                print("Wrong UUID, try again")



        elif choice=="3":
            app_id= input("Type your UUID to search:")
            application= search_application(app_id)
            if application is not None:
                print(application)
            else:
                print("This application does not exist")

        elif choice=="4":
            display_application()

        elif choice=="5":
            print("Program exit complete")
            break

        else:
            print("Please choose from the list")
            continue

if __name__ == "__main__":
    main()
