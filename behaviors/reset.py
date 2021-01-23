import json

def resets():
    var = input("Would you like to reset? (Y/N) ")
    if var.upper() == 'Y':
        globals_orig = json.load(open("data/globals_orig.json","r"))
        men_orig = json.load(open("data/men_orig.json","r"))
        women_orig = json.load(open("data/women_orig.json","r"))
        locations_orig = json.load(open("data/locations_orig.json"))

        with open("data/women.json","w") as outfile:
            json.dump(women_orig, outfile)
        
        with open("data/men.json","w") as outfile:
            json.dump(men_orig, outfile)

        with open("data/globals.json","w") as outfile:
            json.dump(globals_orig, outfile)

        with open("data/locations.json","w") as outfile:
            json.dump(locations_orig, outfile)

    elif var.upper() == 'N':
        globals_ = json.load(open("data/globals.json","r"))
        print(f"You remain on step {globals_['step']} with {globals_['year']} years elapsed.")
        print("Run the simulation again to continue from this spot.")

    else:
        print("Please choose Y or N. ")
        resets()