import random
import string
length=10
from jinja2.compiler import generate
""" Lowercase/Uppercase randomize strings """

low_generated_string="".join(random.choice(string.ascii_uppercase)for _ in range(length))
print("Unik upper case string :", low_generated_string)

""" Alphanumeric randomize strings """
characters= string.ascii_letters + string.digits #antall mulige bokstaver og tall
medium_generated_string= "".join(random.choice(characters) for _ in range(length)) #bruker join og looper gjennom characters

print("Generert_string:", medium_generated_string)

""" Strings with specific characters/symbols """
str_characters = "!@#$%^&*" + string.ascii_lowercase + string.digits
strong_generated_string = ''.join(random.choice(str_characters) for _ in range(length))
print("Specific character/symbol string", strong_generated_string)


import uuid
# Random id using uuid1()
print ("Id using uuid1(): ", uuid.uuid1())
# Random id using uuid3()
print ("Id using uuid3(): ", uuid.uuid3(uuid.NAMESPACE_DNS,
'lambdatest.com'))
# Random id using uuid4()
print ("Id using uuid4(): ", uuid.uuid4())
# Random id using uuid5()
print ("Id using uuid5(): ", uuid.uuid5(uuid.NAMESPACE_DNS,
'lambdatest.com'))


"""Generating passwords"""

import random
import string
import secrets
def password_generator(length, strength):
    lower_pw = string.ascii_lowercase + string.digits

    medium_pw = string.ascii_letters + string.digits

    strong_pw = string.ascii_letters + string.digits + "!@#$%^&*()"
    password = ""
    if strength==1:
        password = ''.join(random.choices(lower_pw ,k= pw_length))
        return password
    elif strength == 2:
        password = ''.join(secrets.choice(medium_pw) for _ in range(length))
        return password

    elif strength == 3:
        password = ''.join(secrets.choice(strong_pw) for _ in range(length))
        return password
    else:
        password="Invalid strength, choose between 1-3"
        return password


pw_length= int(input("Enter length of password"))

print("Choose strength of your password \n, 1 is weak, 2 is medium, 3 is strong")
strength = int(input("Enter the required strength: "))
print("Your generator password is: ",
password_generator(length=pw_length,strength=strength))







