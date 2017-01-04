city_dict={ 
'Atlanta' :'ATL'	 ,
'Brooklyn' :'BKN'	 ,
'Boston' :'BOS'	 ,
'Charlotte' :'CHA'	 ,
'Chicago' :'CHI'	 ,
'Cleveland' :'CLE'	 ,
'Dallas' :'DAL'	 ,
'Denver' :'DEN'	 ,
'Detroit' :'DET'	 ,
'Golden State' :'GS'	 ,
'Houston' :'HOU'	 ,
'Indiana' :'IND'	 ,
'L.A. Clippers' :'LAC'	 ,
'L.A. Lakers' :'LAL'	 ,
'Memphis' :'MEM'	 ,
'Miami' :'MIA'	 ,
'Milwaukee' :'MIL'	 ,
'Minnesota' :'MIN'	 ,
'New Orleans' :'NO'	 ,
'New York' :'NY'	 ,
'Oklahoma City' :'OKC'	 ,
'Orlando' :'ORL'	 ,
'Philadelphia' :'PHI'	 ,
'Phoenix' :'PHO'	 ,
'Portland' :'POR'	 ,
'Sacramento' :'SAC'	 ,
'San Antonio' :'SA'	 ,
'Toronto' :'TOR'	 ,
'Utah' :'UTA'	 ,
'Washington'   :'WAS'	  
} 
import pandas as pd
import time
import calendar
import datetime


def clean_teams():
	team_map = {v: k for k, v in city_dict.iteritems()}

	sched=pd.read_csv('../../Data/schedule.csv')
	proj=pd.read_csv('../../Projections/Projections.csv')
	abbr_to_num = {name: num for num, name in enumerate(calendar.month_abbr) if num}
	for idx, row in sched.iterrows():
		v_team=row.VISITOR
		h_team=row.HOME.strip('**')
		v_team=city_dict[v_team]
		h_team=city_dict[h_team]
		sched.set_value(idx, 'VISITOR', v_team)
		sched.set_value(idx, 'HOME', h_team)
		date=row.DATE.split('-')
		if date[2]=='16':
			date[2]=2016
		else:
			date[2]=2017
		date[1]=abbr_to_num[date[1]]
		date[0]=int(date[0])
		print date
		new_date=datetime.date(date[2], date[1], date[0]).isoformat()
		sched.set_value(idx, 'DATE', new_date)
	sched.to_csv('../../Data/schedule.csv', index=False)

clean_teams()
