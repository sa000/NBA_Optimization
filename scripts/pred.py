import pandas as pd
import numpy as np
def create_prediction_file():
	data=pd.read_csv('data.csv')
	dates=data['Date'].unique()
	past_data=pd.read_csv('../Data/2015_2016.csv')
	prediction=pd.DataFrame()
	for date in dates:
		gameday=data[data['Date']==date]
		players=gameday['Name'].values
		for index, row in gameday.iterrows():
			player=row['Name']
			salary=row['DK Salary']
			print index
			name=player.split(',')[1][1:]+' '+player.split(',')[0]
			team=row['Team'].upper()
			opp=row['Oppt'].upper()
			past_games=past_data[(past_data['Player']==name) & (past_data['Opp']==opp)]
			average=past_games.mean()
			risk=np.std(past_games['DKPts'])
			average['risk']=risk
			average['player']=name
			average['team']=team
			average['opp']=opp
			average['date']=int(date)
			average['Salary']=salary
			prediction=prediction.append(average,ignore_index=True)
			#print average
	prediction.to_csv('prediction.csv', ignore_index=True)

def update_dk_file():
	current_day=pd.read_csv('test1.csv')
create_prediction_file()		
