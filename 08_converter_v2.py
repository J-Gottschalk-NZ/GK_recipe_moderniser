# Conversion Function...

import csv

# ***** Functions go here ******
def general_converter(how_much, lookup, dictionary, conversion_factor):

    if lookup in dictionary:
        mult_by = dictionary.get(lookup)
        how_much = how_much * float(mult_by) / conversion_factor
        converted = "yes"

    else:
        converted = "no"

    return [how_much, converted]

def unit_checker():

    unit_tocheck = input("Unit? ")

    # Abbreviation lists
    teaspoon = ["tsp", "teaspoon", "t" "teaspoons"]
    tablespoon = ["tbs", "tablespoon", "T", "tbsp" "tablespoons"]
    ounce = ["oz", "ounce", "fl oz", "ounces"]
    cup = ["c", "cup", "cups"]
    pint = ["p", "pt", "fl pt", "pint", "pints"]
    quart = ["q", "qt", "fl qt", "quart", "quarts"]
    mls = ["ml", "milliliter", "millilitre", "milliliters", "millilitres"]
    litre = ["litre", "liter", "l", "litres", "liters"]
    pound = ["pound", "lb", "#", "pounds"]

    if unit_tocheck == "":
    # print("you chose {}".format(unit_tocheck))
        return unit_tocheck
    elif unit_tocheck == "T" or unit_tocheck.lower() in tablespoon:
        return "tbs"
    elif unit_tocheck.lower() in teaspoon:
        return "tsp"
    elif unit_tocheck.lower() in ounce:
        return "ounce"
    elif unit_tocheck.lower() in cup:
        return "cup"
    elif unit_tocheck.lower() in pint:
        return "pint"
    elif unit_tocheck.lower() in quart:
        return "quart"
    elif unit_tocheck.lower() in mls:
        return "ml"
    elif unit_tocheck.lower() in litre:
        return "litre"
    elif unit_tocheck.lower() in pound:
        return "pound"


# ****** Main Routine Goes here *******

# dictionaries go here
unit_central = {
    "tsp": 5,
    "tbs": 15,
    "cup" : 237,
    "ounce": 28.35,
    "pint": 473,
    "quart": 946,
    "pound": 454,
    "litre": 1000,
    "ml": 1
}

# *** Generate food dictionary *****
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

# **** Get items etc *****

keep_going = ""
while keep_going == "":
    amount = eval(input("How much? "))
    amount = float(amount)

    # Get unit and change it to match dictionary.
    unit = unit_checker()
    ingredient = input("Ingredient: ")

    # Convert to mls if possible
    amount = general_converter(amount, unit, unit_central, 1)
    print(amount)

    # If we converted to mls, try and convert to grams
    if amount[1] == "yes":
        amount_2 = general_converter(amount[0], ingredient, food_dictionary, 250)

        # if the ingredient is in the list, convert it
        if amount_2[1] == "yes":
            print(amount_2)     # Rather than printing, update modernised list (g)

        # if the ingredient is not in the list, leave the unit as ml
        else: print("unchanged") # Rather than printing, update modernised list (ml)

    # If the unit is not mls, leave the line unchanged
    else:
        print("unchanged")  # Update list with scaled amount and original unit

    # keep_going = input("<enter> or q ")

