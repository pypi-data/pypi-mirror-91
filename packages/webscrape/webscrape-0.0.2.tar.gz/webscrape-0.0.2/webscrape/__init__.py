import requests
from bs4 import BeautifulSoup

class Scrape:
  def __init__(self,url):
    self.url = url
  
  def get_links(self):
    #gets all links from webpage
    x = requests.get(self.url)
    soup = BeautifulSoup(x.text, 'html.parser')
    urls = []
    for link in soup.find_all('a'):
      url = link.get('href')
      if not url[0:7] == 'https://' or url[0:6] == 'http://':
        url = self.url+url
      urls.append(url)
    return urls