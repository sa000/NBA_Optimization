import csv
import os
import pandas as pd
##Grab data
import numpy as np
from teams import teams_dict
def add_fatigue(schedule):
	teams=schedule.HOME.unique()

	schedule.loc[0:2,'HomeRest']=0
	schedule.loc[0:2,'AwayRest']=0
	dates=schedule.DATE.unique()[1:]
	yesterday_indices=[0,1,2]
	for date in dates:
		#Grab games for the date
		games=schedule[schedule.DATE==date]
		#For each game, identify rest for home and visitor team
		for index, game in games.iterrows():
			if game.HOME in schedule.iloc[yesterday_indices].VISITOR or game.VISITOR in schedule.iloc[yesterday_indices].HOME:
				schedule.loc[index, 'HomeRest']=0
			else:
				schedule.loc[index, 'HomeRest']=1
			if game.VISITOR in schedule.iloc[yesterday_indices].VISITOR or game.VISITOR in schedule.iloc[yesterday_indices].HOME:
				schedule.loc[index, 'AwayRest']=0
			else:
				schedule.loc[index, 'AwayRest']=1
		yesterday_indices=games.index
		print date
	return schedule



def addb2b():
	pass
def create_stats():
	files=os.listdir('../Projections/past')[1:]
	df=pd.DataFrame()
	for file in files:
		print file
		p=pd.read_csv('../Projections/past/%s'%file)
		df=df.append(p, ignore_index=True)
	risk=df.groupby(['Name']).std()
	risk=risk.drop(['Id', 'Projected', 'Override','Salary'], axis=1)
	risk.to_csv('../Projections/risk.csv')


create_stats()

# schedule=pd.read_csv('../Data/schedule.csv')

# schedule=add_fatigue(schedule)
# schedule.to_csv('ayyyy.csv', index=False)