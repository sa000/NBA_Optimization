import requests
from lxml import html 
import os
import pandas as pd

import re 
import csv
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



def grab_DVP():
	positions=['PG', 'SG', 'SF', 'PF', 'C']
	for pos in positions:
		filename='DVP_%s.csv'%pos
		url='http://www.rotowire.com/daily/nba/defense-vspos.htm?site=DraftKings&pos=%s'%pos
		page=requests.get(url)
		data=html.fromstring(page.content)
		target=open(filename, 'w')
		csvwriter=csv.writer(target)
		header=['Team', 'Position', 'Season', 'Last 5', 'Last 10', 'PTS', 'REB', 'AST', 'STL', 'BLK', '3PM', 'FG%', 'FT%', 'TO']
		csvwriter.writerow(header)
		for i in xrange(1,31):
			path='/html/body/div[3]/div[7]/div/table/tbody/tr[%s]/td/text()' % str(i)
			row=data.xpath(path)
			csvwriter.writerow(row)
			print i
		print 'Data for %s Complete' %pos
		target.close()
		df=pd.read_csv(filename)
		df.sort(['Last 5'], ascending=False)
		df.to_csv(filename, index=False)
		os.rename(filename, '../Data/%s'%filename)
#merge()
#grab_DVP()

def grab_contests():
	dates=[]
	files=os.listdir('../Projections/past')[1:]
	for file in files:
		date=file.strip('projection_').strip('.csv')
		date=date[0:3]+'-'+date[3:-4]+'-'+date[-4:]
		dates.append(date)
	target=open('../Data/ContestResults.csv', 'w')
	csvwriter=csv.writer(target)
	headers=['Name', 'Entry Fee',  'Num of Entries', 'Top Prize', 'FPTS to Cash', 'Winner', 'FPTS to win', 'Total Entrees', 'Date']
	csvwriter.writerow(headers)

	for date in dates:
		url='http://www.dfsgold.com/nba/draftkings-daily-fantasy-recap-%s'%date
		page=requests.get(url)
		data=html.fromstring(page.content)
		num=len(data.xpath('//*[@id="MainContent_GridView3"]/tbody/tr'))
		for i in xrange(num):
			name=data.xpath('//*[@id="MainContent_GridView3"]/tbody/tr[%s]/td[1]/div[1]/text()'%str(i+1))
			row1=data.xpath('//*[@id="MainContent_GridView3"]/tbody/tr[%s]/td/text()'%str(i+1))
			row1[0]=name[0]
			row2=data.xpath('//*[@id="MainContent_GridView3"]/tbody/tr[%s]/td/a//text()'%str(i+1))
			info=row1+row2
			info.append(date)

			csvwriter.writerow(info)
			print date, i
	target.close()

grab_contests()
