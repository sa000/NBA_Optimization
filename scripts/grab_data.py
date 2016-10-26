from urllib2 import urlopen
from lxml import etree
import csv
import requests
from bs4 import BeautifulSoup
import os
import pandas as pd
##Grab data
url='http://rotoguru1.com/cgi-bin/hyday.pl?mon=11&day=31&year=2015&game=dk&scsv=1'
months=[10,11,12,1,2,3,4 ]
days=[i+1 for i in range(31)]
years=[2015,2016]
#Oct 27-Apr 16
#months=[10,11 ]
#days=[i+1 for i in range(6)]

def grab_data():
	for index, month in enumerate(months):
		for day in days:
			filename="Month%dDay%d.csv"%(month, day)
			print "starting scraping for %s"%filename
			if index<3:
				year=years[0]
			else:
				year=years[1]

			url='http://rotoguru1.com/cgi-bin/hyday.pl?mon=%d&day=%d&year=%d&game=dk&scsv=1' %(month, day, year)
			tree = etree.HTML(urlopen(url).read())
			r=requests.get(url)
			soup = BeautifulSoup(r.text, 'lxml')
			t=soup.find_all('pre')[-1]
			t=t.text.strip()	
			if len(t)<100:
				print "NO games, skipping this day"	
			else:	
				target=open(filename, 'w')
				target.write(t)
				print "Writing data for mon%dday%d"%(month,day)
				target.close()
def merge():
	merge=[]
	files=os.listdir('data/')

	for file in files:
		print file
		if '.DS_Store' in file:
			pass
		df=pd.read_csv('data/%s'%file)
		merge.append(df)
	merged=pd.concat(merge)
	merged.to_csv('data.csv')


merge()


