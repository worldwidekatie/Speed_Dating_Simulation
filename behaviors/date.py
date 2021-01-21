import category_encoders as ce
import joblib
import json
import numpy as np
import pandas as pd
import random

from sklearn.impute import SimpleImputer
from sklearn.pipeline import make_pipeline
from sklearn.ensemble import RandomForestClassifier


globals_ = json.load(open("data/globals.json","r"))


men = json.load(open("data/men.json","r"))
women = json.load(open("data/women.json","r"))


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
    df = df.drop(columns=["name", 'gender', 'name_o', 'gender_o', 'likelihood_o', 'status_o', 'status'])

    return df

women_ = pd.DataFrame(women).T
men_ = pd.DataFrame(men).T

def date(size=globals_['pool_size']):
    m = men_.sample(n=size).reset_index().rename(columns={'index': 'name'})
    f = women_.sample(n=size).reset_index().rename(columns={'index': 'name'})

    m_o = {}
    for i in list(m):
        m_o[i] = i + "_o"
    m_o = m.rename(columns=m_o)
    
    f_o = {}
    for i in list(f):
        f_o[i] = i + "_o"
    f_o = f.rename(columns=f_o)

    m = pd.concat([m, f_o], axis=1)
    f = pd.concat([f, m_o], axis=1)

    m['room_size'] = 14
    X_men = wrangle(m)

    f['room_size'] = 14
    X_women = wrangle(f)
    

    X_women['match'] = women_model.predict(X_women)
    X_men['match'] = men_model.predict(X_men)

    m_outcomes = {}
    f_outcomes = {}
    dates = {}
    for i in range(0, size):
        if X_men['match'][i] == 1 and X_women['match'][i] == 1:
            outcome = 'taken'
            result = 1
        else:
            outcome = 'single'
            result = 0

        dates[i] = {'man': m['name'][i],
        'woman': f['name'][i],
        'outcome': result}

        f_outcomes[f['name'][i]] = outcome
        m_outcomes[m['name'][i]] = outcome

    for i in m_outcomes:
        men[i]['status'] = m_outcomes[i]

    for i in f_outcomes:
        women[i]['status'] = f_outcomes[i]

    with open("data/new_women.json","w") as outfile:
        json.dump(women, outfile)
    
    with open("data/new_men.json","w") as outfile:
        json.dump(men, outfile)

    globals_['step'] = globals_['step'] + 1
    print(globals_['step'])

    with open("data/new_globals.json","w") as outfile:
        json.dump(globals_, outfile)
    return dates

date()

