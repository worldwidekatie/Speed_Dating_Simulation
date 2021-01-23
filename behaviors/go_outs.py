import json
import numpy as np
import pandas as pd
import random

def go_out(person):
    """A behavior function to make people go out."""
    globals_ = json.load(open("data/globals.json","r"))

    locations = json.load(open("data/locations.json"))
    men = json.load(open("data/men.json","r"))
    women = json.load(open("data/women.json","r"))

    chance = round(globals_['social'] * 10)
    chances = [1] * chance
    for i in range(10-chance):
        chances.append(0)

    if random.choice(chances) == 1:
        venues = []
        for i in locations:
            if locations[i]['full'] != True:
                venues.append(i)
        venue = random.choice(venues)

        locations[venue]['current_occupancy'] += 1
        if locations[venue]['current_occupancy'] >= locations[venue]["capacity"]:
            locations[venue]["full"] = True
        

        if person in men:
            men[person]["location"] = venue
            if men[person]["status"] == "single":
                locations[venue]['available_men'] += 1
                locations[venue]['men'].append(person)
            with open("data/men.json","w") as outfile:
                json.dump(men, outfile)

        elif person in women:
            women[person]["location"] = venue
            if women[person]["status"] == "single":
                locations[venue]['available_women'] += 1
                locations[venue]['women'].append(person)
            
            with open("data/women.json","w") as outfile:
                json.dump(women, outfile)

        else:
            print(f"{person} is not a valid name.")


        with open("data/locations.json","w") as outfile:
            json.dump(locations, outfile)


    else:
        pass


# if __name__ == "__main__":
#     go_out("Vincent")
#     go_out("Shaniya")
#     go_out("name")