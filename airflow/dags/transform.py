from extract import extraction
import pandas as pd
import logging
from config import SYMBOLS

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')



def transformation(data):
    try:
        


        metadata = data.get('Meta Data')

        symbol = metadata.get('2. Symbol')

        time_series = data.get('Time Series (Daily)')


        df = pd.DataFrame.from_dict(time_series, orient='index')
        

        df_reset = df.reset_index()

        df_reset['symbol'] = symbol



        df_renamed = df_reset.rename(columns={
            'index' : 'date',
            '1. open' : 'open',
            '2. high' : 'high',
            '3. low' : 'low',
            '4. close' : 'close',
            '5. volume' : 'volume'
        })


        df_renamed['date'] = pd.to_datetime(df_renamed['date'])
        float_cols = ['open', 'high', 'low', 'close', 'volume']
        df_renamed[float_cols] = df_renamed[float_cols].astype(float)
        df_renamed['volume'] = df_renamed['volume'].astype(int)

        sorted_df = df_renamed.sort_values(by='date')

        logging.info('Succesful transformation')
        return sorted_df
        
    except Exception as e:
        logging.error(f'Unsuccesful transformation {e}')



if __name__=="__main__":
    for symbol in SYMBOLS:
        data = extraction(symbol)
        print(transformation(data))