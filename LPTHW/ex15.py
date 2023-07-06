from sys import argv

script, filename = argv

# Open file received from argv
txt = open(filename)

print(f"Here's your file {filename}:")
print(txt.read())

# Open the file again, this time through input()
print("Type the filename again:")
file_again = input("> ")

txt_again = open(file_again)

print(txt_again.read())
# Close them back
txt.close()
txt_again.close()