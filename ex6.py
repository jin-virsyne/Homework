# Assign int variable and then assign the int into a string variable
types_of_people = 10
x = f"There are {types_of_people} types of people."

# Assign str variable and then assign the str into another string variable
binary = "binary"
do_not = "don't"
y = f"Those who knows {binary} and those who {do_not}."

# Print x and y
print (x)
print (y)

# Printing it.. again, fancily
print(f"I said: {x}")
print(f"I aldo said: '{y}'")

# Assign boolean variable
hilarious = False
# Create a string format which accept parameters 
joke_evaluation = "Isn't that joke so funny?! {}"
# Print the string format
print(joke_evaluation.format(hilarious))

# Creating more strings
w = "This is the left side of..."
e = "a string with a right side."

# Combine both strings together and print
print(w + e)