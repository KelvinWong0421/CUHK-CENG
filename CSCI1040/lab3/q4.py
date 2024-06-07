from abc import abstractmethod


class Employee :
    def __init__(self, id, name):
        self.id = id
        self.name = name

    @abstractmethod
    def earnings(self):
        pass

class SalaryEmployee(Employee):
    def __init__(self, id, name, salary):
        super().__init__(id, name)
        self.salary = salary

    #Overriding
    def earnings(self):
        self.wage = self.salary
        return self.wage





class HourlyEmployee(Employee):
    def __init__(self, id, name, hourly_rate, hours_worked):
        super().__init__(id, name)
        self.hourly_rate = float(hourly_rate)
        self.hours_worked = int(hours_worked)
    
    #Overriding
    def earnings(self):
        self.wage = self.hourly_rate*self.hours_worked
        return self.wage

class CommissionEmployee(SalaryEmployee):
    def __init__(self, id, name, salary, commission_rate, gross_sales):
        super().__init__(id, name, salary)
        self.commission_rate = float(commission_rate)
        self.gross_sales = int(gross_sales) 

    #Overriding
    def earnings(self):
        self.wage = self.salary+(self.commission_rate*self.gross_sales)
        return self.wage
    


john = SalaryEmployee(id=1, name='John Smith', salary=1500)
jane = HourlyEmployee(id=2, name='Jane Doe', hourly_rate=40, hours_worked=15)
kevin = CommissionEmployee(id=3, name='Kevin Bacon', salary=1000,
 commission_rate=0.05, gross_sales=2000)

print(john.earnings())
print(jane.earnings())
print(kevin.earnings())

