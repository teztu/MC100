import uuid
import random
import string


# hiding
class Employee:
    # comment
    __length = 10
    __characters = string.ascii_letters + string.digits
    __password = ""
    __uuid = ""

    def __init__(self, name):
        self.name = name
        self.__uuid = str(uuid.uuid4())
        self.__password = ''.join(
            random.choice(self.__characters) for _ in range(self.__length)
        )

    def vis_credentials(self):
        print(self.__uuid, self.__password)

    def vis_employee(self):
        print(self.name)

    def validate(self, uuid_value, password):
        if self.__uuid == uuid_value and self.__password == password:
            print("valid information")
        else:
            print("invalid information")


employee1 = Employee("Nicolas")
employee1.vis_employee()
employee1.vis_credentials()
employee1.validate("feil-uuid", "feil-passord")
