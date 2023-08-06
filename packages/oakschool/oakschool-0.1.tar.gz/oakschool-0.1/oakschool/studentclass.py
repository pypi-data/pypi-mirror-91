class Student:
    def __init__(self, name):
        self.name = name
        # student1.name
        # self = student1
        self.exp = 0
        self.lesson = 0
        # Call function
        # self.AddExp(10)

    def Hello(self):
        print('Sawasdee my name is {}'.format(self.name))
    
    def Coding(self):
        print('{}:Still coding...'.format(self.name))
        self.exp += 5
        self.lesson += 1
    
    def ShowExp(self):
        print('- {} has {} exp\n- learning {} times'.format(self.name,self.exp,self.lesson))

    def AddExp(self, score):
        self.exp += score
        self.lesson += 1


class SpecialStudent(Student):
    def __init__(self,name,father):
        super().__init__(name) # This line mean like Student(name)
        self.father = father
        mafia = ['Bill Gates','Thomas Edison']
        if father in mafia:
            self.exp += 100

    def AddExp(self, score):
        self.exp += (score * 3)
        self.lesson += 1

    def NeedExp(self,score=10):
        print('Teacher!! I need {} special score '.format(score))
        self.AddExp(score)




if __name__ == '__main__':
    print('-----------------Day 1-------------------')
    student0 = SpecialStudent('Mark','Bill Gates')
    student0.NeedExp()
    student0.ShowExp()

    student1 = Student('Albert')  # st is object // this line is using class
    print(student1.name)
    student1.Hello()


    print('-----------------------------------------')

    student2 = Student('Steve')

    print(student2.name)
    student2.Hello()

    print('-----------------Day 2--------------------')
    print('Who wanna coding? (get 10 exp)')
    print(student1.name)
    student1.AddExp(10)


    print('-----------------Day 3--------------------')
    print('Each your exp is :')
    print(student1.name, student1.exp)
    print(student2.name, student2.exp)

    print('-----------------Day 4--------------------')
    for i in range(5):
        student2.Coding()

    student1.ShowExp()
    student2.ShowExp()