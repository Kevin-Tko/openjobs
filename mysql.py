import os
from dotenv import load_dotenv
import time
from scraping import scraping
from sqlalchemy import create_engine, DATE, VARCHAR

load_dotenv()
host = os.getenv('HOST')
user = os.getenv('USER')
password = os.getenv('PASSWORD')
database = os.getenv('DATABASE')
port = 3306


def writing_to_db():
    dbcon = None
    while not dbcon:
        try:
            engine = create_engine(f"mysql+pymysql://{user}:{password}@{host}/{database}?charset=utf8mb4")
            dbcon = engine.connect()
            print('DB Connected')
        except Exception as e:
            print(f'Error connecting {e}')
            time.sleep(3)

    bank_jobs = scraping()

    data_type = {'DATE': DATE(), 'JOB_TITLE': VARCHAR(1000), 'JOB_LINK': VARCHAR(1000)}
    try:
        bank_jobs.to_sql(name='jobs',
                         con=dbcon,
                         if_exists='replace')
        print('Data successfully written to SQL')
    except Exception as e:
        print(f'Error writting to SQL: {e}')
