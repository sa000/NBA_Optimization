from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from lxml import html 
import requests
from bs4 import BeautifulSoup
import pandas as pd
import csv

def get_transactions():
	projections=pd.read_csv('../Projections/Projections.csv')
	headers=['Name', 'Team', 'Position', 'Dropped', 'Added', 'Total', 'Date']
	target=open('../Projections/transactions.csv', 'w')
	csvwriter=csv.writer(target)
	csvwriter.writerow(headers)
	dates=projections.Date.unique()
	for date in dates:
		print date
		url='https://basketball.fantasysports.yahoo.com/nba/buzzindex?sort=BI_S&src=combined&bimtab=A&pos=ALL&date=%s' %(date)
		print url
		req=requests.get(url)
		soup=BeautifulSoup(req.text,"lxml")
		table=soup.find("table", "Tst-table Table")
		for row in table.findAll('tr')[1:]:
			player=row.findAll('td')
			for entry in player[0].findAll(text=True):
				name=player[0].findAll(text=True)[6]
				team=player[0].findAll(text=True)[8].split('-')[0].upper()
				pos=player[0].findAll(text=True)[8].split('-')[1].upper()
			data=[name, team, pos, player[1].text, player[2].text, player[4].text, date]
			csvwriter.writerow(data)
	target.close()

def extend_name():
	projections=pd.read_csv('../Projections/Projections.csv')
	transactions=pd.read_csv('../Projections/transactions.csv')
	for index, row in transactions.iterrows():
		print row
# get_transactions()
extend_name()