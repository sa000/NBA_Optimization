import pandas as pd 
import numpy as np 
import math
from datetime import datetime

projections=pd.read_csv('../../Projections/Projections.csv')
def create_projections(date, name):
	
	bayes_proj=pd.read_csv('../../Projections/past/%s'%name)
	sched=pd.read_csv('../../Data/schedule.csv')
	for idx, row in bayes_proj.iterrows():
		player=row.Name
		print player
		p_proj=projections[(projections['Name']==player) &(projections['Date']<date)]
		season_average=np.average(p_proj['Scored'])
		last_5=np.median(p_proj['Scored'][-5:])
		last_3=np.median(p_proj['Scored'][-3:])
		last_1=np.median(p_proj['Scored'][-1:])
		std=np.std(p_proj['Scored'])
		bayes_proj.set_value(idx, 'last_5', last_5)
		bayes_proj.set_value(idx, 'last_3', last_3)
		bayes_proj.set_value(idx, 'last_1', last_1)
		bayes_proj.set_value(idx, 'std', round(std,2))
		proj=row.Projected
		bucket=int(math.ceil(proj/5))
		# if bucket>8:
		# 	bucket=8
		# if bucket==0:
		# 	bucket=1
		# for i in range(1,9):
		# 	if bucket==i:
		# 		bayes_proj.set_value(idx, 'bucket%s'%str(int(i*5)), int(1))
		# 	else:
		# 		bayes_proj.set_value(idx, 'bucket%s'%str(int(i*5)), int(0))
 		home_away=home_or_away(date,row.Team)
 		b2b, count=add_fatigue(date,row.Team, player)
 		bayes_proj.set_value(idx, 'b2b', b2b)
 		bayes_proj.set_value(idx, 'Games played in last 5 days', count)
 		bayes_proj.set_value(idx, 'Home', home_away)
 		print bayes_proj.columns
 		bayes_proj=bayes_proj.drop(''u'Override''',1)
	bayes_proj.to_csv('../../Data/Bayes/bayes_%s.csv' %date, index=False)

def extend_projections():
	projections.sort('Date', ascending=1, inplace=True)
	for idx, row in projections.iterrows():
		player=row.Name
		date=row.Date
		print player
		p_proj=projections[(projections['Name']==player) &(projections['Date']<date)]
		last_5=np.nan_to_num(np.median(p_proj['Scored'][-5:]))
		last_3=np.nan_to_num(np.median(p_proj['Scored'][-3:]))
		last_1=np.nan_to_num(np.median(p_proj['Scored'][-1:]))
		std=round(np.std(projections[(projections['Name']==player)]['Scored']),2)
		projections.set_value(idx, 'last_5', last_5)
		projections.set_value(idx, 'last_3', last_3)
		projections.set_value(idx, 'last_1', last_1)
		projections.set_value(idx, 'std', round(std,2))
 		home_away=home_or_away(date,row.Team)
 		b2b, count=add_fatigue(date,row.Team, player)
 		projections.set_value(idx, 'b2b', b2b)
 		projections.set_value(idx, 'Games played in last 5 days', count)
 		projections.set_value(idx, 'Home', home_away)
 	projections.to_csv('../../Data/projections_x.csv', index=False)		

def home_or_away(date, team):
	schedule=pd.read_csv('../../Data/schedule.csv')
	schedule=schedule[schedule['DATE']==date]
	if team in schedule.VISITOR.values:
		return 0
	if team in schedule.HOME.values:
		return 1
def add_fatigue(date, team, player):
	proj=projections.sort(['Date'], ascending=1)
	proj=proj[(proj['Team']==team) & (proj['Name']==player) & (proj['Date']<date)][-6:] 
	date_format = "%Y-%m-%d"
	b2b=0
	if len(proj)>0:
		last_played=proj.tail(1).Date.values[0]
		if (datetime.strptime(date, date_format)-datetime.strptime(last_played,date_format)).days==1:
			b2b=1
		else:
			b2b=0
	count=0
	for idx, row in proj.iterrows():
		cur_date=row.Date
		if (datetime.strptime(date,date_format)-datetime.strptime(cur_date,date_format)).days<5:
			count+=1
	return b2b, count 
extend_projections()
# date='2017-01-01'
# name='projection_Jan12017.csv'
# create_projections(date,name)
