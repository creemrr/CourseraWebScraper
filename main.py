from bs4 import BeautifulSoup
import requests
from pprint import pprint

# Initializing variables
jobs = []

htmltext = requests.get('https://boards.greenhouse.io/embed/job_board?for=coursera', timeout=60).text  # Get html text
soup = BeautifulSoup(htmltext, 'html.parser')
link_text = soup.findAll('a')  # List of all html text with links

# Fill lists of gh_jid tokens and direct links to the job page
for link in link_text:
    gh_jid = link.get('href')
    token = gh_jid.find('=')
    gh_jid = gh_jid[token:]
    # Create a link to a greenhouse.io page with a Coursera job posting
    job_url = f'https://boards.greenhouse.io/embed/job_app?for=coursera&token{gh_jid}'
    job_text = requests.get(job_url).text
    job_soup = BeautifulSoup(job_text, 'html.parser')
    # Create a list of all unordered lists
    lists = job_soup.findAll('ul')
    job_info = {'Link': link.get('href'),
                'Title': job_soup.find('h1', class_='app-title').text,
                'Overview': job_soup.find('span', style='font-weight: 400;').text,
                'Responsibilities': lists[0].text,  # First unordered list on Coursera posting is responsibilities
                'Basic Qualifications': lists[1].text,  # Second unordered list on Coursera posting is basic quals
                'Preferred Qualifications': lists[2].text}  # Third unordered list on Coursera posting is pref quals
    jobs.append(job_info)

# Prints out list of all jobs and their corresponding information
pprint(jobs)
