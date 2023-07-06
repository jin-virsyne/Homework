numbers = []

"""
while i < 6:
    print(f"At the top i is {i}")
    numbers.append(i)

    i = i + 1
    print("Numbers now: ", numbers)
    print(f"At the bottom i is {i}")

print("The numbers: ")

for num in numbers:
    print(num)
"""

def start_loop(limit):
    i = 0
    while i < limit:
        numbers.append(i)
        i += 1
        print("Numbers now: ", numbers)

    j = 0
    for j in range(j, limit):
        numbers.append(j)
        print("Numbers now: ", numbers)


start_loop(5)

for num in numbers:
    print(num)