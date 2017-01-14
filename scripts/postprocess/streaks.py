import pandas as pd
from datetime import datetime
import numpy as np

def add_history():
	projections=pd.read_csv('../../Projections/Projections.csv')
	projections['Streak']=0
	projections.sort('Date', inplace=True)
	for idx, row in projections.iterrows():
		print idx
		date=row.Date
		name=row.Name
		salary=row.Salary
		scored=row.Scored
		p_proj=projections[(projections['Name']==name) &(projections['Date']<date)]
		if len(p_proj)>0:
			prev_streak=p_proj.iloc[-1].Streak
			delta_salary=p_proj.iloc[-1].Salary-salary 
		else:
			delta_salary=0
			prev_streak=0
		if scored>35:
			projections.set_value(idx, 'Streak', prev_streak+1)
		season_average=np.average(p_proj['Scored'])
		last_5=np.average(p_proj['Scored'][-5:])
		last_3=np.average(p_proj['Scored'][-3:])
		last_1=np.average(p_proj['Scored'][-1:])
		prev_scored=p_proj.Scored
		
		projections.set_value(idx, 'last5', last_5)
		projections.set_value(idx, 'last3', last_3)
		projections.set_value(idx, 'last1', last_1)
		projections.set_value(idx, 'Salary Change', delta_salary)
	projections.to_csv('projections_NN.csv')

add_history()
