import os
from dotenv import load_dotenv

load_dotenv()
#finds/loads the .env file

#conn_string = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/careers"
#conn_string = 'postgresql://Sonya@localhost/housing'
# DB_USER = 'Sonya'
# DB_HOST = 'localhost'
DB_USER = os.getenv('DB_USER')
DB_HOST = os.getenv('DB_HOST')
DB_NAME = os.getenv('DB_NAME')
