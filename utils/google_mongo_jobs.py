from multiprocessing import process
import pandas as pd
import datetime as dt
import http.client
import json
import urllib.parse
import os
from pymongo import MongoClient
from concurrent.futures import ThreadPoolExecutor, as_completed

from dotenv import load_dotenv
load_dotenv()

mongodb_conn = os.getenv('MONGODB_CONNECTION_STRING')

# Global variables to keep track of searched job titles and cities
searched_jobs = set()
searched_cities = set()

def google_job_search(job_title, city_state, start=0):
    '''
    job_title(str): "Data Scientist", "Data Analyst"
    city_state(str): "Denver, CO"
    '''
    query = f"{job_title} {city_state}"
    params = {
        "api_key": os.getenv('WEBSCRAPING_API_KEY'),
        "engine": "google_jobs",
        "q": query,
        "hl": "en",
        "google_domain": "google.com",
        # "start": start,
        # "chips": f"date_posted:{post_age}",
    }

    query_string = urllib.parse.urlencode(params, quote_via=urllib.parse.quote)

    conn = http.client.HTTPSConnection("serpapi.webscrapingapi.com")
    try:
        conn.request("GET", f"/v1?{query_string}")
        print(f"GET /v1?{query_string}")
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
        return jobs_results
    except (KeyError, json.JSONDecodeError) as e:
        print(f"Error occurred for search: {job_title} in {city_state}")
        print(f"Error message: {str(e)}")
        print(f"Data: {data}")
        return None

def mongo_dump(jobs_results, collection_name):
    client = MongoClient(mongodb_conn)
    db = client.job_search_db
    collection = db[collection_name]
    
    for job in jobs_results:
        job['retrieve_date'] = dt.datetime.today().strftime('%Y-%m-%d')
        collection.insert_one(job)
    
    print(f"Dumped {len(jobs_results)} documents to MongoDB collection {collection_name}")

def process_batch(job, city_state, start=0):
    global searched_jobs, searched_cities

    # Check if the job title and city have already been searched
    if (job, city_state) in searched_jobs:
        print(f'Skipping already searched job: {job} in {city_state}')
        return

    jobs_results = google_job_search(job, city_state, start)
    if jobs_results is not None:
        print(f'City: {city_state} Job: {job} Start: {start}')
        mongo_dump(jobs_results, 'sf_bay_test_jobs')

        # Add the job title and city to the searched sets
        searched_jobs.add((job, city_state))
        searched_cities.add(city_state)

def main(job_list, city_state_list):
    for job in job_list:
        for city_state in city_state_list:
            output = process_batch(job, city_state)

if __name__ == "__main__":
    job_list = ["Data Scientist", "Machine Learning Engineer", "AI Gen Engineer", "ML Ops"]
    city_state_list = ["Atlanta, GA", "Austin, TX", "Boston, MA", "Chicago, IL", 
                    "Denver CO", "Dallas-Ft. Worth, TX", "Los Angeles, CA",
                    "New York City NY", "San Francisco, CA", "Seattle, WA",
                    "Palo Alto CA", "Mountain View CA", "San Jose, CA"]
    simple_city_state_list: list[str] = ["Palo Alto CA", "San Francisco CA", "Mountain View CA"]
    main(job_list, simple_city_state_list)