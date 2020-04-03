import re

# ingredient has mixed fraction followed by unit and ingredient

full_recipe =[
    "3/4 cup milk",
    "1 cup flour",
    "2 tablespoons white sugar",
    "1 3/4 cups flour",
    "1.5 tsp baking powder",
    "pinch of cinammon"
]

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

        # Get unit and ingredient...
        compile_regex = re.compile(mixed_regex)
        unit_ingredient = re.split(compile_regex, recipe_line)
        unit_ingredient = (unit_ingredient[1]).strip()  # remove extra white space from unit

    else:
        get_amount = recipe_line.split(" ", 1)  # split line at first space

        try:
            amount = eval(get_amount[0])    # convert amount to float if possible
        except NameError:
            amount = get_amount[0]
            convert = "no"

        unit_ingredient = get_amount[1]

    # Get unit and ingredient...
    get_unit = unit_ingredient.split(" ", 1)    # splits text at first space
    unit = get_unit[0]
    ingredient = get_unit[1]

    print("{} {} {}".format(amount, unit, ingredient))

