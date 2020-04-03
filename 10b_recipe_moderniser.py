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

        if response == "":
            print(error)
            continue
        elif has_errors != "":
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

        except NameError:
            print(error)

        except ValueError:
            print(error)

        except SyntaxError:
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


# Function to get (and check) scale factor
def get_sf():

    serving_size = num_check("What is the recipe serving size? ")

    # Main Routine goes here
    dodgy_sf = "yes"
    while dodgy_sf == "yes":

        desired_size = num_check("How many servings are needed? ")

        scale_factor = desired_size / serving_size

        if scale_factor < 0.25:
            dodgy_sf = input("Warning: This scale factor is very small and you "
                          "might struggle to accurately weigh the ingredients.  \n"
                          "Do you want to fix this and make more servings? ").lower()
        elif scale_factor > 4:
            dodgy_sf = input("Warning: This scale factor is quite large - you might "
                          "have issues with mixing bowl volumes and oven space.  "
                          "\nDo you want to fix this and make a smaller "
                          "batch? ").lower()
        else:
            dodgy_sf = "no"

    return scale_factor


# Function to get (and check amount, unit and ingredient)
def get_all_ingredients():
    all_ingredients = []

    stop = ""
    print("Please enter ingredients one line at a time.  Press 'xxx' to when "
          "you are done.")
    print()
    while stop != "xxx":
        # Ask user for ingredient (via not blank function)
        get_recipe_line = not_blank("Recipe Line <or 'xxx' to end>: ",
                                   "This can't be blank",
                                   "yes")

        # Stop loopin if exit code is typed and there are more
        # than 2 ingredients...
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


def unit_checker(raw_unit, us):

    unit_tocheck = raw_unit

    # Abbreviation lists
    teaspoon = ["tsp", "teaspoon", "t", "teaspoons"]
    tablespoon = ["tbs", "tablespoon", "tbsp", "tablespoons"]
    dessertspoon = ["dessertspoon", "dessertspoons"]
    ounce = ["oz", "oz.", "ozs.", "ounce", "fl oz", "ounces"]
    cup = ["c", "cup", "cups"]
    pint = ["p", "pt", "fl pt", "pint", "pints"]
    quart = ["q", "qt", "fl qt", "quart", "quarts"]
    mls = ["ml", "milliliter", "millilitre", "milliliters", "millilitres"]
    litre = ["litre", "liter", "l", "litres", "liters"]
    pound = ["pound", "lb", "lb.", "lbs", "lbs.","#", "pounds"]
    grams = ["g", "gram", "grams"]

    if unit_tocheck == "":
    # print("you chose {}".format(unit_tocheck))
        return unit_tocheck
    elif unit_tocheck.lower() in grams:
        return "g"
    elif unit_tocheck == "T" or unit_tocheck.lower() in tablespoon:
        return "tbs"
    elif unit_tocheck.lower() in teaspoon:
        return "tsp"
    elif unit_tocheck.lower() in dessertspoon:
        return "dessertspoon"
    elif unit_tocheck.lower() in ounce:
        return "ounce"
    elif unit_tocheck.lower() in cup and us == "yes":
        return "us cup"
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
    else:
        return unit_tocheck


def round_nicely(to_round):

    # round amount appropriately...
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
    print("This program converts recipe ingredients to mls / grams and also allows \n"
          "users to up-size or down-size ingredients.")

    print()
    print("The program will ask for the source of the recipe - we recommend \n"
          "typing in the URL where you found the recipe or the book where \n"
          "it is from so that you can refer back to the original if necessary.")

    print()
    print("The program also asks for the number of servings.  If you are not sure,\n"
          "type '1'.  Then when it asks for servings required, you can increase\n"
          "or decrease the amount (eg 2 or 1/2) and the program will scale the\n"
          "ingredient amounts for you.")
    print()
    print("Note that you can use fractions if needed.  For example, write \n"
          "one half as 1/2 and one and three quarters as 1 3/4")
    print()
    print("Please only type in ONE ingredient per line, if a recipe says \n"
          "'butter or margarine', choose ONE ingredient, either butter \n"
          "or margarine.")
    print()
    print("Lastly, all lines should start with a number / fraction unless \n "
          "no number is give <eg: a pinch of salt>.")
    print()
    print("**********")
    print()


# ***** Main Routine ******
problem = "no"

# set up Dictionaries
unit_central = {
    "tsp": 5,
    "tbs": 15,
    "dessertspoon": 12.5,
    "cup" : 250,
    "us cup": 237,
    "ounce": 28.35,
    "pint": 473,
    "quart": 946,
    "pound": 454,
    "litre": 1000,
    "ml": 1,
    "g": 1
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
source = not_blank("Where is the recipe from? ",
                   "The recipe source can't be blank,",
                   "yes")
print()
us_amounts = yes_no_check("Are you using an American recipe? ")
print()

# Get serving sizes and scale factor
scale_factor = get_sf()
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
        unit = unit_checker(unit, us_amounts)

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

# Put updated ingredient in list

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
