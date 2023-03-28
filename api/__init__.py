from flask import Flask
#from sqlalchemy import create_engine
import pandas as pd
from api.models.property import Property
import json
import psycopg2

from settings import DB_USER, DB_HOST, DB_NAME

# def create_app(db_user,db_host,db_name):
def create_app():
    app = Flask(__name__)

    # This is keyword mapping. I don't think it's needed if you use the 
    # postgres string/url instead
    # app.config.from_mapping(
    #     DB_USER = DB_USER,
    #     DB_HOST = DB_HOST,
    #     DB_NAME = DB_NAME,
    #     # DB_USER=db_user,
    #     # DB_HOST=db_host,
    #     # DB_NAME=db_name
    # )
    
    def get_df() -> pd.DataFrame:
        """read the csv dataset and return a dataframe"""
        usecols = ["Id", "Neighborhood", "TotalBsmtSF", "1stFlrSF", "2ndFlrSF", "TotRmsAbvGrd",  "SalePrice"]
        df = pd.read_csv("data/kaggle_housing_train.csv", usecols=usecols, index_col="Id")

        #housing = df[usecols]

        #need to rename "1stFlrSF" and for sql table "2ndFlrSF",
        #df2 = df.rename({'a': 'X', 'b': 'Y'}, axis=1)  # new method
        #NOTE, had to use new rename method from here https://stackoverflow.com/questions/11346283/renaming-column-names-in-pandas 
        # not old method from https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.rename.html
        
        housing = df.rename({"Id":"id", "1stFlrSF": "firstFlrSF", "2ndFlrSF": "secondFlrSF"}, axis=1)
        return housing.to_csv('data/corrected.csv', index=False)
        #return housing

        #NOTE !! this needs to be done OUTSIDE of the files.  In a Shell command. 
        # Run psql and create the database in postgress, then you will be able to access it in your files!! 
        # Maybe add this to the README.md!!!! <--- The lines below replace manually setting up a postgres db

    def build_conn():
        #housing = get_df()
        conn_string = f"postgresql://{DB_USER}@{DB_HOST}/{DB_NAME}"
        #conn_string = 'postgresql://Sonya@localhost/housing'
        conn = psycopg2.connect(conn_string)
        #engine = create_engine(conn_string)
        #conn = engine.connect()
        #housing.to_sql('housing', conn, if_exists = 'replace')
        #cursor = conn.cursor()
        return conn#, housing
    #sales_price_above_300k = conn.execute('''select * from housing where "SalePrice" > 300000 limit 5''').fetchall()

    def build_housing() -> None:
        conn = build_conn()
        housing = get_df()
        #housing.to_sql('housing', conn, if_exists = 'replace')

    #get_df() - ran this 1x to create the modified csv file
    #then created database in postgres
    #added table to postgres with 'psql -d housing -f migrations/create_tables.sql
    #then filled the table with this command in the pqsl shell:
    # \copy table (column, names, of, table) FROM '/full/path/to/csv-file.csv' DELIMITER ',' CSV HEADER; 
    # \copy housing (Neighborhood,TotalBsmtSF,firstFlrSF,secondFlrSF,TotRmsAbvGrd,SalePrice)
    #               FROM '/Users/Sonya/Documents/Jigsaw/flask-project-lab/data/corrected.csv' 
    #               DELIMITER ',' CSV HEADER;

    @app.route('/')
    def index():
        return "This is the Housing App"

    @app.route('/properties')
    def properties():
        conn = build_conn()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM housing LIMIT 5;')
        properties = cursor.fetchall()
        property_objs = [Property(property).__dict__ for property in properties]
        return json.dumps(property_objs, default=str ) #to fix decimal error in route
    
    @app.route('/properties/<id>')
    def show_property(id):
        conn = build_conn()
        cursor = conn.cursor()
        cursor.execute('''SELECT * FROM housing WHERE id = %s LIMIT 1;''', (id,))
        property = cursor.fetchone()
        prop_dict = Property(property).__dict__
        return json.dumps(prop_dict, default=str ) #to fix decimal error in route

    return app
        
