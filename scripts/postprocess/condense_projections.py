import pandas as pd
import os
import time
import calendar
import datetime

def merge(files, path):
	df=pd.DataFrame()
	for file in files:
		print file
		#date=file.strip('projection_').strip('.csv')
		p=pd.read_csv('%s%s'%(path,file))
		date=file.strip('_Scored.csv')
		print date
		d1=date[:-4]
		month=d1[:3]
		day=int(d1[3:])
		year=int(date[-4:])
		abbr_to_num = {name: num for num, name in enumerate(calendar.month_abbr) if num}
		month=abbr_to_num[month]
		date=datetime.date(year, month, day).isoformat()
		#print date
		p['Date']=date
		#p.drop('Override', axis=1, inplace=True)
		df=df.append(p, ignore_index=True)


	#df.sort(['Actual Scored'], ascending=False)
	df.to_csv('../../Projections/ProjectionsPerfect_PositionConstraints.csv', index=False)



def add_num_games(files):
	sched=pd.read_csv('../../Data/schedule.csv')
	for file in files:
		date=file.strip('_P.csv')
		sched_date=date[3:5]+'-'+date[0:3]+'-'+date[-2:]
		games=sched[sched['DATE']==sched_date]
		num_games=games.shape[0]
		proj=pd.read_csv('../../Prediction/%s'%file)
		proj['Num_Games']=num_games
		proj.to_csv('../../Prediction/%s'%file, index=False)
		print file

path='../../Prediction/'

files=os.listdir(path)[1:]
print files

merge(files, path)