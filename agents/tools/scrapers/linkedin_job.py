import requests
from urllib3.util.retry import Retry
from src.models.job_posting import JobPosting
from requests.adapters import HTTPAdapter
import random
import time
import re
from bs4 import BeautifulSoup

def create_session_with_retries() -> requests.Session:
    """Create a session with retry strategy and rotating user agents"""
    session = requests.Session()
    
    # Configure retry strategy
    retries = Retry(
        total=5,  # number of retries
        backoff_factor=2,  # wait 1, 2, 4, 8, 16 seconds between retries
        status_forcelist=[429, 500, 502, 503, 504]  # retry on these status codes
    )
    
    session.mount('https://', HTTPAdapter(max_retries=retries))
    
    # Rotate between different user agents
    user_agents = [
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0'
    ]
    
    session.headers.update({
        'User-Agent': random.choice(user_agents),
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
    })
    
    return session

def scrape_job_posting(url: str) -> dict:
    """Scrapes the job posting with improved error handling and anti-bot detection
    
    Args:
        url (str): The URL of the job posting to scrape
        
    Returns:
        job_posting.JobPosting: A JobPosting object containing the job title, company name, company location, job description, and salary information
    """
    session = create_session_with_retries()
    # Add random delay before request
    time.sleep(random.uniform(1, 3))
    
    try:
        response = session.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")
        # Wrap element finding in try-except blocks to handle missing elements
        try:
            job_title = soup.find("h1", class_="topcard__title").text.strip()
            company_name = soup.find("a", class_="topcard__org-name-link topcard__flavor--black-link").text.strip()
            company_location = soup.find("span", class_="topcard__flavor topcard__flavor--bullet").text.strip()
            job_description = soup.find("div", class_="description__text description__text--rich").text.strip()
            job_description = job_description.replace("\n", " ")
        except AttributeError:
            job_title, company_name, company_location, job_description = None, None, None, None

        sentences = re.split(r'(?=[A-Z])', job_description)
        salary_keywords = ["$", "€", "£", "¥", "₹", "salary", "salaries"]
        salary_information = ', '.join([sentence for sentence in sentences if any(keyword in sentence.lower() for keyword in salary_keywords)])
        
        return JobPosting(job_title, company_name, company_location, job_description, salary_information).to_dict()
        
    except requests.exceptions.RequestException as e:
        print(f"Error fetching job posting: {e}")
        raise
    
if __name__ == "__main__":
    job_url = "https://www.linkedin.com/jobs/view/3766686044/"
    job_posting = scrape_job_posting(job_url)
    print(job_posting)