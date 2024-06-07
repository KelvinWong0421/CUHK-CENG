from msilib.schema import Class


class Employee:
    def __init__(self, first_name, last_name, domain='company.com'):
        self.first_name = first_name
        self.last_name = last_name
        self.full_name = " ".join([first_name,last_name])
        self.email = ".".join([first_name.lower(),last_name.lower()]).replace(' ','-')+"@"+domain
    def __str__(self):
        return self.full_name+", "+self.email
     


emp1 = Employee("Leia", "Organa")
emp2 = Employee("Obi-Wan", "Kenobi")
emp3 = Employee("Anakin", "Skywalker")
emp4 = Employee("Tai Man", "Chan", "cuhk.edu.hk")

print(emp1.first_name)
print(emp1.full_name)
print(emp2.email)
print(emp3)
print(emp4)

