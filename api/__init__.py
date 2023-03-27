from flask import Flask, jsonify
from sqlalchemy import create_engine
import pandas as pd
from api.models.property import Property
import json

def create_app():
    app = Flask(__name__)
    
    def get_df():
        usecols = ["Id", "Neighborhood", "TotalBsmtSF", "1stFlrSF", "2ndFlrSF", "TotRmsAbvGrd",  "SalePrice"]
        df = pd.read_csv("data/kaggle_housing_train.csv", usecols=usecols, index_col="Id")

        #housing = df[usecols]

        #need to rename "1stFlrSF" and for sql table "2ndFlrSF",
        #df2 = df.rename({'a': 'X', 'b': 'Y'}, axis=1)  # new method
        #NOTE, had to use new rename method from here https://stackoverflow.com/questions/11346283/renaming-column-names-in-pandas 
        # not old method from https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.rename.html

        housing = df.rename({"Id":"id", "1stFlrSF": "firstFlrSF", "2ndFlrSF": "secondFlrSF"}, axis=1)
        return housing


        #NOTE !! this needs to be done OUTSIDE of the files.  In a Shell command. 
        # Run psql and create the database in postgress, then you will be able to access it in your files!! 
        # Maybe add this to the README.md!!!! <--- The lines below replace manually setting up a postgres db

    #conn_string = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/careers"
    def build_conn():
        #housing = get_df()
        conn_string = 'postgresql://Sonya@localhost/housing'
        engine = create_engine(conn_string)
        conn = engine.connect()
        #housing.to_sql('housing', conn, if_exists = 'replace')
        #cursor = conn.cursor()
        return conn#, housing
    #sales_price_above_300k = conn.execute('''select * from housing where "SalePrice" > 300000 limit 5''').fetchall()

    def build_housing():
        conn = build_conn()
        housing = get_df()
        return housing.to_sql('housing', conn, if_exists = 'replace')



    @app.route('/')
    def index():
        return "This is the Housing App"

    @app.route('/properties')
    def properties():
        conn = build_conn()
        housing = build_housing()
        #breakpoint()

        sql_result = conn.execute('SELECT * FROM housing LIMIT 5;')
        properties = sql_result.fetchall()
        #breakpoint()
        property_objs = [Property(property).__dict__ for property in properties]
        # use the mass migrate lab to set up these objects...[Venue(venue).__dict__ for venue in venues]
        #return jsonify(property_objs)
        return json.dumps(property_objs, default=str ) #to fix decimal error in route
    
    #TODO fix this route!!!
    @app.route('/properties/<id>')
    def show_property(id):
        conn = build_conn()
        build_housing()
        #breakpoint()
        sql_result = conn.execute('''SELECT * FROM housing WHERE 'id' = %s Limit 1;''', (id,))
        property = sql_result.fetchone()
        prop_dict = Property(property).__dict__
        return json.dumps(prop_dict, default=str ) #to fix decimal error in route








    return app
        
