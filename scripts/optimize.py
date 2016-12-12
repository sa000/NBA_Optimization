
from pulp import *
import numpy as np
import pandas as pd
import re 



def optimize():

	data=pd.read_csv('../Projections/past/projection_Dec112016.csv')
	prob = pulp.LpProblem('NBA', pulp.LpMaximize)

	#decision variables
	decision_variables = []
	player_names=[]
	player_vars={}
	projected_lineup=[]
	scored_lineup=[]
	
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
		formula = (row['Projected']+.001)*variable
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
	optimization_result = prob.solve()
	print "final"
	print prob
	prob.writeLP("NBA.lp" )

	assert optimization_result == pulp.LpStatusOptimal
	print("Status:", LpStatus[prob.status])
	# print("Optimal Solution to the problem: ", value(prob.objective))
	print ("Individual decision_variables: ")
	cost=0

	for v in prob.variables():
		print(v.name, "=", v.varValue)
		if v.varValue:
			projected_lineup.append(player_vars[v.name])
			scored_lineup.append(data[data['Name']==player_vars[v.name]].Scored.values[0])

	print projected_lineup
	print scored_lineup

 	print("Expected Calculations ", value(prob.objective))
 	print 'Scored Calculations', sum(scored_lineup)







optimize()