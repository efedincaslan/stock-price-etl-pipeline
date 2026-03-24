import pandas as pd
from sqlalchemy import create_engine
from transform import transformation
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy import Table, MetaData
from dotenv import load_dotenv
import os
import logging
from config import SYMBOLS

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')


load_dotenv()


def loading(data):
    try:
        user = os.getenv('db_user')
        password = os.getenv('db_pass')

        engine = create_engine(f'postgresql://{user}:{password}@host.docker.internal:5432/IBM')

        meta = MetaData(schema='ibm_data')
        table = Table('stock_prices', meta, autoload_with=engine)

        
        rows = data.to_dict(orient='records')



        # Build the INSERT statement with the ON CONFLICT DO NOTHING clause
        stmt = insert(table).values(rows)
        stmt = stmt.on_conflict_do_nothing(index_elements=['date', 'symbol'])

        with engine.connect() as conn:
            conn.execute(stmt)
            conn.commit()

        logging.info('succesfully loaded')
    except Exception as e:
        logging.error(f'unsuccesful upload{e}')
        

if __name__=="__main__":
    from airflow.dags.extract import extraction
    for symbol in SYMBOLS:
        data = extraction(symbol)
        df = transformation(data)
        loading(df)
    