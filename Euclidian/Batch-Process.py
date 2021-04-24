#import pandas for results
import pandas as pd
from datetime import datetime
import os

# Setup logging
import logging
logging.basicConfig(filename='batch.log', level= logging.ERROR)

# import Crystalball
from cb import Crystalball as cb

path = os.getcwd()
inputfile = "Inbox/cpf.csv" 
outputfile = "/Outbox/batch.csv" 
METHOD = 'arima'




if os.path.exists(inputfile):
    dfcpf = pd.read_csv(path + "/" + inputfile)
    for i, r in dfcpf.iterrows():
        df = cb.get_history(str(r['cpf']))
        if df.empty:
            logging.error( "BATCH: " + "Cpf not Found: " + str(r['cpf']))
            continue
        shoplist = cb.forecast(df,'arima', str(r['date']))
        shoplist['date'] = str(r['date'])
        shoplist['cpf'] = str(r['cpf'])
        shoplist.to_csv(path+outputfile, mode='a', header=False)

else:
    print(False)
