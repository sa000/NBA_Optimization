from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from lxml import html 
import requests
from bs4 import BeautifulSoup
import pandas as pd
import csv

def get_transactions():
	projections=pd.read_csv('../Projections/Projections.csv')
	headers=['Name', 'Dropped', 'Added', 'Total', 'Date']
	target=open('../Projections/transactions.csv', 'w')
	csvwriter=csv.writer(target)
	csvwriter.writerow(headers)
	dates=projections.Date.unique()
	for date in dates[0:1]:
		print date
		url='https://basketball.fantasysports.yahoo.com/nba/buzzindex?sort=BI_S&src=combined&bimtab=A&pos=ALL&date=%s' %(date)
		print url
		req=requests.get(url)
		soup=BeautifulSoup(req.text,"lxml")
		table=soup.find("table", "Tst-table Table")
		for row in table.findAll('tr')[1:]:
			player=row.findAll('td')
			for link in player[0].findAll('a', href=True):
				if 'news' not in link['href'] and 'players' in link['href']:
					p_url=link['href']
					print p_url
					p_page=requests.get(p_url)
					p_soup=BeautifulSoup(p_page.text,"lxml")
					name=p_soup.h1.text
			data=[name, player[1].text, player[2].text, player[4].text, date]
			csvwriter.writerow(data)
	target.close()
get_transactions()