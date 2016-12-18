
import random

from pulp import *
import numpy as np
import pandas as pd
import re 
import csv
import random

def optimize(projected_lineup, date, iterations):
	#use modified or unmodified projections
	print date
	data=pd.read_csv('../Projections/past/projection_%s.csv'%date)

	prob = pulp.LpProblem('NBA', pulp.LpMaximize)
	


	teams=data.Team.unique()
	team_dict={}
	p_vars=[]
	p_formula=''
	risk=pd.read_csv('../Data/risk.csv')
	#decision variables
	decision_variables = []
	player_names=[]
	player_vars={}
	player_pos_team={}
	
	position_arr=[]
	team_arr=[]
	total_Pts = ""
	for rownum, row in data.iterrows():
		positions={}
		name=row.Name
		positions['PG']=positions['SG']=positions['SF']=positions['PF']=positions['C']=0
		#For each player, classify their position
		if 'PG' in row['Position']:
			positions['PG']=1
		if 'SG' in row['Position']:
			positions['SG']=1
		if 'SF' in row['Position']:
			positions['SF']=1
		if 'PF' in row['Position']:
			positions['PF']=1
		if 'C' in row['Position']:
			positions['C']=1
		position_arr.append(positions)

		#Clasiffy teams

		team_dict[row['Team']]=1
		team_arr.append(team_dict)

		variable = str('x' + str(rownum))
		player_vars[variable]=row['Name']
		player_pos_team[variable]=[row['Position'], row['Team']]
		variable = pulp.LpVariable(str(variable), lowBound = 0, upBound = 1, cat= 'Integer') #make variables binary
		
		decision_variables.append(variable)
		

		#Setting up objective function : Maximize projected points
		if projected_lineup:
			column='Projected'
		else:
			column='Scored'
		#formula = (srow[column]+.001)*variable
		#total_Pts += formula


	#prob +=  lpSum(total_Pts)
	##Subject to our budget 
	total_budget=50000
	total_cost=""
	player_num=""
	pgs=sgs=sfs=pfs=cs=''
	team_c1=''
	for rownum, row in data.iterrows():
		for i, player in enumerate(decision_variables):
			if rownum == i:
				#Budget Constraint
				formula = row['Salary']*player
				total_cost += formula
				#print position_arr[i]
				#Player type constraint
				pgs += position_arr[i]['PG']*player
				sgs += position_arr[i]['SG']*player
				sfs += position_arr[i]['SF']*player
				pfs += position_arr[i]['PF']*player
				cs += position_arr[i]['C']*player
				player_num+=player
				for team in teams:
					team_c1=team_arr[i][team]*player

		
		
		

	p_vars=[]


	prob += (total_cost <= total_budget)


	prob += (player_num ==8)

	prob += (pgs <=3)
	prob += (pgs >=1)

	prob += (sgs <=3)
	prob += (sgs >=1)

	prob += (sfs <=3)
	prob += (sfs >=1)

	prob += (pfs <=3)
	prob += (pfs >=1)

	prob += (cs <=2)
	prob += (cs >=1)


	diversity_constraint=''
	if projected_lineup:
		file='%s_P.csv' % date
	else:
		file='%s_S.csv' %date

	player_list=[]
	team_list=[]
	pos_list=[]
	for i in xrange(8):
		player_list.append('Player%s' %str(i+1))
		team_list.append('Team%s' %str(i+1))
		pos_list.append('Pos%s' %str(i+1))

	#Solving the problem
	div_limit=3 #Setting to 8 essentially nullifies the constraint. this should be used for the best lineup
	target=open(file, 'w')
	headers=player_list+team_list+pos_list+['Projected Value', 'Actual Scored', 'Iteration', 'date', 'NumGames', 'Risk'] 
	csvwriter=csv.writer(target)
	csvwriter.writerow(headers)
	for i in range(1,iterations+1):

		total_Pts=''
		if i>1:
			data=pd.read_csv('../Projections/past/projection_%s.csv'%date)
			data=run_monte_carlo(data)
		for rownum, row in data.iterrows():
			variable=decision_variables[rownum	]
			formula = row['Projected']*variable
			total_Pts += formula


		prob +=  lpSum(total_Pts)
		num_games=get_num_of_games(date)
		positions=[]
		projected_lineup=[]
		scored_lineup=[]
		optimization_result = prob.solve()
		selected_vars = []



		assert optimization_result == pulp.LpStatusOptimal

		teams=[]
		risks=[]
		risk=pd.read_csv('../Data/risk.csv')
		for v in prob.variables():
			if v.varValue:
				#print v
				#print v.name
				selected_vars.append(v)
				projected_lineup.append(player_vars[v.name])
				scored_lineup.append(data[data['Name']==player_vars[v.name]].Scored.values[0])
				teams.append(player_pos_team[v.name][1])
				positions.append(player_pos_team[v.name][0].split('/')[0])

		diversity_constraint=sum([var for var in selected_vars])

		#prob+=(diversity_constraint<=div_limit)

	 	final_output=projected_lineup+teams+positions+[value(prob.objective), sum(scored_lineup), i, date, num_games, round(sum(risks),2)]
	 	csvwriter.writerow(final_output)
	 	print i, sum(scored_lineup)

	target.close()
	df=pd.read_csv(file)
	df=df.sort(['Actual Scored'], ascending=False)
	df.to_csv(file, index=False)
	os.rename(file, '../Prediction/%s' %file)

def get_num_of_games(date):
	date=date[0:-4]
	sched=pd.read_csv('../Data/schedule.csv')
	sched_date=date[3:]+'-'+date[0:3]+'-'+'16'
	games=sched[sched['DATE']==sched_date]
	num_games=games.shape[0]
	return num_games

##Initial Parameters





def run_monte_carlo(df):
	risk=pd.read_csv('../Data/risk.csv')
	for index, row in df.iterrows():
		num=random.uniform(0,1)
		proj=row.Projected
		name=row.Name
		std=risk[risk.Name==name]['STD FPTS']
		if num<=.15:
			new_proj=proj-.75*std
			#print proj
		elif num>=.85:
			new_proj=proj+.75*std
		else:
			new_proj=proj+random.uniform(-1,1)*std
		# else:
		# 	if num<=.15:
		# 		new_proj=proj-1*std
		# 		#print proj
		# 	elif num>=.85:
		# 		new_proj=proj+1*std
		# 	else:
		# 		new_proj=proj+random.uniform(-1,1)*.25*std
		
		df.set_value(index, 'Projected', new_proj)
	return df
	
	

files=os.listdir('../Projections/past')[1:]
dates=[]
for file in files:
	date=file.strip('projection_').strip('.csv')
	dates.append(date)

df=pd.read_csv('../Projections/past/%s'%file)
for date in dates[1:2]:
	optimize(True,date, 3000)






