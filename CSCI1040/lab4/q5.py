class TestPaper:
    def __init__(self, subject: str, solution, pass_mark: float ):
        self.subject = subject
        self.solution = solution
        self.pass_mark = pass_mark

class Student:
    def __init__(self, id: int):
        self.id = id
        self.tests_taken = {}
    
    def take_test(self, paper:object, attempts:list[str]):
        self.paper = paper
        self.counter = 0
        for i in range(len(self.paper.solution)):
            if self.paper.solution[i] == attempts[i]:
                self.counter += 1

        self.mark = float(self.counter / len(self.paper.solution))

        self.p = False
        if (self.mark*100) >= self.paper.pass_mark:
            self.p = True

        self.tests_taken[self.paper.subject] = (self.mark, self.p)

    
    def __str__(self):
        if len(self.tests_taken) == 0:
            return str(self.id)+": "+ "[ No test records ]"
        else:
            estr = str(self.id)+ ": [ "
            c = 0
            for i in self.tests_taken.keys():
                ls = self.tests_taken[i]

                
                if ls[1]:
                    p="Passed"
                else:
                    p="Failed"

                estr = estr +i +": "+ str(round(ls[0]*100,1))+"% ("+p+")"

                if c == len(self.tests_taken)-1:
                    estr += " ]"
                else:
                    estr += ", "
                
                c = c+1   

            return estr



math = TestPaper("Math", ["1A", "2C", "3D", "4A", "5A"], 60)
chem = TestPaper("Chemistry", ["1C", "2C", "3D", "4A"], 50)
comp = TestPaper("Computing", ["1D", "2C", "3C", "4B", "5D", "6C", "7A"], 40)

alice = Student(11551234)
bob = Student(11556789)

print(alice)
alice.take_test(math, ["1A", "2D", "3D", "4A", "5A"])
print(alice) 

bob.take_test(chem, ["1C", "2D", "3A", "4C"])
bob.take_test(comp, ["1A", "2C", "3A", "4C", "5D", "6C", "7B"])
print(bob)
        