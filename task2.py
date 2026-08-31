#pip install cryptography

from cryptography.fernet import Fernet

#genererer key for encryption og decryption
key = Fernet.generate_key()

#bruker key i fernet instanset
fernet= Fernet(key)

print("encryption/decryption key:", key)
print("fernet objekt:", fernet) # objekt


# we will be encrypting the below string.
message = "hello friends"


encryptedMessage= fernet.encrypt(message.encode())

print("encrypted message:", encryptedMessage)
print("original message:", message)

# decrypt the encrypted string with the # Fernet instance of the key,
#altså bruker encrypted message og gjør om til message orignal via fernet decrypt)
decryptedMessage = fernet.decrypt(encryptedMessage).decode()
print("decrypted string: ", decryptedMessage)


# Caesar Cipher


def caesar_cipher_encrypt(plaintext, key): #plaintext= tekst jeg vil kryptere
    encrypted_text = ""
    for char in plaintext.upper(): #for hver karakter i plaintext(gjort om til uppercases)
        if char.isalpha(): #hvis tegn er en bokstav, så flyttes den
            encrypted_text += chr((ord(char) - 65 + key) % 26 + 65)

        else:
            encrypted_text += char
    return encrypted_text

def caesar_cipher_decrypt(ciphertext, key):
    decrypted_text = ""
    for char in ciphertext.upper():
        if char.isalpha():
            decrypted_text += chr((ord(char) - 65 - key + 26) % 26 + 65)
        else:
            decrypted_text += char
    return decrypted_text

""" Ved kryptering gjør man + key
ved dekryptering så er det - key

 number = ord(char) - ord("A")
shifted_number = (number + key) % 26
encrypted_char = chr(shifted_number + ord("A"))

i ASCII-tabellen er blant annet:

A = 65, a = 97
B = 66, b= 98
C = 67, c= 99

så print(ord("A"))= 65
  """


print(ord("A"))


# Example
plaintext = "MOCKMEET"
key = 3  # antall plasser frem i alfabetet A-> F
ciphertext = caesar_cipher_encrypt(plaintext, key)
print("Encrypted:", ciphertext)
print("Decrypted:", caesar_cipher_decrypt(ciphertext, key))


#pip install pycryptodome
"""AES Symmetric Key Cryptography""AES Symmetric Key Cryptography"""
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from Crypto.Random import get_random_bytes


def aes_encrypt(plaintext, key):
    cipher = AES.new(key, AES.MODE_CBC)
    ciphertext = cipher.encrypt(pad(plaintext.encode('utf-8'), AES.block_size))
    return cipher.iv + ciphertext
def aes_decrypt(ciphertext, key):
    iv = ciphertext[:16]
    cipher = AES.new(key, AES.MODE_CBC, iv)
    plaintext = unpad(cipher.decrypt(ciphertext[16:]), AES.block_size)


    return plaintext.decode('utf-8')
# Example
key = get_random_bytes(16) # 128-bit key
plaintext = "HELLO"
ciphertext = aes_encrypt(plaintext, key)
print("Encrypted:", ciphertext)
print("Decrypted:", aes_decrypt(ciphertext, key))

"""Asymmetric-key Encryption"""

"""In Asymmetric-key Encryption, we use two keys a public key and a private
key. The public key is used to encrypt the data and the private key is
used to decrypt the data. By the name, the public key can be public (can
be sent to anyone who needs to send data). No one has your private key, so
no one in the middle can read your data."""

#pip install rsa
"""Steps:
a. Import rsa library
b. Generate public and private keys with rsa.newkeys() method.
c. Encode the string to byte string.
d. Then encrypt the byte string with the public key.
e. Then the encrypted string can be decrypted with the private key.
f. The public key can only be used for encryption and the private can
only be used for decryption.
"""
#pip install rsa
import rsa
# generate public and private keys with rsa.newkeys method,this method accepts key length as its parameter
# key length should be atleast 16

publicKey, privateKey = rsa.newkeys(512)

# this is the string that we will be encrypting
message = "hello friends"



# rsa.encrypt method is used to encrypt string with public key string
#should be encoded to byte string before encryption

encMessage = rsa.encrypt(message.encode(), publicKey)

print("original string: ", message)
print("encrypted string: ", encMessage)


# the encrypted message can be decrypted with ras.decrypt method and
#private key and the decrypt method returns encoded byte string
# use decode method to convert it to string and public key cannot be used
#for decryption
decMessage = rsa.decrypt(encMessage, privateKey).decode()

print("decrypted string: ", decMessage)


# ============================================================
# TASK 5 - DATA MASKING
# Skjuler deler av sensitiv informasjon
# ============================================================

# re = Regular Expressions.
# Brukes for å finne og erstatte bestemte mønstre i tekst.
import re


class DataMasker:

    # Denne funksjonen skjuler et navn.
    # Eksempel:
    # "John" -> "J***"
    def mask_name(self, name):

        # name[0] betyr: hent første bokstav i navnet.
        # len(name) finner hvor mange tegn navnet har.
        # "*" * (len(name) - 1) lager riktig antall stjerner.
        return name[0] + "*" * (len(name) - 1)


    # Denne funksjonen skjuler deler av en e-postadresse.
    # Eksempel:
    # johndoe@example.com
    # ->
    # j******@example.com
    def mask_email(self, email):

        # re.sub() betyr:
        # finn tegn som passer regex-mønsteret
        # og erstatt dem med "*".
        #
        # Regexen sørger for at:
        # - første tegn beholdes
        # - tegn før @ blir skjult
        # - domenet etter @ beholdes
        return re.sub(r'(?<=.).(?=.*@)', '*', email)


    # Denne funksjonen skjuler et telefonnummer,
    # men beholder de siste 4 sifrene.
    #
    # Eksempel:
    # 123-456-7890
    # ->
    # ***-***-7890
    def mask_phone(self, phone):

        # \d betyr "et tall".
        #
        # Regexen finner tall som har minst
        # fire andre tall etter seg.
        #
        # Disse tallene blir erstattet med "*".
        return re.sub(r'\d(?=\D*(?:\d\D*){4})', '*', phone)



# Lager et objekt av DataMasker-klassen.
# Nå kan vi bruke funksjonene i klassen.
masker = DataMasker()


# Tester funksjonene.
print("Masked Name:", masker.mask_name("John Doe"))
print("Masked Email:", masker.mask_email("johndoe@example.com"))
print("Masked Phone:", masker.mask_phone("123-456-7890"))



# ============================================================
# TASK 6 - BASIC THREAT INTELLIGENCE
# Henter informasjon om en IP-adresse fra et API
# ============================================================

# requests brukes for å sende HTTP-requests til nettsider/API-er.
#
# Hvis du ikke har requests installert:
# skriv dette i terminalen:
#
# pip install requests

import requests


class ThreatIntelligence:

    # Denne funksjonen tar imot en IP-adresse.
    def get_ip_info(self, ip):

        # f-string brukes for å sette IP-adressen
        # direkte inn i URL-en.
        #
        # Hvis ip = "8.8.8.8"
        # blir URL-en:
        #
        # https://ipinfo.io/8.8.8.8/json
        url = f"https://ipinfo.io/{ip}/json"


        # requests.get() sender en HTTP GET-request.
        #
        # Vi spør altså API-et:
        # "Kan du gi meg informasjon om denne IP-en?"
        response = requests.get(url)


        # response.json() gjør JSON-svaret
        # om til en Python dictionary.
        #
        # Et svar kan for eksempel inneholde:
        #
        # {
        #     "ip": "8.8.8.8",
        #     "city": "...",
        #     "country": "US"
        # }
        return response.json()


    # Denne funksjonen simulerer threat intelligence.
    #
    # Den henter IKKE ekte threat data.
    # Den returnerer bare eksempeldata.
    def get_threat_data(self):

        # Dette er en Python dictionary.
        #
        # Vi later som et sikkerhetssystem
        # har oppdaget en mulig DDoS.
        return {
            "threat_level": "High",
            "description": "Possible DDoS detected"
        }



# Lager et ThreatIntelligence-objekt.
intelligence = ThreatIntelligence()


# Henter informasjon om IP-adressen 8.8.8.8.
print(
    "IP Info:",
    intelligence.get_ip_info("8.8.8.8")
)


# Printer våre simulerte threat-data.
print(
    "Threat Data:",
    intelligence.get_threat_data()
)



# ============================================================
# TASK 7 - LOGGING SYSTEM
# Logger hendelser fra programmet til en fil
# ============================================================

# logging er innebygget i Python.
# Vi trenger derfor IKKE å installere noe.
import logging


class Logger:

    # __init__ kjøres automatisk når vi lager et Logger-objekt.
    #
    # log_file er navnet på filen
    # hvor loggene skal lagres.
    def __init__(self, log_file):

        # basicConfig konfigurerer logging-systemet.
        logging.basicConfig(

            # Bestemmer hvilken fil loggene skal lagres i.
            filename=log_file,

            # DEBUG betyr at vi tar med DEBUG
            # og alle høyere alvorlighetsnivåer.
            level=logging.DEBUG,

            # Bestemmer hvordan hver logglinje skal se ut.
            #
            # %(asctime)s   = tidspunkt
            # %(levelname)s = INFO, WARNING, ERROR osv.
            # %(message)s   = selve meldingen
            format="%(asctime)s - %(levelname)s - %(message)s"
        )


    # Logger en vanlig informasjonsmelding.
    def log_info(self, message):
        logging.info(message)


    # Logger en advarsel.
    def log_warning(self, message):
        logging.warning(message)


    # Logger en feilmelding.
    def log_error(self, message):
        logging.error(message)



# Lager et Logger-objekt.
#
# Loggene blir lagret i:
# app.log
logger = Logger("app.log")


# Skriver forskjellige typer logger.
logger.log_info("This is an info message")

logger.log_warning("This is a warning message")

logger.log_error("This is an error message")


