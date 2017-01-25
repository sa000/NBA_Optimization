from pulp import *
import collections

import numpy as np
import pandas as pd
import re 
import csv
import random
from  player import Player
import calendar
import datetime
#Create an optimize lineup to enter in Draft Kings contests .
#Forcing diversity constraints , team stacking, and frequency limits to produce smart lineups to enter.


def optimize(setting, date, iterations):
	monthdate=date[0:-4]
	abbr_to_num = {name: num for num, name in enumerate(calendar.month_abbr) if num}
	month=abbr_to_num[monthdate[0:3]]
	date_str=date[-4:]+'-'+str(month)+'-'+monthdate[3:]
	print date_str
	filename='%s_%s.csv' %(date, setting)

	#data=pd.read_csv('../Projections/past/projection_%s.csv'%date)
	data=pd.read_csv('../Projections/projections_NN.csv')
	data=data[data.Date==date_str]
	prob = pulp.LpProblem('NBA', pulp.LpMaximize)

	players={}
	#trans only
	player_to_vars={}
	total_budget=50000

	pgs=sgs=sfs=pfs=cs=''
	pg_salary=''
	pfs_salary=''
	objective_function=''
	total_cost=''
	num_players=''
	teams=data.Team.unique()
	team_constraints={}
	#Initialize team constraints
	for team in teams:
		team_constraints[team]=''

	for rownum, row in data.iterrows():
		#Create a variable and player instance for each row
		variable = str('x' + str(rownum))
		variable = pulp.LpVariable(str(variable), lowBound = 0, upBound = 1, cat= 'Integer')

		player=Player(row, str(variable))
		players[str(variable)]=player
		num_players += variable
		player_to_vars[row.Name]=variable
		#print variable

		player_points = row[setting]*variable
		objective_function += player_points

		player_cost = row['Salary']*variable
		total_cost+= player_cost

		#Categorize players by position groups

		pgs += player.position['PG']*variable
		#pg_salary+=player.position['PG']*variable*player.salary
		sgs += player.position['SG']*variable

		sfs += player.position['SF']*variable
		pfs += player.position['PF']*variable
		#pfs_salary+=player.position['PF']*variable*player.salary
		cs += player.position['C']*variable

		#Categorize by team
		team_constraints[player.team]+=variable
	#Set  the objective function
	prob +=  lpSum(objective_function)


	#Mininum constraints for an eligible lineup
	prob += (total_cost <= total_budget)
	prob += (num_players ==8)
	#prob += (pg_salary >= 8000*pgs)
	#prob += (pfs_salary <= 7000*pfs)
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

	div_limit=3  
	lineups=[]
	trans=pd.read_csv('../Projections/transactions_clean.csv')
	recent_dates=trans[trans.Date<date].Date.unique()[-5:]
	trans=trans[trans['Date'].isin(recent_dates)]
	hot_players=''
	hot_list=[]
	cold_players=''
	cold_list=[]
	# for idx, row in trans.iterrows():
	# 	if row.Name in player_to_vars.keys() and row.Name not in hot_list and row.Name not in cold_list:

	# 		if row.Net>5000:
	# 			hot_list.append(row.Name)
	# 			hot_players+=player_to_vars[row.Name]
	# 		if row.Net<=-1000:
	# 			cold_list.append(row.Name)
	# 			cold_players+=player_to_vars[row.Name]
	for idx, row in data.iterrows():
		if row.Name not in hot_list:
			if row.last1>30 and row.Salary<8000:
				hot_players+=player_to_vars[row.Name]
				hot_list.append(row.Name)
			elif row.last3<30 and row.Salary>8000:
				hot_players+=player_to_vars[row.Name]
				hot_list.append(row.Name)
			elif row.last1>30 and row.last3>30 and row.Salary<8000:
				hot_players+=player_to_vars[row.Name]
				hot_list.append(row.Name)
			else:
				pass
		if row.last1<30 and row.Salary<8000:
			cold_players+=player_to_vars[row.Name]


	print hot_players 
	print cold_players
	#print cold_players

	prob += (hot_players >=3)
	prob +=(cold_players<=0)
	#prob += (cold_players <=1)
	#Additiaional Constraint 1: Team stacking
	if setting=='Projected':
		p_formula=''
		for index, team in enumerate(team_constraints):
			p_var=pulp.LpVariable('P%s'%str(index), cat= 'Binary')
			p_formula+=p_var
			prob+=(team_constraints[team]>=p_var)
			prob+=(team_constraints[team]/8<=p_var)

		prob+=(p_formula==7)

	for i in range(1,iterations+1):

		print 'Iteration %d'% i
		fileLP="NBA_X%d.lp"%i
		#prob.writeLP(fileLP)


		optimization_result = prob.solve()
		assert optimization_result == pulp.LpStatusOptimal
		lineup=[]
		selected_vars=[]
		diversity_constraint=''
		freq_limit=10
		div_limit=3
		lineup_values=[]
		for var in prob.variables():
			if 'x' not in str(var):
				continue
			if var.varValue:
				
				selected_vars.append(var)
				player=players[str(var)]
				lineup.append(player)
				#print player.name, player.scored, player.projected
				#Update player count such and a new constraint
				player.count+=1
				frequency_constraint=''
				frequency_constraint+=player.count*var+var
				#Places a cap how many times a player can be used
				if setting =='Projected':
					prob+=(frequency_constraint<=freq_limit)
				#Resets the value to be 'fresh' for next optimization
				var.varValue=0
			#Force diversity s.t no than two lineups can share more than 3 players
		diversity_constraint=sum([var for var in selected_vars])				
		prob+=(diversity_constraint<=div_limit)

		lineups.append(lineup)
	write_output(lineups, filename,prob)

#Soley to write out data
def write_output(lineups, filename, prob):
	#Writes lineups to csv
	player_list=[]
	team_list=[]
	pos_list=[]
	salary_list=[]
	for i in xrange(8):
		player_list.append('Player%s' %str(i+1))
		team_list.append('Team%s' %str(i+1))
		pos_list.append('Pos%s' %str(i+1))
		salary_list.append('Salary%s' %(str(i+1)))
	target=open(filename, 'w')
	headers=player_list+team_list+pos_list+salary_list+['Projected Value', 'Actual Scored', 'Iteration', 'date'] 
	target=open(filename, 'w')
	csvwriter=csv.writer(target)
	csvwriter.writerow(headers)
	for iteration, lineup in enumerate(lineups):
		names=[]
		teams=[]
		scored=[]
		salaries=[]
		projected=[]
		positions=[]
		for player in lineup:
			names.append(player.name)
			teams.append(player.team)
			scored.append(player.scored)
			projected.append(player.projected)
			positions.append(player.pos)
			salaries.append(player.salary)
		counter=collections.Counter(teams)

		final_output=names+teams+positions+salaries+[round(sum(projected),2), round(sum(scored),2), iteration+1, date]
		csvwriter.writerow(final_output)
	target.close()

	df=pd.read_csv(filename)
	df=df.sort_values(['Actual Scored'], ascending=False)
	df.to_csv('../Prediction/%s'% filename, index=False)




dates=os.listdir('../Projections/past')[1:]
dates=[date.strip('projection_').strip('.csv') for date in dates]
iterations=50
for date in dates[0:1]:
	optimize('Projected', date,iterations)