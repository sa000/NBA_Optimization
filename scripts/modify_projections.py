import pandas as pd 
from teams import *
#Account for team defense
def defense(date):
	projections=pd.read_csv('../Projections/past/projection_%s.csv'%date)
	schedule=pd.read_csv('../Data/schedule.csv')
	sched_date=date[3:5]+'-'+date[0:3]+'-'+'16'
	teams_abr = {v: k for k, v in teams_dict.iteritems()}

	for index_p, proj in projections.iterrows():
		print proj.Name

		team=proj.Team
		team=teams_abr[team]
		print team

		if team in ['L.A. Lakers','L.A. Clippers']:
			print 'a'
			city=team
		elif len(team.split(' '))>2 and 'Trail' not in team.split(' '):
			print 'b'
			city=" ".join(team.split(' ')[0:2])
		else:
			print 'c'
			city=team.split(' ')[0]
		print city
		#Find opponent
		todays_games=schedule[schedule['DATE']==sched_date]
		if city in todays_games['VISITOR'].values:
			opp=todays_games[todays_games['VISITOR']==city]['HOME'].values[0]
		else:#home team
			print city
			opp=todays_games[todays_games['HOME']==city]['VISITOR'].values[0]

		pos=proj.Position.split('/')[0]
		#with pos and opp, we can alter his projected score
		defense=pd.read_csv('../Data/DVP_%s.csv'%pos)

		for index, row in defense.iterrows():
			if opp in row['Team'].split() :
				break
				#found our index
		if proj['Salary']<=6000:
			if index<=6:
				scale=1.4
			elif index<=12:
				scale=1.2
			elif index<=18:
				scale=1
			elif index<=24:
				scale=.8
			else:
				scale=.6

			projections.set_value(index_p, 'Projected', proj['Projected']*scale)
	projections.to_csv('../Projections/Modified_Projection/Mprojection_%s.csv'%date, index=False)


date='Dec112016'

defense(date)