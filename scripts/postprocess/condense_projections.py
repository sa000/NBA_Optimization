import pandas as pd
import os
def merge(files):
	df=pd.DataFrame()
	for file in files:
		print file
		p=pd.read_csv('../../Prediction/%s'%file)
		df=df.append(p, ignore_index=True)
	df.sort(['Actual Scored'], ascending=False)
	df.to_csv('../../Data/Perfect_WithRisk.csv', index=False)



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
files=os.listdir('../../Prediction/')[1:]


merge(files)