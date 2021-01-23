# import category_encoders as ce
# import joblib
import json
# import numpy as np
# import pandas as pd
import random

# from sklearn.impute import SimpleImputer
# from sklearn.pipeline import make_pipeline
# from sklearn.ensemble import RandomForestClassifier

from behaviors.reset import resets
from behaviors.go_outs import go_out
from behaviors.dates import date
# from behaviors.breakups import breakup



def simulate():
    resets()
    steps = input("How many steps would you like to run? ")
    
    for i in range(1, int(steps)+1):
        print(f"Step {i}/{int(steps)}")
        locations_orig = json.load(open("data/locations_orig.json"))
        with open("data/locations.json","w") as outfile:
            json.dump(locations_orig, outfile)
        globals_ = json.load(open("data/globals.json","r"))
        men = json.load(open("data/men.json","r"))
        women = json.load(open("data/women.json","r"))

        for i in women:
            women[i]['location'] = 'home'

        for i in men:
            men[i]['location'] = 'home'

        with open("data/women.json","w") as outfile:
            json.dump(women, outfile)

        with open("data/men.json","w") as outfile:
            json.dump(men, outfile)   

        men = json.load(open("data/men.json","r"))
        women = json.load(open("data/women.json","r"))
        
        people = list(men.keys()) + list(women.keys())
        random.shuffle(people)

        for i in people:
            go_out(i)
    
        for i in people:
            date(i)

        globals_['step'] += 1
        if (globals_['step']/globals_['date_frequency']) % 52 == 0:
            globals_['year'] += 1
            for i in men:
                men[i]['age'] += 1
            for i in women:
                women[i]['age'] += 1

        with open("data/globals.json","w") as outfile:
            json.dump(globals_, outfile)
        



if __name__ == "__main__":
   simulate()