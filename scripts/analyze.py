import csv
import os
import pandas as pd
##Grab data
import numpy as np
from teams import teams_dict
def accuracy():
	df=pd.read_csv('../Projections/projections.csv')