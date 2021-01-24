import json
from pprint import pprint
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime


def results():
    men = json.load(open("data/men.json"))
    women = json.load(open("data/women.json"))

    men = pd.DataFrame(men).T
    women = pd.DataFrame(women).T
    all = pd.concat([men, women])
    print(all['status'].value_counts(normalize=True))


def save_stats():
    globals_ = json.load(open("data/globals.json"))
    men = json.load(open("data/men.json"))
    women = json.load(open("data/women.json"))
    results_ = json.load(open("data/results/results.json"))

    men = pd.DataFrame(men).T
    women = pd.DataFrame(women).T
    all = pd.concat([men, women])
    df = pd.DataFrame(all['status'].value_counts(normalize=True)).reset_index()

    results_[globals_['step']] = {df['index'][0]: df['status'][0], df['index'][1]: df['status'][1]}
    
    with open("data/results/results.json","w") as outfile:
        json.dump(results_, outfile)   



def make_graph():
    results_ = json.load(open("data/results/results.json"))
    df = pd.DataFrame(results_).T.reset_index().rename(columns={'index': "step"})
    print(df)
    plt.style.use('ggplot')

    x =  list(df['step'])
    y = list(df['single'])

    x_pos = [i for i, _ in enumerate(x)]

    plt.bar(x_pos, y, color='green')
    plt.xlabel("Step #")
    plt.ylabel("% Single")
    plt.title("Percentage of Singles Over Time")

    plt.xticks(x_pos, x)


    plt.show()