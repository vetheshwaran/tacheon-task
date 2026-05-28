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
    format="%(asctime)s [%(levelname)s] %(message)s"
)


API_KEY      = os.getenv("NEWS_API_KEY")
PROJECT_ID   = os.getenv("GCP_PROJECT_ID")
DATASET      = "news_pipeline"
TABLE        = "top_headlines"
QUERY        = "marketing"   # topic to search
PAGE_SIZE    = 20            # max articles to fetch


# ──────────────────────────────────────────────
# STEP 1: Fetch
# ──────────────────────────────────────────────
def fetch_news(query=QUERY, page_size=PAGE_SIZE):
    """
    Fetches top headlines from NewsAPI.
    Returns raw JSON or None if it fails.
    """
    logging.info(f"Fetching news for topic: '{query}'")

    url = "https://newsapi.org/v2/everything"
    params = {
        "q":        query,
        "pageSize": page_size,
        "language": "en",
        "sortBy":   "publishedAt",
        "apiKey":   API_KEY
    }

    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()

        if data.get("status") != "ok":
            logging.error(f"API returned error: {data.get('message')}")
            return None

        logging.info(f"Fetched {len(data['articles'])} articles")
        return data

    except requests.exceptions.Timeout:
        logging.error("Request timed out. API may be slow.")
        return None

    except requests.exceptions.ConnectionError:
        logging.error("Connection failed. Check internet connection.")
        return None

    except requests.exceptions.HTTPError as e:
        logging.error(f"HTTP error: {e}")
        return None

    except Exception as e:
        logging.error(f"Unexpected error during fetch: {e}")
        return None


# ──────────────────────────────────────────────
# STEP 2: Transform
# ──────────────────────────────────────────────
def transform_data(raw_data):
    """
    Flattens raw API response into a clean table.
    Adds derived fields for analytical value.
    """
    logging.info("Transforming data...")

    articles = raw_data.get("articles", [])

    if not articles:
        logging.warning("No articles found in response.")
        return None

    rows = []
    for article in articles:
        rows.append({
            "source_name":    article.get("source", {}).get("name"),
            "author":         article.get("author"),
            "title":          article.get("title"),
            "description":    article.get("description"),
            "url":            article.get("url"),
            "published_at":   article.get("publishedAt"),
            "content":        article.get("content"),
        })

    df = pd.DataFrame(rows)

   
    df["author"]      = df["author"].fillna("Unknown")
    df["description"] = df["description"].fillna("")
    df["source_name"] = df["source_name"].fillna("Unknown")
    df["content"]     = df["content"].fillna("")

  
    df["published_at"] = pd.to_datetime(
        df["published_at"], errors="coerce", utc=True
    )

    
    df = df.dropna(subset=["published_at"])

    # ── Derived fields (analytical value) ─────

    # 1. title_word_count — longer titles may
    #    indicate more detailed reporting
    df["title_word_count"] = df["title"].apply(
        lambda x: len(str(x).split()) if x else 0
    )

    # 2. has_description — quick quality flag
    df["has_description"] = df["description"].apply(
        lambda x: len(str(x).strip()) > 0
    )

    # 3. published_date — date only, for grouping
    df["published_date"] = df["published_at"].dt.date

    # 4. hour_of_day — to spot publishing patterns
    df["hour_of_day"] = df["published_at"].dt.hour

    # 5. fetched_at — when pipeline ran
    df["fetched_at"] = datetime.now(timezone.utc)

    # 6. search_topic — what query was used
    df["search_topic"] = QUERY

    logging.info(f"Transformed {len(df)} rows successfully")
    return df


# ──────────────────────────────────────────────
# STEP 3: Load to BigQuery
# ──────────────────────────────────────────────
def load_to_bigquery(df):
    """
    Loads transformed DataFrame into BigQuery.
    Creates dataset/table if they don't exist.
    """
    logging.info("Connecting to BigQuery...")

    client = bigquery.Client(project=PROJECT_ID)
    table_id = f"{PROJECT_ID}.{DATASET}.{TABLE}"

    # Create dataset if it doesn't exist
    dataset_ref = bigquery.Dataset(
        f"{PROJECT_ID}.{DATASET}"
    )
    dataset_ref.location = "US"

    try:
        client.create_dataset(dataset_ref, exists_ok=True)
        logging.info(f"Dataset '{DATASET}' ready")
    except Exception as e:
        logging.error(f"Failed to create dataset: {e}")
        return

    # Define schema explicitly
    schema = [
        bigquery.SchemaField("source_name",     "STRING"),
        bigquery.SchemaField("author",           "STRING"),
        bigquery.SchemaField("title",            "STRING"),
        bigquery.SchemaField("description",      "STRING"),
        bigquery.SchemaField("url",              "STRING"),
        bigquery.SchemaField("published_at",     "TIMESTAMP"),
        bigquery.SchemaField("content",          "STRING"),
        bigquery.SchemaField("title_word_count", "INTEGER"),
        bigquery.SchemaField("has_description",  "BOOL"),
        bigquery.SchemaField("published_date",   "DATE"),
        bigquery.SchemaField("hour_of_day",      "INTEGER"),
        bigquery.SchemaField("fetched_at",       "TIMESTAMP"),
        bigquery.SchemaField("search_topic",     "STRING"),
    ]

    job_config = bigquery.LoadJobConfig(
        schema=schema,
        write_disposition="WRITE_APPEND",
    )

    try:
        job = client.load_table_from_dataframe(
            df, table_id, job_config=job_config
        )
        job.result()
        logging.info(
            f"Loaded {len(df)} rows into {table_id}"
        )
    except Exception as e:
        logging.error(f"Failed to load to BigQuery: {e}")


# ──────────────────────────────────────────────
# MAIN
# ──────────────────────────────────────────────
def run_pipeline():
    logging.info("=== Pipeline started ===")

    # Step 1: Fetch
    raw_data = fetch_news(query=QUERY, page_size=PAGE_SIZE)
    if not raw_data:
        logging.error("Pipeline stopped: fetch failed")
        return

    # Step 2: Transform
    df = transform_data(raw_data)
    if df is None or df.empty:
        logging.error("Pipeline stopped: transform failed")
        return

    # Step 3: Load
    load_to_bigquery(df)

    logging.info("=== Pipeline completed ===")


if __name__ == "__main__":
    run_pipeline()