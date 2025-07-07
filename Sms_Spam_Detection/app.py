import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder
import nltk
import pickle
dataset=pickle.load(open('sms.pkl', 'rb'))
print(dataset.head())
