import pandas as pd
import numpy as np
from db import dataForML
from pmdarima.arima import auto_arima
import pickle as pkl

def trainAndSaveModel():
    expenses = dataForML()
    if expenses == []:
        return
    expensesDF = pd.DataFrame(expenses)
    model = auto_arima(expensesDF)
    pkl.dump(model, open('model.pkl', 'wb'))

trainAndSaveModel()