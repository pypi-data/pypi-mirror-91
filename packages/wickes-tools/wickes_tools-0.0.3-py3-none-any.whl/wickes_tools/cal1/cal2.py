class cal:
    def __init__(self, num1, num2):
        self.num1 = num1
        self.num2 = num2

    def add_numbers(self):
        return self.num1 + self.num2
    @staticmethod
    def subtract_numbers(num1, num2):
        return num1 - num2
    @staticmethod
    def multiply_numbers(num1, num2):
        return num1 * num2
    @staticmethod
    def divide_numbers(num1, num2):
        return num1 / num2


def main():
    print("calculator module")


if __name__ == "__main__":
    main()