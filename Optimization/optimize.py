from pulp import *
import collections

import numpy as np
import pandas as pd
import re 
import csv
import random
from  player import Player

def optimize(setting, date, iterations):

	filename='%s_%s.csv' %(date, setting)
	data=pd.read_csv('../Projections/past/projection_%s.csv'%date)
	prob = pulp.LpProblem('NBA', pulp.LpMaximize)

	players={}
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

		player_points = row[setting]*variable
		objective_function += player_points

		player_cost = int(round(row['Salary']/5.0)*5.0)*variable
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
	#Additiaional Constraint 1: Team stacking
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
		prob.writeLP(fileLP)


		optimization_result = prob.solve()
		assert optimization_result == pulp.LpStatusOptimal
		lineup=[]
		selected_vars=[]
		diversity_constraint=''
		freq_limit=10
		div_limit=3
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
				prob+=(frequency_constraint<=freq_limit)
				#Resets the value to be 'fresh' for next optimization
				var.varValue=0
		diversity_constraint=sum([var for var in selected_vars])
		#Force diversity s.t no twol two lineups can share more than 3 players
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
	df.to_csv(filename, index=False)




dates=os.listdir('../Projections/past')[1:]
date=[date.strip('projection_').strip('.csv') for date in dates][0]
iterations=50
optimize('Projected', date,iterations)