import pandas as pd 
import numpy as np 
import math

def create_projections(date, name):
	projections=pd.read_csv('../../Projections/Projections.csv')
	bayes_proj=pd.read_csv('../../Projections/past/%s'%name)
	for idx, row in bayes_proj.iterrows():
		player=row.Name
		print player
		p_proj=projections[(projections['Name']==player) &(projections['Date']<date)]
		season_average=np.average(p_proj['Scored'])
		last_5=np.median(p_proj['Scored'][-5:])
		last_3=np.median(p_proj['Scored'][-3:])
		last_1=np.median(p_proj['Scored'][-1:])
		std=np.std(p_proj['Scored'])
		bayes_proj.set_value(idx, 'last_5', last_5)
		bayes_proj.set_value(idx, 'last_3', last_3)
		bayes_proj.set_value(idx, 'last_1', last_1)
		bayes_proj.set_value(idx, 'std', round(std,2))
		proj=row.Projected
		bucket=int(math.ceil(proj/5))
		if bucket>8:
			bucket=8
		for i in range(1,9):
			if bucket==i:
				bayes_proj.set_value(idx, 'bucket%s'%str(int(i*5)), int(1))
			else:
				bayes_proj.set_value(idx, 'bucket%s'%str(int(i*5)), int(0))




	bayes_proj.to_csv('bayes.csv', index=False)
date='2017-01-02'
name='projection_Jan22017.csv'
create_projections(date,name)
