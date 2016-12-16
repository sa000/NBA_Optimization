import pandas as pd 
from teams import *
import numpy as np
import os
#Account for team defense
def defense(date):
	projections=pd.read_csv('../Projections/past/projection_%s.csv'%date)
	schedule=pd.read_csv('../Data/schedule.csv')
	date=date[0:-4]
	sched_date=date[3:]+'-'+date[0:3]+'-'+'16'
	teams_abr = {v: k for k, v in teams_dict.iteritems()}

	for index_p, proj in projections.iterrows():
		print proj.Name

		team=proj.Team
		team=teams_abr[team]
		#print team

		if team in ['L.A. Lakers','L.A. Clippers']:
			city=team
		elif len(team.split(' '))>2 and 'Trail' not in team.split(' '):
			city=" ".join(team.split(' ')[0:2])
		else:
			city=team.split(' ')[0]
		#print city
		#Find opponent
		print city, date
		todays_games=schedule[schedule['DATE']==sched_date]
		if city in todays_games['VISITOR'].values:
			opp=todays_games[todays_games['VISITOR']==city]['HOME'].values[0]
		else:#home team
			opp=todays_games[todays_games['HOME']==city]['VISITOR'].values[0]

		pos=proj.Position.split('/')[0]
		#with pos and opp, we can alter his projected score
		defense=pd.read_csv('../Data/DVP_%s.csv'%pos)
		risks=pd.read_csv('../Projections/risk.csv')
		std=risks[risks['Name']==proj.Name]['Scored'].values[0]
		if np.isnan(std):
			std=0
		for index, row in defense.iterrows():
			if opp in row['Team'].split() :
				break
				#found our index
		if proj['Salary']<=6000:
			if index<=6:
				scale=.75*std
			elif index<=12:
				scale=.5*std
			elif index<=18:
				scale=0
			elif index<=24:
				scale=-.75*std
			else:
				scale=-.5*std
			print proj['Projected'], scale
			projections.set_value(index_p, 'Projected', max(proj['Projected']+scale,.1))
	projections.to_csv('../Projections/Modified_Projection/Mprojection_%s.csv'%date, index=False)


# dates=os.listdir('../Projections/past')[1:]
# dates=[date.strip('projection_').strip('.csv') for date in dates]
# for date in dates:
# 	defense(date)

data=pd.read_csv('../Data/Cumulative_Predictions.csv')

for index, row in data.iterrows():
	date=row.date
	new_date=date[0:3]+'-'+date[3:-4]+'-2016'
	data.set_value(index, 'date', new_date)
data.to_csv('../Data/Cumulative_Predictions.csv')