import pandas as pd
from bs4 import BeautifulSoup
from datetime import datetime
import requests

# find current year for use later
year = datetime.now().year

# Empty lists to append the date, job title and link to the job
dates = []
text = []
links = []
jobs_df = None

def scraping():
    # Looping through 10 pages of myjobmag
    for i in range(1, 11):
        try:
            URL = f'https://www.myjobmag.co.ke/search/jobs?field=Banking&currentpage={i}'
            response = requests.get(URL)
            content = response.text
            soup = BeautifulSoup(content, 'html5lib')

            # Extracting links and job titles
            h2_list = soup.find_all('h2')
            for h2 in h2_list:
                atags_list = h2.find_all('a')
                for tag in atags_list:
                    text.append(tag.text)
                    links.append(f"https://www.myjobmag.co.ke{tag.get('href')}")

            # Extracting date of posting
            job_dates = soup.find_all('li', id='job-date')
            for date in job_dates:
                dates.append(f'{date.text} {year}')
        except Exception as e:
            print(f'Scraping failed due to :{e}')

    diction = {'DATE': dates,
               'JOB_TITLE': text,
               'JOB_LINK': links}

    jobs_df = pd.DataFrame(data=diction)

    jobs_df['DATE'] = jobs_df['DATE'].astype('str').str.strip().str.replace(' ', '/').astype('datetime64[ns]')

    return jobs_df