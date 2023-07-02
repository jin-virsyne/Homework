cars = 100
space_in_a_car = 4.0
drivers = 30
passengers = 90

#Fancy comment which the Study Drills made me wrote
cars_not_driven = cars - drivers
cars_driven = drivers
carpool_capacity = cars_driven * space_in_a_car
average_passengers_per_car = passengers / cars_driven

print("There are", cars, "cars available.")
print("There are only", drivers, "drivers available.")
print("There will be", cars_not_driven, "empty cars today.")
print("We can transport", carpool_capacity, "people today.")
print("We have", passengers, "to carpool today.")
print("We need to put about", average_passengers_per_car, "in each car.")

"""
Study Drills

Explain Error in your own words: It means the variable "car_pool_capacity" is not created yet

1. If it's just 4, then carpool_capacity will remain as an integer rather than floating point. 
No, it's not necessary unless you want to explicitly state this variable is a floating point.
"""