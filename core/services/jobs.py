import requests
from decouple import config

BASE_URL = "https://jobs.indianapi.in/jobs"

def fetch_jobs(title=None, location=None, company=None, experience=None, job_type=None, limit=20):
    # Prepare parameters - only include non-None values
    params = {
        "limit": str(limit)  # API expects string
    }
    
    # Only add parameters that are provided
    if title:
        params['title'] = title
    if location:
        params['location'] = location
    if company:
        params['company'] = company
    if experience:
        params['experience'] = experience
    if job_type:
        params['job_type'] = job_type
    
    # Prepare headers with API key
    headers = {}
    api_key = config('INDIAAPI_JOBS_KEY', default=None)
    if api_key:
        headers['X-Api-Key'] = api_key
    else:
        print("⚠️ Warning: No API key found. Set INDIAAPI_JOBS_KEY in your .env file")
        return {"error": "API key is required"}
    
    try:
        print(f"👉 Fetching jobs with params: {params}")  # DEBUG
        print(f"👉 Using headers: {{'X-Api-Key': '***'}}")  # DEBUG (hiding actual key)
        
        response = requests.get(BASE_URL, params=params, headers=headers, timeout=10)
        print(f"👉 Final URL: {response.url}")  # DEBUG
        print(f"👉 Response status: {response.status_code}")  # DEBUG
        
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f"Error fetching jobs: {e}")
        if hasattr(e, 'response') and e.response is not None:
            try:
                error_detail = e.response.json()
                print(f"Error details: {error_detail}")
                return {"error": str(e), "details": error_detail}
            except:
                print(f"Error response text: {e.response.text}")
                return {"error": str(e), "response_text": e.response.text}
        return {"error": str(e)}