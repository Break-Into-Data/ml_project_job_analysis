import pandas as pd
import datetime as dt
import http.client
import json
import urllib.parse
import os
from sqlalchemy import create_engine
from concurrent.futures import ThreadPoolExecutor, as_completed
from dotenv import load_dotenv
load_dotenv()


def google_job_search(job_title, city_state, start=0):
    '''
    job_title(str): "Data Scientist", "Data Analyst"
    city_state(str): "Denver, CO"
    post_age,(str)(optional): "3day", "week", "month"
    '''
    query = f"{job_title} {city_state}"
    params = {
        "api_key": os.getenv('SerpAPIkey'),
        "engine": "google_jobs",
        "q": query,
        "hl": "en",
        "start": start,
        # "chips": f"date_posted:{post_age}",
    }

    query_string = urllib.parse.urlencode(params, quote_via=urllib.parse.quote)

    conn = http.client.HTTPSConnection("serpapi.webscrapingapi.com")
    try:
        conn.request("GET", f"/v1?{query_string}")
        res = conn.getresponse()
        try:
            data = res.read()
        finally:
            res.close()
    finally:
        conn.close()

    try:
        json_data = json.loads(data.decode("utf-8"))
        jobs_results = json_data['google_jobs_results']
        job_columns = ['title', 'company_name', 'location', 'description', 'extensions', 'job_id']
        df = pd.DataFrame(jobs_results, columns=job_columns)
        return df
    except (KeyError, json.JSONDecodeError) as e:
        print(f"Error occurred for search: {job_title} in {city_state}")
        print(f"Error message: {str(e)}")
        return None

def sql_dump(df, table):
    engine = create_engine(f"postgresql://{os.getenv('MasterName')}:{os.getenv('MasterPass')}@{os.getenv('RDS_EndPoint')}:5432/postgres")
    with engine.connect() as conn:
        df.to_sql(table, conn, if_exists='append', chunksize=20, method='multi', index=False)
        print(f"Dumped {df.shape} to SQL table {table}")

def process_batch(job, city_state, start):
    df_10jobs = google_job_search(job, city_state, start)
    if df_10jobs is not None:
        print(f'City: {city_state} Job: {job} Start: {start}')
        print(df_10jobs.shape)
        date = dt.datetime.today().strftime('%Y-%m-%d')
        df_10jobs['retrieve_date'] = date
        df_10jobs.drop_duplicates(subset=['job_id', 'company_name'], inplace=True)
        rows_affected = sql_dump(df_10jobs, 'usajobstest')
        print(f"Rows affected: {rows_affected}")

def main(job_list, city_state_list):
    with ThreadPoolExecutor() as executor:
        futures = []
        for job in job_list:
            for city_state in city_state_list:
                for start in range(0, 1):
                    future = executor.submit(process_batch, job, city_state, start)
                    futures.append(future)

        for future in as_completed(futures):
            future.result()

if __name__ == "__main__":
    job_list = ["Data Scientist", "Machine Learning Engineer", "AI Gen Engineer",
                "Data Analyst", "Data Engineer", "Business Intelligence Analyst"]
    city_state_list = ["Atlanta, GA", "Austin, TX", "Boston, MA", "Chicago, IL", 
                    "Denver CO", "Dallas-Ft. Worth, TX", "Los Angeles, CA",
                    "New York City NY", "San Francisco, CA", "Seattle, WA",
                    "Palo Alto CA", "Mountain View CA"]
    simple_city_state_list: list[str] = ["Palo Alto CA", "San Francisco CA", ]
    main(job_list, city_state_list)