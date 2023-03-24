import pandas as pd
from sqlalchemy import create_engine

usecols = ["Id", "TotalBsmtSF", "1stFlrSF", "2ndFlrSF", "TotRmsAbvGrd", "Neighborhood", "SalePrice"]
df = pd.read_csv("data/kaggle_housing_train.csv", usecols=usecols)

#housing = df[usecols]

#need to rename "1stFlrSF" and for sql table "2ndFlrSF",
#df2 = df.rename({'a': 'X', 'b': 'Y'}, axis=1)  # new method
#NOTE, had to use new rename method from here https://stackoverflow.com/questions/11346283/renaming-column-names-in-pandas 
# not old method from https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.rename.html

housing = df.rename({"1stFlrSF": "firstFlrSF", "2ndFlrSF": "secondFlrSF"}, axis=1)


#NOTE !! this needs to be done OUTSIDE of the files.  In a Shell command. 
# Run psql and create the database in postgress, then you will be able to access it in your files!! 
# Maybe add this to the README.md!!!! <--- The lists below replace manually setting up a postgres db

conn_string = 'postgresql://Sonya@localhost/housing'
engine = create_engine(conn_string)
conn = engine.connect()
housing.to_sql('housing', conn, if_exists = 'replace')
results = conn.execute('''select * from housing where "SalePrice" > 300000 limit 5''').fetchall()