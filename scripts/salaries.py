from urllib2 import urlopen
from lxml import etree
import csv
import requests
from bs4 import BeautifulSoup
import os
import pandas as pd
##Grab data
url='http://rotoguru1.com/cgi-bin/hyday.pl?mon=11&day=31&year=2016&game=dk&scsv=1'
months=[10,11,12]
days=[i+1 for i in range(31)]
years=[2016]
#Oct 27-Apr 16
#months=[10,11 ]
#days=[i+1 for i in range(6)]
monthDict={1:'Jan', 2:'Feb', 3:'Mar', 4:'Apr', 5:'May', 6:'Jun', 7:'Jul', 8:'Aug', 9:'Sep', 10:'Oct', 11:'Nov', 12:'Dec'}

def grab_past_salaries():
	for index, month in enumerate(months):
		for day in days:
			past_files=os.listdir('../Data/Salaries')
			print month, day, 
			filename="%s_%d.csv"%(monthDict[month], day)
			if filename in past_files:
				print "Data already acquired for %s" %filename
				continue
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
				t=t.replace(',','')
				t.replace(';', ',')
				target.write(t)
				target.close()

				os.rename(filename, '../Data/Salaries/Past/%s'%filename)
def merge():
	merge=[]
	files=os.listdir('../Data/Salaries/Past')
	for file in files:
		print file
		if '.DS_Store' in file:
			continue
		df=pd.read_csv('../Data/Salaries/Past/%s'%file)

		merge.append(df)
	merged=pd.concat(merge)
	filename='Salaries_2016_2017.csv'
	merged.to_csv(filename, index=False)
	os.rename(filename, '../Data/Salaries%s'%filename)

def clean():
	filename='Salaries_2016_2017.csv'
	df=pd.read_csv('../Data/Salaries/%s'%filename, delimeter=';')
	for row in df.iterrows():
		end
#grab_past_salaries()
merge()


