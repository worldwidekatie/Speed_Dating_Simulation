import category_encoders as ce
import copy as copy
import joblib
import json
import numpy as np
import pandas as pd
import random

from sklearn.impute import SimpleImputer
from sklearn.pipeline import make_pipeline
from sklearn.ensemble import RandomForestClassifier


globals_ = json.load(open("data/globals.json","r"))

men_model = joblib.load('assets/men.joblib')
women_model = joblib.load('assets/women.joblib')


def wrangle(df):
    x = ['room_size',
    'age',
    'importance_same_race',
    'importance_same_religion',
    'likelihood',
    'attractive_important',
    'sincere_important',
    'intellicence_important',
    'funny_important',
    'ambtition_important',
    'attractive',
    'sincere',
    'intelligence',
    'funny',
    'ambition',
    'shared_interests_important',
    'sports',
    'tvsports',
    'exercise',
    'dining',
    'museums',
    'art',
    'hiking',
    'gaming',
    'clubbing',
    'reading',
    'tv',
    'theater',
    'movies',
    'concerts',
    'music',
    'shopping',
    'yoga',
    'expected_happy_with_sd_people',
    'age_o',
    'importance_same_race_o',
    'importance_same_religion_o',
    'attractive_important_o',
    'sincere_important_o',
    'intellicence_important_o',
    'funny_important_o',
    'ambtition_important_o',
    'attractive_o',
    'sincere_o',
    'intelligence_o',
    'funny_o',
    'ambition_o',
    'shared_interests_important_o',
    'sports_o',
    'tvsports_o',
    'exercise_o',
    'dining_o',
    'museums_o',
    'art_o',
    'hiking_o',
    'gaming_o',
    'clubbing_o',
    'reading_o',
    'tv_o',
    'theater_o',
    'movies_o',
    'concerts_o',
    'music_o',
    'shopping_o',
    'yoga_o',
    'expected_happy_with_sd_people_o']

    df[x] = df[x].replace("?", np.NaN)
    df[x] = df[x].apply(pd.to_numeric)
    df = df.drop(columns=['gender','gender_o', 'likelihood_o', 'status_o', 'status', 'location', 'location_o', 'partner', 'partner_o', 'behaviors', 'behaviors_o'])

    return df


def compat(person, partner, locations, men, women):
    people = copy.copy(women)
    for i in men:
        people[i] = men[i]

    if people[person]['status'] == 'taken':
        return 0
    elif people[partner]['status'] == 'taken':
        return 0
    else:
        # First do the person's choice
        df = pd.DataFrame(people[person])
        df2 = pd.DataFrame(people[partner])
        o = {}
        for i in list(df2):
            o[i] = i + "_o"
        df2 = df2.rename(columns=o)
        df3 = pd.concat([df, df2], axis=1)
        df3 = df3.iloc[[0]]
        df3['room_size'] = locations[people[person]['location']]["current_occupancy"]
        X = wrangle(df3)
        if people[person]['gender'] == 'female':
            person_choice = women_model.predict(X)
        else:
            person_choice = men_model.predict(X)
        
        # Then do the partner's choice
        df = pd.DataFrame(people[partner])
        df2 = pd.DataFrame(people[person])
        o = {}
        for i in list(df2):
            o[i] = i + "_o"
        df2 = df2.rename(columns=o)
        df3 = pd.concat([df, df2], axis=1)
        df3 = df3.iloc[[0]]
        df3['room_size'] = locations[people[partner]['location']]["current_occupancy"]
        X = wrangle(df3)
        if people[partner]['gender'] == 'female':
            partner_choice = women_model.predict(X)
        else:
            partner_choice = men_model.predict(X)

        if partner_choice == 1 and person_choice == 1:
            return 1

        else:
            return 0


def date(person):
    """A function for the dating behavior"""
    locations = json.load(open("data/locations.json"))
    men = json.load(open("data/men.json","r"))
    women = json.load(open("data/women.json","r"))

    if person in men:
        if men[person]['location'] == 'home':
            pass
        elif men[person]['status'] == 'taken':
            pass

        else:
            if locations[men[person]['location']]["available_women"] != 0:
                partner = random.choice(locations[men[person]['location']]["women"])              
                if compat(person, partner, locations, men, women) == 1:
                    print(f"{person} + {partner} = <3")
                    men[person]['status'] = 'taken'
                    men[person]['partner'] = partner
                    women[partner]['status'] = 'taken'
                    women[partner]['partner'] = person
                    locations[men[person]['location']]["available_women"] -= 1
                    locations[men[person]['location']]["available_men"] -= 1


                else:
                    pass
            
            else:
                pass

    elif person in women:
        if women[person]['location'] == 'home':
            pass
        elif women[person]['status'] == 'taken':
            pass

        else:
            if locations[women[person]['location']]["available_men"] != 0:
                partner = random.choice(locations[women[person]['location']]["men"])
                if compat(person, partner, locations, men, women) == 1:
                    print(f"{person} + {partner} = <3")
                    women[person]['status'] = 'taken'
                    women[person]['partner'] = partner
                    men[partner]['status'] = 'taken'
                    men[partner]['partner'] = person
                    locations[women[person]['location']]["available_women"] -= 1
                    locations[women[person]['location']]["available_men"] -= 1


                else:
                    pass
            
            
            else:
                pass
    else:
        print(f"{person} not a valid name")

    with open("data/women.json","w") as outfile:
        json.dump(women, outfile)

    with open("data/men.json","w") as outfile:
        json.dump(men, outfile)   

    with open("data/locations.json","w") as outfile:
        json.dump(locations, outfile)