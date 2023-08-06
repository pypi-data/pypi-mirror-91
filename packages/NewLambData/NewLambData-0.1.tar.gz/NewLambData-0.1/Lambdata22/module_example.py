"""Helper functions for DS use."""

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split


locationData = {
                'Cities': ['London', 'Tokyo', 'Dallas', 'Jakarta', 'Sydney'],
                'Address': ['123 England Street', '123 Japan ave', '123 Texas way', '123 Indonesia way','123 Roo court'],
                'Country': ['England', 'Japan', 'United States', 'Indonesia', 'Australia']
                }

df = pd.DataFrame(locationData)  

npArray = np.array([33,11,62,51,88,100,6782,99,800,554455])
numpy_df = pd.DataFrame(np.random.randn(1000,15))




def null_count(df):
    """Determines nulls within a pandas DF."""
    for cities in df:
        df['isNULL'] = (df.isnull().sum())

        return df['isNULL']

def TTS(X,y):
    """Creates a train, test, split from a pandas df"""
    X,y = np.arange(10).reshape((5,2)), range(10)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    return X_train, X_test, y_train, y_test

def randomize(df):
    """Creates a randomized version of the original
       inputed df."""  

    rando_df = df['Cities'].sample(n=3, random_state=42)

    return rando_df     






        





        



