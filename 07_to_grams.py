import csv

# open file
groceries = open('01_ingredients_ml_to_g.csv')

# Read data into a list
csv_groceries = csv.reader(groceries)

# Create a dictionary to hold the data
food_dictionary = {}

# Add the data from the list into the dictionary
# (first item in row is key, next is definition)

for row in csv_groceries:
    food_dictionary[row[0]] = row[1]

print(food_dictionary)

keep_going = ""
while keep_going == "":
    amount = eval(input("How much? "))
    amount = float(amount)

    # Get ingredient and change it to match dictionary.
    ingredient = input("Ingredient: ").lower()

    if ingredient in food_dictionary:
        mult_by = food_dictionary.get(ingredient)
        amount = amount * float(mult_by) / 250
        print("Amount in g {}".format(amount))
    else:
        print("{} is unchanged".format(amount))
