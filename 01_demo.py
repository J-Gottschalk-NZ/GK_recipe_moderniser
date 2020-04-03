def smallest_number(numbers):
    smallest = numbers[0]
    for num in numbers:
        print(num)
        if num < smallest:
            smallest = num
            print("Smallest", smallest)

    return smallest

print(smallest_number([4, 5, 8, 3, 2, 1]))
