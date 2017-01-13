import requests
from lxml import html 
import os
import pandas as pd

import numpy as np
import csv

def clean_roster():
	target=open('roster.csv','w')
	csvwriter=csv.writer(target)
	csvwriter.writerow(['Name', 'Position'])
	data=pd.read_csv('rawroster.csv')
	for idx, row in data.iterrows():
		print row
		if row[0] == 'NAME' or len(row[0])==1:
			if isinstance(row[1], basestring):
				if row[1]!='TEAM':
					pos=row[1]
		else:
			name=row[0]
			name=' '.join(reversed(name.replace(' ','').split(',')))
			print name, pos
			csvwriter.writerow([name, pos.upper()])

	target.close()
clean_roster()
		