from pulp import *
import numpy as np
import pandas as pd
import re 
import csv
import random
from  player import Player

def optimize(setting, date, iterations):
	filename='%s_%s' %(setting, date)
	data=pd.read_csv('../Projections/past/projection_%s.csv'%date)
	prob = pulp.LpProblem('NBA', pulp.LpMaximize)
	print 'hi'
	players={}
	total_budget=50000
	pgs=sgs=sfs=pfs=cs=''
	objective_function=''
	total_cost=''
	decision_variables=[]
	num_players=''
	for rownum, row in data.iterrows():
		variable = str('x' + str(rownum))
		variable = pulp.LpVariable(str(variable), lowBound = 0, upBound = 1, cat= 'Integer')
		player=Player(row, str(variable))
		players[str(variable)]=player
		decision_variables.append(variable)
		num_players += variable

		player_points = row[setting]*variable
		objective_function += player_points

		player_cost = row['Salary']*variable
		total_cost+= player_cost

		#Categorize players by position groups
		pgs += player.position['PG']*variable
		sgs += player.position['SG']*variable
		sfs += player.position['SF']*variable
		pfs += player.position['PF']*variable
		cs += player.position['C']*variable
	#Set  the objective function
	prob +=  lpSum(objective_function)


	#Mininum constraints for an eligible lineup
	prob += (total_cost <= total_budget)
	prob += (num_players ==8)

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

	#additional Constraint
	diversity_constraint=''
	div_limit=3  
	lineups=[]
	for i in range(1,iterations+1):
		print 'Iteration %d'% i
		fileLP="NBA_X%d.lp"%i
		prob.writeLP(fileLP)
		optimization_result = prob.solve()
		assert optimization_result == pulp.LpStatusOptimal
		lineup=[]
		for var in prob.variables():
			if 'x' not in str(var):
				continue
			if var.varValue:
				player=players[str(var)]
				lineup.append(player)
				print player.name, player.scored, player.projected
		lineups.append(lineup)
	save_data(filename,lineups)

def save_date(lineups):
	#Writes lineups to csv
	player_list=team_list=pos_list=[]
	for i in xrange(8):
		player_list.append('Player%s' %str(i+1))
		team_list.append('Team%s' %str(i+1))
		pos_list.append('Pos%s' %str(i+1))

	target=open(file, 'w')
	headers=player_list+team_list+pos_list+['Projected Value', 'Actual Scored', 'Iteration', 'date', 'NumGames', 'Risk'] 
	target=open(filename, 'w')
	csvwriter=csv.writer(target)
	csvwriter.writerow(headers)
	for lineup in lineups:
		data=[]
		for player in lineup:
			data.append(player.)


dates=os.listdir('../Projections/past')[1:]
date=[date.strip('projection_').strip('.csv') for date in dates][0]
iterations=1
optimize('Projected', date,iterations)