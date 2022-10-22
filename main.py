from bs4 import BeautifulSoup
import requests

# Initializing variables
jobs = []
job_links = []
tokens = []
job_titles = []
job_overviews = []
job_responsibilities = []
job_basic_qualifications = []
job_preferred_qualifications = []

htmltext = requests.get('https://boards.greenhouse.io/embed/job_board?for=coursera').text  # Get html text
soup = BeautifulSoup(htmltext, 'html.parser')
link_text = soup.findAll('a')  # List of all html text with links

# Fill lists of gh_jid tokens and direct links to the job page
for link in link_text:
    gh_jid = link.get('href')
    token = gh_jid.find('=')
    gh_jid = gh_jid[token:]
    job_links.append(link.get('href'))
    tokens.append(gh_jid)

# Fill lists with related job information
for i in range(len(job_links)):
    # Create a link to a greenhouse.io page with a Coursera job posting
    job_url = 'https://boards.greenhouse.io/embed/job_app?for=coursera&token' + tokens[i]
    job_text = requests.get(job_url).text
    job_soup = BeautifulSoup(job_text, 'html.parser')
    job_titles.append(job_soup.find('h1', class_='app-title').text)
    job_overviews.append(job_soup.find('span', style='font-weight: 400;').text)
    # Create a list of all unordered lists
    lists = job_soup.findAll('ul')
    # Index necessary unordered lists and change it to text
    responsibilities = lists[0].text
    basic_qualifications = lists[1].text
    preferred_qualifications = lists[2].text
    job_responsibilities.append(responsibilities)
    job_basic_qualifications.append(basic_qualifications)
    job_preferred_qualifications.append(preferred_qualifications)

for i in range(len(job_links)):
    # List of related job info
    job_info = [job_links[i], job_titles[i], job_overviews[i], job_responsibilities[i], job_basic_qualifications[i],
                job_preferred_qualifications[i]]
    # List of lists where each element holds a list of related job information
    jobs.append(job_info)

# Prints out list of all jobs and their corresponding information
# for i in jobs:
#    for j in i:
#        print(j)
