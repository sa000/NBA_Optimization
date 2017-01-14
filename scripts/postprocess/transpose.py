
import pandas as pd
import csv
def tranpose():
	filename='ProjectionsPerfect_PositionConstraints_tranpose.csv'
	target=open(filename, 'wb')
	csvwriter=csv.writer(target)
	headers=['Date', 'Player', 'Pos', 'Salary', 'Predicted', 'Scored', 'Team']
	csvwriter.writerow(headers)
	perfect=pd.read_csv('../../Data/ProjectionsPerfect_PositionConstraints.csv')
	for idx, row in perfect.iterrows():
		print idx
		date=row.date.replace('-', '')
		proj='projection_%s.csv'%date
		projection=pd.read_csv('../../Projections/past/%s' % proj)
		for i in xrange(8):
			player='Player%s'%str(i+1)
			data=projection[projection['Name']==row[player]]
			name=data.Name.values[0]
			salary=data.Salary.values[0]
			project=data.Projected.values[0]
			scored=data.Scored.values[0]
			pos=data.Position.values[0]
			team=data.Team.values[0]
			entry=[row.date, name, pos, salary, round(project,2), scored, team]
			csvwriter.writerow(entry)
	target.close()
tranpose()