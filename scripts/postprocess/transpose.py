
import pandas as pd
import csv
def tranpose():
	filename='predictions_withSalary.csv'
	target=open(filename, 'wb')
	csvwriter=csv.writer(target)
	headers=['Date', 'Player', 'Pos', 'Salary', 'Predicted', 'Scored']
	csvwriter.writerow(headers)
	perfect=pd.read_csv('../../Data/Cumulative_Predictions_Perfect.csv')
	for idx, row in perfect.iterrows():
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
			entry=[row.date, name, pos, salary, round(project,2), scored]
			csvwriter.writerow(entry)
	target.close()
tranpose()