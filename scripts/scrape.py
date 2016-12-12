import requests
from lxml import html 
import os
import pandas as pd


def rename(start_id, end_id):
	dates={}
	for id in xrange(start_id, end_id):
		url='https://www.fantasysportsco.com/Projections/Sport/NBA/Site/DraftKings/PID/%d' % id
		page=requests.get(url)
		data=html.fromstring(page.content)
		date=data.xpath('//*[@id="dnn_ctr749_ModuleContent"]/div/div/div[1]/div/span')[0].text.strip('\n').strip(' ')
		date=date.strip('\n')
		date=date.replace(',','')
		date=date.replace(' ','')
		dates[id]=date
		print 'FInished date%d_%s' %(id,dates[id])
	print 'dates complete'
	projections=os.listdir('../Projections')
	for proj in projections:
		print proj
		if proj == '.DS_Store' or 'projection' in proj:
			continue
		proj_id=int(proj[-7:-4])
		print proj_id, dates[proj_id]
		filename='projection_%s.csv' % dates[proj_id]
		os.rename('../Projections/%s' % proj, '../Projections/%s'%filename)
	print 'rename complete'




#rename(411, 457)

def merge():
	projections=os.listdir('../Projections')
	df_list=[]
	for proj in projections:
		if proj=='.DS_Store':
			continue
		df=pd.read_csv('../Projections/%s'%proj)
		df_list.append(df)
	full_df=pd.concat(df_list)

	full_df.to_csv('Final.csv', index=False)

	print 'merge complete'
merge()
