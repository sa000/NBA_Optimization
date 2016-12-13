
from pulp import *
import numpy as np
import pandas as pd
import re 
import csv

def optimize(projected_lineup, date, iteration):
	#use modified or unmodified projections
	data=pd.read_csv('../Projections/past/projection_%s.csv'%date)
	#data=pd.read_csv('../Projections/Modified_Projection/Mprojection_%s.csv'%date)
	prob = pulp.LpProblem('NBA', pulp.LpMaximize)

	#decision variables
	decision_variables = []
	player_names=[]
	player_vars={}

	
	position_arr=[]
	total_Pts = ""
	for rownum, row in data.iterrows():
		positions={}
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



		variable = str('x' + str(rownum))
		player_vars[variable]=row['Name']
		variable = pulp.LpVariable(str(variable), lowBound = 0, upBound = 1, cat= 'Integer') #make variables binary
		
		decision_variables.append(variable)
		


		#Setting up objective function : Maximize projected points
		if projected_lineup:
			column='Projected'
		else:
			column='Scored'
		formula = (row[column]+.001)*variable
		print formula
		total_Pts += formula
	print ("Total number of decision_variables: " + str(len(decision_variables)))
	print ("Array with Decision Variables:" + str(decision_variables))

	#Maximization total pts


	prob +=  lpSum(total_Pts)
	##Subject to our budget 
	total_budget=50000
	total_cost=""
	player_num=""
	print "Setting up Budget Constraints \n"
	for rownum, row in data.iterrows():
		for i, player in enumerate(decision_variables):
			if rownum == i:
				formula = row['Salary']*player
				total_cost += formula
				#print row['Name'], player
				#print row['Salary']
				#print '\n'

	print "total cost is \n"
	print str(total_cost)
	#We cant exceed budget
	prob += (total_cost <= total_budget)

	print "Setting up Position Constraints \n"
	##Position restrictions
	pgs=sgs=sfs=pfs=cs=''

	for rownum, row in data.iterrows():
		for i, player in enumerate(decision_variables):
			if rownum == i:
				#print position_arr[i]
				pgs += position_arr[i]['PG']*player
				sgs += position_arr[i]['SG']*player
				sfs += position_arr[i]['SF']*player
				pfs += position_arr[i]['PF']*player
				cs += position_arr[i]['C']*player
				player_num+=player

	#print "Position constraints"
	#print pgs, sgs, sfs, pfs, cs

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
	target=open(file, 'w')
	player_list=[]
	for i in xrange(8):
		player_list.append('Player%s' %str(i+1))

	headers=player_list+['Projected Value', 'Actual Scored', 'Iteration'] 
	csvwriter=csv.writer(target)
	csvwriter.writerow(headers)
	for i in range(1,iterations+1):
		projected_lineup=[]
		scored_lineup=[]
		optimization_result = prob.solve()
		selected_vars = []
		print "final"
		#print prob
		fileLP="NBA%d.lp"%i
		prob.writeLP(fileLP)
		os.rename(fileLP, '../Prediction/%s'%fileLP)

		assert optimization_result == pulp.LpStatusOptimal
		print("Status:", LpStatus[prob.status])
		print ("Individual decision_variables: ")

		for v in prob.variables():
			#print(v.name, "=", v.varValue)
			if v.varValue:
				#print v
				selected_vars.append(v)
				projected_lineup.append(player_vars[v.name])
				scored_lineup.append(data[data['Name']==player_vars[v.name]].Scored.values[0])
		#Diversity constraint
		diversity_constraint=sum([var for var in selected_vars])
		print 'new constraint', diversity_constraint<=3
		prob+=(diversity_constraint<=4)

		print projected_lineup
		print scored_lineup

	 	print("Expected Calculations ", value(prob.objective))
	 	print 'Scored Calculations', sum(scored_lineup)
	 	final_output=projected_lineup+[value(prob.objective), sum(scored_lineup), i ]
	 	csvwriter.writerow(final_output)
	 	print "Iteration%d" %i
	target.close()
	os.rename(file, '../Prediction/%s' %file)



##Initial Parameters

projected_lineup=False #If true, generated projected lineup. if 0, generates the BEST lineup for that given night.
date='Dec122016'

iterations=10

optimize(projected_lineup, date,iterations)