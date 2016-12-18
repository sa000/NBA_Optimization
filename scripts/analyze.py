import csv
import os
import pandas as pd
##Grab data
import numpy as np
from teams import teams_dict
import calendar
import datetime
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
		#print file
		p=pd.read_csv('../Projections/past/%s'%file)
		df=df.append(p, ignore_index=True)
	players=df['Name'].unique()
	header=['Name', 'Average FPTS', 'STD FPTS', 'Average Diff', 'STD diff']
	target=open('../Data/risk.csv', 'w')
	csvwriter=csv.writer(target)
	csvwriter.writerow(header)
	for player in players:
		print player
		player_df=df[df['Name']==player]
		diff=player_df['Scored']-player_df['Projected']
		avg=np.average(player_df['Scored'])
		std=np.std(player_df['Scored'])
		avg_diff=np.average(diff)
		std_diff=np.std(diff)
		data=[player,round(avg,2),round(std,2), round(avg_diff, 2), round(std_diff, 2)]
		csvwriter.writerow(data)
	target.close()


def create_risk_csv():
	data=pd.read_csv('../Data/Projected_WithRisk.csv')
	target=open('../Data/Lineup_Risks_Projected.csv', 'w')
	risk=pd.read_csv('../Data/risk.csv')
	headers=['Name', 'Pos', 'Risk']
	csvwriter=csv.writer(target)
	csvwriter.writerow(headers)
	for index, row in data.iterrows():
		for i in xrange(8):
			name=row[i]
			pos=row[16+i]
			std=round(risk[risk['Name']==name]['STD FPTS'].values[0],2)
			info=[name, pos, std]
			csvwriter.writerow(info)
	target.close()


def creating_net_data():
	data=pd.read_csv('../Data/Raw_Projected_Cumulated.csv')
	sched=pd.read_csv('../Data/schedule.csv')
	team_abr={v: k for k, v in teams_dict.iteritems()}
	positions=['PG','SG','SF','PF','C']
	pos_encode={}
	teams=sched.VISITOR.unique()
	teams.sort()
	headers=['Home', 'Away', 'Last 5','PG','SG','SF','PF','C', 'Number of games played last 5']
	p_team=["Player_%s"%team for team in teams]
	opp_team=['OPP_%s'%team for team in teams]
	headers.extend(p_team)
	headers.extend(opp_team)
	who_v_who_teams=[]
	who_v_who_teams.extend(teams)
	who_v_who_teams.extend(teams)
	abbr_to_num = {name: num for num, name in enumerate(calendar.month_abbr) if num}
	target=open('../Data/Raw_Projected_Update.csv','w')
	csvwriter=csv.writer(target)
	total_header=[]
	total_header.extend(data.columns.values)
	total_header.extend(headers)
	csvwriter.writerow(total_header)
	for index, pos in enumerate(positions):
		encode=[0,0,0,0,0]
		encode[index]=1
		pos_encode[pos]=encode
	for index, row in data.iterrows():

		print row.Name
		cur_data=[]
		cur_data.extend(row.values)
		cur_date=row.Date
		#strip the date:
		cur_mon=abbr_to_num[cur_date[0:3]]
		day=cur_date[3:].split('2016')[0]
		if len(day)<2:
			day='0%s'%day
		year='2016'
		cur_proper_date=datetime.date(2016, cur_mon, int(day))
		date=row.Date[0:-4]
		sched_date=date[3:]+'-'+date[0:3]+'-'+'16'
		games=sched[sched['DATE']==sched_date]
		team=row.Team
		full_team=team_abr[team]
		#print 'PREDSET', full_team
		# if full_team not in ['L.A Clippers', 'L.A Lakers', 'New Orleans', 'Oklahoma City', 'New York']:
		# 	print 'case', full_team
		# 	full_team=full_team.split(' ')[0]

		if len(full_team.split(' '))>2:
			full_team=" ".join(full_team.split(' ')[0:2])
		else:
			full_team=full_team.split(' ')[0]
		#print 'post', full_team
		for g_row, game in games.iterrows():
			if full_team in game.VISITOR:
				opp=game.HOME
				home=1
				away=0
				break
			if full_team in game.HOME:
				opp=game.VISITOR
				home=0
				away=1

		name=row.Name
		g_id=row.Id
		p_data=data[data.Name==name]
		pos=row.Position.split('/')[0]
		encode=pos_encode[pos]
		if len(p_data[p_data['Id']<g_id]['Scored'])<5:
			last_5=np.median(p_data[p_data['Id']<g_id]['Scored'])
		else:
			last_5=np.median(p_data[p_data['Id']<g_id]['Scored'][-5:])
		num_games=0
		for p_index, p_row in p_data[p_data['Id']<g_id].iterrows():
			compared_date=p_row.Date
			compared_mon=abbr_to_num[compared_date[0:3]]
			day=compared_date[3:].split('2016')[0]
			if len(day)<2:
				day='0%s'%day
			compared_date=datetime.date(2016, compared_mon, int(day))
			#print 'dates', compared_date, cur_proper_date, abs((compared_date-cur_proper_date).days)

			if (compared_date-cur_proper_date).days>=-5:
				num_games+=1
				#print 'TRUE'

		new_info=[home, away, last_5, encode,]
		who_v_who=[0]*60
		#print 'PRE', full_team, opp
		for team_index, value in enumerate(teams):
			if full_team in value:
				player_index=team_index
				#print 'player_team' ,full_team, value
			if opp in value:
				opp_index=team_index
				#print 'opp_team', opp, value, 
		#print player_index, opp_index
		who_v_who[player_index]=1
		who_v_who[opp_index+30]=1
		new_info=[home, away, last_5]
		new_info.extend(encode)
		new_info.extend( [num_games])
		new_info.extend(who_v_who)
		cur_data.extend(new_info)
		csvwriter.writerow(cur_data)
	target.close()



def get_num_of_games(date):
	date=date[0:-4]
	sched=pd.read_csv('../Data/schedule.csv')
	sched_date=date[3:]+'-'+date[0:3]+'-'+'16'
	games=sched[sched['DATE']==sched_date]
	num_games=games.shape[0]
	return num_games	
creating_net_data()	
#create_stats()
# create_risk_csv()
# schedule=pd.read_csv('../Data/schedule.csv')

# schedule=add_fatigue(schedule)
# schedule.to_csv('ayyyy.csv', index=False)