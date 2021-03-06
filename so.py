import requests
from bs4 import BeautifulSoup

URL = f"https://stackoverflow.com/jobs?q=python&pg=2"


def get_last_page():
    result = requests.get(URL)
    soup = BeautifulSoup(result.text, "html.parser")
    pages = soup.find("div", {"class": "s-pagination"}).find_all("a")
    last_pages = pages[-2].get_text(strip=True)
    return int(last_pages)


def extract_job(html):
  title = html.find("a", {"class": "stretched-link"})["title"]
  company_row = html.find('h3', {'class': 'fs-body1'}).find_all('span')
  if company_row[0].string is None:
      company = "None"
  else:
      company = company_row[0].string.strip()
  location = company_row[1].string.strip()
  job_id = html['data-jobid']
  link = f"https://stackoverflow.com/jobs/{job_id}/"
  return{"title": title, "company": company, "location": location, "apply_link": link}


def extrect_jobs(last_page):
    jobs = []
    for page in range(last_page):
        print(f"스텍오버플로우 스크레핑중: {page}번째 페이지")
        result = requests.get(f"{URL}&pg={page + 1}")
        soup = BeautifulSoup(result.text, "html.parser")
        results = soup.find_all("div", {"class": "-job"})
        for result in results:
            job = extract_job(result)
            jobs.append(job)
    return jobs


def get_jobs():
    last_page = get_last_page()
    jobs = extrect_jobs(last_page)
    return jobs
