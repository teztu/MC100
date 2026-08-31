import uuid
import random
import string

#hiding

class Employee:
    #comment
    __length= 10
    __characters = string.ascii_letters + string.digits
    __password = ""
    __uuid = ""

    def __init__(self, name):
        self.name=name
        self.__uuid=str(uuid.uuid4())
        self.__password= ''.join(random.choice(characters) for _ in range(length))

    def vis_credentials(self):
        print(self.__uuid, self.__password)

    def vis_employee(self):
        print(self.name)
    def validate(self, uuid,password):
        if(self.__uuid== uuid and self.__password==password):
            print("valid information")
        else:
            print("invalid information")





employee1=Employee("Nicolas")


