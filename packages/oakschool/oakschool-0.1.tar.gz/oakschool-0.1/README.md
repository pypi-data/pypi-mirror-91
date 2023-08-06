# This is example of oop (class) in python for beginner

### วิธีติดตั้ง

เปิด CMD / Terminal

```python
pip install oakschool
```

### How to use

เปิด IDLE ขึ้นมาแล้วพิมพ์...

```python
from oakschool import Student, SpecialStudent
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
```

