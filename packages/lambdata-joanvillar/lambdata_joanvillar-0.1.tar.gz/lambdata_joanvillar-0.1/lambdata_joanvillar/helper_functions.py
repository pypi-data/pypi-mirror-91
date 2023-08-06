"""helper functions"""

import pandas as pd 

class myDataFrameHe(pd.DataFrame):
  def split_dates(self):
    newdf = []
    for x in range(len(self)):
      data_date = str(self.values[x]).strip('[\'').strip('\']').split('/')
      newdf.append(data_date)
    add_data = pd.DataFrame(data=newdf,columns=['Month', 'Day', 'Year'])
    new_df = pd.concat([self,add_data], axis=1)
    return new_df

  def null_count(self):
    cnt = self.isnull().sum().sum()
    return cnt
  
def train_test_split(df, frac):
  train = df.sample(n=int(len(df)*frac))
  test = df.drop(index=train.index)
  return train,test


