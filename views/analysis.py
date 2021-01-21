import category_encoders as ce

from joblib import load
import json
import random

from sklearn.impute import SimpleImputer
from sklearn.pipeline import make_pipeline
from sklearn.ensemble import RandomForestClassifier

# w_model = joblib.load('assets/women.joblib')


men = open('data/men.json', 'r')
men = json.load(men)
men.close()
print(men)

# with open('data/women.json') as f:
#   women = json.load(f)
#   print(women)


