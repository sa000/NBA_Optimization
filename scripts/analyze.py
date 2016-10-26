import csv
import os
import pandas as pd
##Grab data
import numpy as np
from teams import teams_dict
def create_projections(schedule_date, data_date):
	data=pd.read_csv('../Data/small.csv')
	data=pd.read_csv('../Data/2015_2016.csv')
	data.is_copy=False
	schedule=pd.read_csv('../Data/schedule.csv')

	##Filter data based off teams that are currently playing
	filtered_schedule=schedule[schedule['Date']==schedule_date]
	home_teams=filtered_schedule['Home/Neutral'].values
	away_teams=filtered_schedule['Visitor/Neutral'].values
	home_teams_abr=[]
	away_teams_abr=[]

	for home_team, away_team in zip(home_teams, away_teams):
		home=teams_dict[home_team]
		away=teams_dict[away_team]
		home_teams_abr.append(home)
		away_teams_abr.append(away)
	
	games=zip(home_teams_abr, away_teams_abr)
 	games_df=[]
 	#target=open('relevant_games.csv'%data_date, 'wb')
 	player_df=[]
 	for game in games:
 		print 'going thru games'
 		game_df=data[ (data['Tm']==game[0]) & (data['Opp']==game[1]) | (data['Tm']==game[1]) & (data['Opp']==game[0]) ]
 		players=np.unique(game_df['Player'].values)
 		#create an average

 		for player in players:
 			print 'going thru players'
 			name=pd.Series(player)
 			name=name.rename({0:'Player'})

 			player_data=game_df[game_df['Player']==player].mean()
 			player_data=player_data.append(name)

 			player_df.append(pd.DataFrame(player_data).T)
 	print 'complete'
 	final_df=pd.concat(player_df)
 	final_df.to_csv('test1.csv', index=False)

	#We now have teams in the right format to filter our data




schedule_date='Tue Oct 25 2016'
data_date='10/25/2016'

create_projections(schedule_date, data_date)