# modules to be used...
import csv
import re

# ***** Functions ******

def not_blank(question, error_msg, num_ok):
    error = error_msg

    valid = False
    while not valid:
        response = input(question)
        has_errors = ""

        if num_ok != "yes":
            # look at each character in string and if it's a number, complain
            for letter in response:
                if letter.isdigit() == True:
                    has_errors = "yes"
                    break

        if response == "" or has_errors != "":
            print(error)
            continue
        else:
            return response


# Number checking function (number must be a float that is more than 0)
def num_check(question):

    error = "Please enter a number that is more than zero"

    valid = False
    while not valid:
        response = input(question)

        if response == "":
            print(error)
            continue

        try:
            response = eval(response)
            response = float(response)

            if response <= 0:
                print(error)
            else:
                return response

        # except statement catches all errors - it's short but is bad practice as it's not all that specific
        except:
            print(error)

def yes_no_check(question):
    error = "Please enter 'yes' or 'no'"

    valid = False
    while not valid:
        response = input(question).lower()

        if response == "y" or response == "yes":
            return ("yes")
        elif response == "n" or response == "no":
            return ("no")
        else:
            print(error)


# Function to get (and check amount, unit and ingredient)
def get_all_ingredients():
    all_ingredients = []

    stop = ""
    print("Please enter ingredients one line at a time.  Press 'xxx' to when "
          "you are done.")
    print()
    while stop != "xxx":
        # Ask user for ingredient (via not blank function)
        get_recipe_line = not_blank("Recipe Line <or 'xxx' to end>: ", "This can't be blank", "yes")

        # Stop looping if exit code is typed & ingredients > 2
        if get_recipe_line.lower() == "xxx" and len(all_ingredients) > 1:
            break

        elif get_recipe_line.lower() == "xxx" and len(all_ingredients) <2:
            print("You need at least two ingredients in the list.  "
                  "Please add more ingredients.")

        # If exit code is not entered, add ingredient to list
        else:
            all_ingredients.append(get_recipe_line)

    return all_ingredients


def general_converter(how_much, lookup, dictionary, conversion_factor):

    if lookup in dictionary:
        mult_by = dictionary.get(lookup)
        how_much = how_much * float(mult_by) / conversion_factor
        converted = "yes"

    else:
        converted = "no"

    return [how_much, converted]


def unit_checker(raw_unit):

    unit_tocheck = raw_unit

    # Abbreviation lists (checks for selected units, could be expanded)
    teaspoon = ["tsp", "teaspoon", "t", "teaspoons"]
    tablespoon = ["tbs", "tablespoon", "tbsp", "tablespoons"]
    cup = ["c", "cup", "cups"]
    mls = ["ml", "milliliter", "millilitre", "milliliters", "millilitres"]
    grams = ["g", "gram", "grams"]

    if unit_tocheck == "":
        return unit_tocheck
    elif unit_tocheck.lower() in grams:
        return "g"
    elif unit_tocheck == "T" or unit_tocheck.lower() in tablespoon:
        return "tbs"
    elif unit_tocheck.lower() in teaspoon:
        return "tsp"
    elif unit_tocheck.lower() in cup:
        return "cup"
    elif unit_tocheck.lower() in mls:
        return "ml"
    else:
        return unit_tocheck


def round_nicely(to_round): # round amount appropriately...
    if to_round % 1 == 0:
        to_round = int(to_round)
    elif to_round * 10 % 1 == 0:
        to_round = "{:.1f}".format(to_round)
    else:
        to_round = "{:.2f}".format(to_round)

    return to_round

def instructions():
    print()
    print("******** Instructions ********")
    print()
    print("This is where the instructions would normally go.  Please add to this or see version 11 for what this"
          "might look like")
    print()
    print("**********")
    print()

# ***** Main Routine ******
problem = "no"

# set up Dictionaries
unit_central = {
    "tsp": 5,
    "tbs": 15,
    "cup" : 250,
    "ml": 1,
    "g": 1
}

# *** Generate food dictionary *****
# open file, read data into list and create dictionary
groceries = open('01_ingredients_ml_to_g.csv')
csv_groceries = csv.reader(groceries)
food_dictionary = {}

# Add the data from the list into the dictionary
for row in csv_groceries:
    food_dictionary[row[0]] = row[1]

# set up lists to hold original and 'modernised' recipes
modernised_recipe = []

# ***** Welcome / Instructions ********
print("******** Welcome to the Great Recipe Moderniser ********")
print()

get_instructions = yes_no_check("Welcome.  Is it your first time using this "
                                "program? ")

if get_instructions.lower() == "yes":
    instructions()
else:
    print()

# ******* Get User Input ***********

# Ask user for recipe name and check its not blank
recipe_name = not_blank("What is the recipe name? ",
                   "The recipe name can't be blank and can't contain numbers,",
                   "no")
# Ask user where the recipe is originally from (numbers OK)
source = not_blank("Where is the recipe from? ", "The recipe source can't be blank,", "yes")
print()

# Get serving sizes and scale factor.  Does not check that serving size is too big / small
serving_size = num_check("What is the recipe serving size? ")
desired_size = num_check("How many servings are needed? ")
scale_factor = desired_size / serving_size
print()

# Get amounts, units and ingredients from user...
full_recipe = get_all_ingredients()

# Split each line of the recipe into amount, unit and ingredient...
mixed_regex = "\d{1,3}\s\d{1,3}\/\d{1,3}"

for recipe_line in full_recipe:
    recipe_line = recipe_line.strip()

    # Get amount...
    if re.match(mixed_regex, recipe_line):

        # Get mixed number by matching the regex
        pre_mixed_num = re.match(mixed_regex, recipe_line)
        mixed_num = pre_mixed_num.group()

        # Replace space with a + sign...
        amount = mixed_num.replace(" ", "+")
        # Change the string into a decimal
        amount = eval(amount)
        amount = amount * scale_factor

        # Get unit and ingredient...
        compile_regex = re.compile(mixed_regex)
        unit_ingredient = re.split(compile_regex, recipe_line)
        unit_ingredient = (unit_ingredient[1]).strip()  # remove extra white space from unit

    else:
        get_amount = recipe_line.split(" ", 1)  # split line at first space

        try:
            # Item has valid amount that is not a mixed fraction
            amount = eval(get_amount[0])    # convert amount to float if possible
            amount = amount * scale_factor

        except NameError:
            # "Pinch of Salt" case (ie: item does not contain concrete amount)
            amount = get_amount[0]
            modernised_recipe.append(recipe_line)
            continue

        except SyntaxError:
            problem = "yes"
            modernised_recipe.append(recipe_line)
            continue

        unit_ingredient = get_amount[1]

    # Get unit and ingredient...
    get_unit = unit_ingredient.split(" ", 1)    # splits text at first space

    num_spaces = recipe_line.count(" ")
    if num_spaces > 1:
        # Item has unit and ingredient
        unit = get_unit[0]
        ingredient = get_unit[1]
        unit = unit_checker(unit)

        # if unit is already in grams, add it to list
        if unit == "g":
            modernised_recipe.append("{:.0f} g {}".format(amount, ingredient))
            continue

        # convert to mls if possible...
        amount = general_converter(amount, unit, unit_central, 1)

        # If we converted to mls, try and convert to grams
        if amount[1] == "yes":
            amount_2 = general_converter(amount[0], ingredient, food_dictionary, 250)

            # if the ingredient is in the list, convert it
            if amount_2[1] == "yes":
                modernised_recipe.append("{:.0f} g {}".format(amount_2[0], ingredient))     # Rather than printing, update modernised list (g)

            # if the ingredient is not in the list, leave the unit as ml
            else:
                modernised_recipe.append("{:.0f} ml {}".format(amount[0], ingredient))
                continue

        # If the unit is not mls, leave the line unchanged
        else:
            # round amount appropriately...
            rounded_amount = round_nicely(amount[0])
            modernised_recipe.append("{} {} {}".format(rounded_amount, unit, ingredient))  # Update list with scaled amount and original unit

    else:
        # Item only has ingredient (no unit)
        rounded_amount = round_nicely(amount)
        modernised_recipe.append("{} {}".format(rounded_amount, unit_ingredient))

# Output ingredient list
print()
print("******** {} Recipe ******".format(recipe_name))
print("Source: {}".format(source))
print()

if problem == "yes":
    print("***** Warning ******")
    print("Some of the entries below might be incorrect as \n"
          "there were problems procesesing some of your inputs.\n"
          "It's possible that you typed a fraction incompletely")
    print()

print("****Ingredients (scaled by a factor of {}) ****".format(scale_factor))
print()
for item in modernised_recipe:
    print(item)
