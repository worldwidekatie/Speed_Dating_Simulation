import copy as copy
import json
import random

globals_ = json.load(open("data/globals.json","r"))

def breakup(person):
    """A function to make people break up"""

    men = json.load(open("data/men.json","r"))
    women = json.load(open("data/women.json","r"))
    people = copy.copy(women)
    for i in men:
        people[i] = men[i]
    if people[person]['status'] == 'single':
        pass

    else:
        chance = round(globals_['social'] * 10)
        chances = [0]*10 + [0]*chance
        for i in range(10-chance):
            chances.append(1)

        if random.choice(chances) == 1:
            if person in men:
                men[person]['status'] = 'single'
                partner = copy.copy(men[person]['partner'])
                men[person]['partner'] = None
                women[partner]['status'] = 'single'
                women[partner]['partner'] = None
                print(f"{person} - {partner} :(")

            elif person in women:
                women[person]['status'] = 'single'
                partner = copy.copy(women[person]['partner'])
                women[person]['partner'] = None
                men[partner]['status'] = 'single'
                men[partner]['partner'] = None
                print(f"{person} - {partner} :(")

            else:
                print(f"{person} not a valid name")
        
        
        with open("data/women.json","w") as outfile:
            json.dump(women, outfile)

        with open("data/men.json","w") as outfile:
            json.dump(men, outfile)   