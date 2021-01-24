# Speed_Dating_Simulation
This simulation represents a neighborhood dating pool of 546 heterosexual singles. By simulating individual couple creation and breakups, it shows the percentage of the group who are single over time as you change various macro cultural factors such as likelihood of going out and likelihood of breaking up.

## Running the Simulation
Download the repo, `cd` into it, then run:
* `pipenv install`
* `pipenv shell`
* `python3 main.py`

When you run `python3 main.py`, you will first be asked: 

`Would you like to reset? (Y/N)`

If you would like to reset and start a simulation from step 1, enter `y`. Otherwise, enter `n`.

If you select `n`, you will be told where you left off. E.g.



`You remain on step 8 with 0 years elapsed.`

`Run the simulation again to continue from this spot.`

You'll then be asked how many steps you'd like to run:
 `How many steps would you like to run?`

You can enter any whole number. If you made a mistake and don't want the run the simulation, simply enter `0`. 


While the simulation is running, it will show all the couples getting together and breaking up on each step as well as summary statistics per step. E.g.

```
Step 2/3
**** New Couples ****
Perry + Kristin = <3
Granville + Ashtyn = <3

...

**** Break-ups ****
Ashlee - Benjiman :(
Caleb - Belen :(

...

taken     0.52381
single    0.47619
```

## Tweaking Variables
There are several macro/cultural variables you can tweak to affect your simulation. To make changes, go `data/globals.json `and make changes directly to the json file. Though `year` and `step` depend on how long you've let the simulation run, you can change:
* `date_frequency` (How many nights a week people go out. The default is 1, so every 52 steps everyone ages one year. If you change it to 2, everyone would age every 104 steps instead).
* `social` (How likely people are to go out on a given night. It is a float between 0 and 1, with 1 being the most social/highest chance of going out and 0 being the least social/lowest chance of going out. The default is set to `0.9`.
* `conservative` (How likely people are to break up once they enter a relationship. It is a float between 0 and 1 with 1 being the most conservative/least likely to break up and 0 being the least conservative/most likely to break up.

## Results
Every time you run the simulation, you're given the percentage of people who are single or in a relationship at each step and a bar chart showing the percentage who were single at each step in the run. When you reset your simulation, results are stored in `data/results/run_results.json` by datetime stamp. It includes the global variables set for that run and the percentage single or taken per step for that run.


## How it Works
### Data

This simulation is not a perfect representation of real-world dating. The data for the simulation came from a speed dating study. This data was used to create the agents (singles) and create the random forest models that predict whether or not two singles who meet in the simulation will mutually decide to end up together. You can see the notebook where the data was processed and the models were trained [here.](https://github.com/worldwidekatie/Speed_Dating_Simulation/blob/main/speed_dating.ipynb) You can access a CSV of the original dataframe [here.](https://github.com/worldwidekatie/Speed_Dating_Simulation/blob/main/data/speeddating.csv) 

> Author: Ray Fisman and Sheena Iyengar

> Source: [Columbia Business School](http://www.stat.columbia.edu/~gelman/arm/examples/speed.dating/) - 2004

> "This data was gathered from participants in experimental speed dating events from 2002-2004. During the events, the attendees would have a four-minute "first date" with every other participant of the opposite sex. At the end of their four minutes, participants were asked if they would like to see their date again. They were also asked to rate their date on six attributes: Attractiveness, Sincerity, Intelligence, Fun, Ambition, and Shared Interests. The dataset also includes questionnaire data gathered from participants at different points in the process. These fields include: demographics, dating habits, self-perception across key attributes, beliefs on what others find valuable in a mate, and lifestyle information."

### Behaviors
Agents have three potential "behaviors":
1. The first is `go_out` wherein singles are randomly assigned to either going out or staying home. The `social` global variable increases or decreases the likelihood agents are assigned to go out vs stay home. Those who are assigned to go out, whether they be single or taken, are then randomly assigned to a location. The number of people in the room is one of the top factors taken into consideration by the women's model when choosing whether or not to date a potential partner, so the size of the venue they end up at does have some affect on whether or not they end up dating potential partners on a given night.

2. The next behavior is `date`. If an agent is not at home, is single, and is at a venue with at least one available single of the opposite gender, they go through the `date` behavior. They are randomly assigned to match up with one agent of the opposite gender at said venue. If this agent is single, both agents use their gender's respective random forest model to decide if they want to date. If both say yes, they become a couple.

3. The last behavior is `breakup`. This applies to all agents who are not single, whether they go out or not. They are randomly assigned to either break up or not break up. The `conservative` global variable increases or decreases the likelihood of agents being assigned to stay together or break up.