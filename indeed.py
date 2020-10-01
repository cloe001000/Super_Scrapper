import requests
from bs4 import BeautifulSoup

LIMIT = 50
URL = f"https://www.indeed.com/jobs?q=python&limit={LIMIT}&radius=25"

def get_last_pages():
  result = requests.get(URL)
  soup = BeautifulSoup(result.text, "html.parser")

  pagination = soup.find("div", {"class":"pagination"})

  links = pagination.find_all('a')

  pages = []

  for link in links[:-1] :
    pages.append(int(link.string))

  max_page =  pages[-1]
  return max_page

def extrct_job(html):
  title = html.find("h2",{"class":"title"}).find("a")["title"]
  company = html.find("span",{"class":"company"})
  if company:
    company_ancher = company.find('a')
    if company_ancher is not None:
      company = str(company_ancher.string).strip()
    else:
      company = str(company.string).strip()
  else:
    company = None
  location = html.find("div",{"class","recJobLoc"})["data-rc-loc"]
  job_id = html["data-jk"]
  
  return {'title':title,'company':company,'location ':location,"link":f"https://www.indeed.com/viewjob?jk={job_id}&tk=1eje0fr2h305p000&from=serp&vjs=3" }

def extrct_indeed_job(last_page):
  jobs = []
  for page in range(last_page):
    print(f"indeed의 {page}번째 페이지를 스크레핑 합니다.")
    result = requests.get(f"{URL}&start={page*LIMIT}")
    soup = BeautifulSoup(result.text, "html.parser")
    results = soup.find_all("div", {"class":"jobsearch-SerpJobCard"})
    for result in results :
      job = extrct_job(result)
      jobs.append(job)
  return jobs

def get_jobs():
  last_page = get_last_pages()
  jobs = extrct_indeed_job(last_page)
  return jobs
