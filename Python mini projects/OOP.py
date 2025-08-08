# OOP_tutorial.py

# 1. Classes and Objects
class Dog:
    # Constructor (__init__) and attributes
    def __init__(self, name, age):
        self.name = name
        self.age = age

    # Method
    def bark(self):
        print(f"{self.name} says woof!")

# Creating an object
dog1 = Dog("Buddy", 3)
dog1.bark()  # Output: Buddy says woof!

# 2. Inheritance
class Animal:
    def __init__(self, species):
        self.species = species

    def speak(self):
        print("Some generic animal sound")

# Cat inherits from Animal
class Cat(Animal):
    def __init__(self, name, age):
        super().__init__("Cat")
        self.name = name
        self.age = age

    # Method overriding (Polymorphism)
    def speak(self):
        print(f"{self.name} says Meow")

cat1 = Cat("Whiskers", 2)
cat1.speak()  # Output: Whiskers, says Meow

# 3. Encapsulation
class BankAccount:
    def __init__(self, owner, balance):
        self.owner = owner
        self.__balance = balance  # Private attribute

    def deposit(self, amount):
        self.__balance += amount

    def withdraw(self, amount):
        if amount <= self.__balance:
            self.__balance -= amount
        else:
            print("Insufficient funds")

    def get_balance(self):
        return self.__balance

account = BankAccount("Alice", 1000)
account.deposit(500)
print(account.get_balance())  # Output: 1500
account.withdraw(2000)        # Output: Insufficient funds

# 4. Polymorphism
class Bird:
    @staticmethod
    def speak():
        print("Chirp")

class Cow:
    @staticmethod
    def speak():
        print("Moo")

def animal_sound(animal):
    animal.speak()

bird = Bird()
cow = Cow()
animal_sound(bird)  # Output: Chirp
animal_sound(cow)   # Output: Moo

# 5. Class and Static Methods
class MathUtils:
    @staticmethod
    def add(a, b):
        return a + b

    @classmethod
    def description(cls):
        print(f"This is {cls.__name__} class.")

print(MathUtils.add(5, 7))  # Output: 12
MathUtils.description()     # Output: This is MathUtils class.

# 6. Properties (getter/setter)
class Person:
    def __init__(self, name):
        self._name = name

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        if not value:
            raise ValueError("Name cannot be empty")
        self._name = value

p = Person("John")
print(p.name)  # Output: John
p.name = "Jane"
print(p.name)  # Output: Jane