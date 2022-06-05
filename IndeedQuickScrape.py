import requests
from bs4 import BeautifulSoup
import pandas as pd

def extract(page):
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.67 Safari/537.36'}
    url = f'https://www.indeed.com/jobs?q=&l=Chicago%2C+IL&fromage=7&radius=0&start={page}'
    r = requests.get(url, headers)
    soup = BeautifulSoup(r.content, 'html.parser')
    return soup

def transform(soup):
    divs = soup.find_all('div', class_ = 'job_seen_beacon')
    for item in divs:
        title = item.find('a').text.strip()
        job_url = item.find(class_='jobTitle').a['href']
        company = item.find('span', class_ ='companyName').text.strip()
        location = item.find('div', class_ ='companyLocation').text.strip()
        try:
            salary = item.find('div', class_ = 'attribute_snippet').text.strip()
        except:
            salary = ''
        try:
            jobtype = item.find('div', class_ = ['metadata', 'aria-label', 'Salary']).text.strip()
        except:
            jobtype = ''
        summary = item.find('div', class_ = 'job-snippet').text.strip().replace('/n', '')

        job = {
            'title': title,
            'job_url': job_url,
            'company': company,
            'location': location,
            'salary': salary,
            'jobtype': jobtype,
            'summary': summary
        }
        joblist.append(job)
    return

joblist = [] 

for i in range(0,200,10):
    print(f'Getting page, {i}')
    c = extract(0)
    transform(c)

df = pd.DataFrame(joblist)
print(df.head())
df.to_csv('IndeedQuickScrapeJobsOutput.csv')