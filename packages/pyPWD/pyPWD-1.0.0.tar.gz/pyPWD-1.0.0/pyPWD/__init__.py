import random
import string


def help():
    print("Passwords are generated in this format: (LETTERS) (SYMBOL) (NUMBERS)\n")
    print('usage: ')
    print('pyPWD.generate(letter_length, special_character, number_length)\n')
    print('example: ')
    print("""import PyPWD
    
password = pyPWD.generate(12, '@', 12)
print(password)""")


def generate(letter_length, special_character, number_length):
    numbers = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0']
    letters = string.ascii_letters
    result_str = ''.join(random.choice(letters) for i in range(letter_length))
    nums = ''.join(random.choice(numbers) for i in range(number_length))
    pwd = result_str + random.choice(special_character) + nums
    return pwd
