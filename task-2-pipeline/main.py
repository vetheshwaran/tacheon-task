import os
import logging
import requests
import pandas as pd
from datetime import datetime
from dotenv import load_dotenv
from google.cloud import bigquery

load_dotenv()

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    )

API_KEY=os.getenv('NEWS_API_KEY')
GCP_PROJECT_ID=os.getenv('GCP_PROJECT_ID')
DATASET_ID='news_dataset'