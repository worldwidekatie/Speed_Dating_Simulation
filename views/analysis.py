import json
from pprint import pprint
import pandas as pd

locations = json.load(open("data/locations.json"))
men = json.load(open("data/men.json"))
women = json.load(open("data/women.json"))

men = pd.DataFrame(men).T
women = pd.DataFrame(women).T

print(men['location'].value_counts())
print(women['location'].value_counts())

print(men['status'].value_counts())
print(women['status'].value_counts())

# print(men)

# print(women)