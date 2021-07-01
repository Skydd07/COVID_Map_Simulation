# -------------------------------------------------------
# Authors:  Sanyam Kadd, Ekamjot Singh
# --------------------------------------------------------

print("WELCOME TO THE COVID PATH FINDING PROGRAM!")

inp = input(str("Where do you want to go?\nEnter 1 if you want to go to Quarantine Place."
                "\nEnter 2 if you want to go to Vaccine Spot.\n>> "))
if inp == str(1):
    exec(open('roleC.py').read())
elif inp == str(2):
    exec(open('roleV.py').read())
else:
    inp = input(str("You did not enter a valid input. Please try again.\n>> "))
    if inp == "1":
        exec(open('roleC.py').read())
    elif inp == "2":
        exec(open('roleV.py').read())
    else:
        print("Since, you did not enter a valid input again, the program has been terminated. Thank You!")
