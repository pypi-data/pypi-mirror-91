class Greetings:
    def __init__(self, name = None):
        """
        Initialises a greetings object with the name of the person
        """
        if name:
            self.name = name
        else:
           self.name = input("Hello, please enter your name: ")
        

    
    # @staticmethod
    def hello(self):
        print(f"Hello {self.name}!")

    # @staticmethod
    def goodbye(self):
        print(f"See you {self.name}!")

    def reverse_name(self):
        self.name = self.name.lower()[::-1].capitalize()


if __name__ == "__main__":
    # a = Greetings()
    # a.hello()
    a = Greetings()
    a.hello()
    a.reverse_name()
    a.hello()
    print(a.name)

    Greetings("Karl").hello()