from langchain_community.utilities import SQLDatabase
import os

DB_HOST=os.environ["DB_HOST"]
DB_PORT=os.environ["DB_PORT"]
DB_USER=os.environ["DB_USER"]
DB_PASSWORD=os.environ["DB_PASSWORD"]
DB_DATABASE=os.environ["DB_DATABASE"]


db = SQLDatabase.from_uri(f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_DATABASE}",sample_rows_in_table_info = 0)