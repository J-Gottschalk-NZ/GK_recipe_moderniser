# Get user's name
name = input("What is your name? ")

# Get users's favourite Number
num_1 = int(input("What is your favourite number? "))

# Work out double, half and the square of their favourite number...
double = num_1 * 2
half = num_1 / 2
squared = num_1 * num_1

# Greet user and output info...
print()
print("Hello {}".format(name))

print("Your favourite integer is {}".format(num_1))
print("Half of {} is {}".format(num_1, half))
print("If you double {} you get {}".format(num_1, double))
print("{} squared is {}".format(num_1, squared))

