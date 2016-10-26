
from pulp import *
import numpy as np
import pandas as pd
import re 



def optimize():
	data=pd.read_csv('test1.csv')
	prob = pulp.LpProblem('NBA', pulp.LpMaximize)

	#decision variables
	decision_variables = []
	player_names=[]
	
	position_arr=[]

	for rownum, row in data.iterrows():
		positions={}
		positions['PG']=positions['SG']=positions['SF']=positions['PF']=positions['C']=0
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



	for rownum, row in data.iterrows():
		variable = str('x' + str(rownum))
		variable = pulp.LpVariable(str(variable), lowBound = 0, upBound = 1, cat= 'Integer') #make variables binary
		
		decision_variables.append(variable)

	print ("Total number of decision_variables: " + str(len(decision_variables)))
	print ("Array with Decision Variables:" + str(decision_variables))

	#Maximization total pts
	total_Pts = ""

	print "Calculating the objective function: \n"
	for rownum, row in data.iterrows():
		for i, player in enumerate(decision_variables):
			if rownum == i:
				player_names.append(row['Player'])
				formula = row['DK Pts']*player
				total_Pts += formula

	prob +=  total_Pts
	##Subject to our budget 
	total_budget=50000
	total_cost=""
	player_num=""
	print "Setting up Budget Constraints \n"
	for rownum, row in data.iterrows():
		for i, player in enumerate(decision_variables):
			if rownum == i:
				formula = int(row['Salary'].replace(',',''))*player
				total_cost += formula
				print row['Player'], player
				print int(row['Salary'].replace(',',''))
				print '\n'

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
				print position_arr[i]
				pgs += position_arr[i]['PG']*player
				sgs += position_arr[i]['SG']*player
				sfs += position_arr[i]['SF']*player
				pfs += position_arr[i]['PF']*player
				cs += position_arr[i]['C']*player
				player_num+=player

	print "Position constraints"
	print pgs, sgs, sfs, pfs, cs

	prob += (player_num ==8)

	prob += (pgs <=3)
	prob += (pgs >=0)

	prob += (sgs <=3)
	prob += (sgs >=0)

	prob += (sfs <=3)
	prob += (sfs >=0)

	prob += (pfs <=3)
	prob += (pfs >=0)

	prob += (cs <=2)
	prob += (cs >=0)
	optimization_result = prob.solve()
	print "final"
	print prob
	prob.writeLP("NBA.lp" )

	assert optimization_result == pulp.LpStatusOptimal
	print("Status:", LpStatus[prob.status])
	# print("Optimal Solution to the problem: ", value(prob.objective))
	print ("Individual decision_variables: ")
	cost=0
	for index, v in enumerate(prob.variables()):
		p_index=int(v.name.replace('x',''))
		print(v.name, "=", v.varValue, 'Player: ', player_names[p_index])
		if v.varValue:

			print data.loc[data['Name'] == player_names[p_index]]['Salary'].values[0].replace(',','')
			cost+=int(data.loc[data['Name'] == player_names[p_index]]['Salary'].values[0].replace(',',''))
	print "Final cost", cost






optimize()