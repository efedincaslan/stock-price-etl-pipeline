import logging
from extract import extraction
from transform import transformation
from load import loading
from config import SYMBOLS


# Set up basic logging (more robust logging can be set up in core/logging_setup.py)
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def main():
    """
    Main entry point for the ETL pipeline.
    Orchestrates the extract, transform, and load process.
    """
    logging.info("ETL pipeline started.")
    try:
        for symbol in SYMBOLS:

            # 1. Extract
            raw_data = extraction(symbol)
            logging.info(f"Data extracted successfully")

            # 2. Transform
            transformed_data = transformation(raw_data)
            logging.info(f"Data transformed successfully. Rows: {len(transformed_data)}")

            # 3. Load
            loading(transformed_data)
            logging.info("Data loaded successfully.")

    except Exception as e:
        logging.error(f"An error occurred during the ETL process: {e}")
        # Additional error notification logic could go here

    logging.info("ETL pipeline finished.")

if __name__ == "__main__":
    main()
