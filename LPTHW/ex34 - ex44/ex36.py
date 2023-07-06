from sys import exit

def die(msg):
    print(msg, "Too bad.")
    exit(0)

def fluff_room():
    print("\nOoh, there's plenty of cats here!")
    print("It's like a heaven for cat lovers.")
    print("What would you like to do with these cats?")
    print("(option: feed, pet head, scratch chin, bring home)")

    choice = input("> ")
    choice = choice.lower()
    if "feed" in choice:
        die("The cats eat you alive instead.")
    elif "pet" in choice or "scratch" in choice:
        die("Too many to handle! Some get impatient and bite you to death.")
    elif "home" in choice:
        print("All the cats happily followed you home! Nice!")
        print("You win!")
        exit(0)
    else:
        print("The cats attack you and you died.")

def hera_room():
    print("\nA wild Hera appears.")
    print("She seems to be looking for something.")
    print("There's a rose, Milano, boots and many more all over the floor.")
    affinity = 0
    need = 3

    while True:
        print("\nWhat would you give her?")
        choice = input("> ")
        choice = choice.lower()

        if affinity >= need:
            print("She nods and opens the door for you.")
            print("You enter the room.")
            fluff_room()
        elif choice == "rose":
            die("She gets mad at you and runs away.")
        elif choice == "boots" and affinity < need:
            print("You seems to gain her attention.")
            affinity += 1
        elif choice == "milano" and affinity < need:
            print("She munches the cookie and smiles.")
            affinity += 1
        elif "pet" in choice and affinity < need:
            print("She giggles.")
            affinity += need
        else:
            print("She shakes her head.")

def trap_room():
    print("\nThe room is dark, very dark.")
    print("Go forward or leave?")

    choice = input("> ")

    if choice == "forward":
        die("You fall into a pithole filled with spikes!")
    elif choice == "leave":
        die("A shadow sneaks behind you and kills you instead.")
    else:
        trap_room()

def start():
    print("You see two doors in front of you.")
    print("Do you choose the left or the right one?")
        
    choice = input("> ")

    if choice == "left":
        trap_room()
    elif choice == "right":
        hera_room()
    else:
        die("You hear a sudden cry and everything darkens.")

start()