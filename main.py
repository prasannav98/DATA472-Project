import requests
from bs4 import BeautifulSoup
import getLink
import os
url = 'https://www.msd.govt.nz/about-msd-and-our-work/publications-resources/statistics/benefit/index.html'
save_location = "/Users/prasannavenkatesh/Documents/DATA 472 Individual Project"
# Replace 'url' with the URL of the website you want to scrape
response = requests.get(url)
getLink.download_excel_files(url, save_location)
if response.status_code == 200:
    soup = BeautifulSoup(response.text, 'html.parser')
    # Find all <a> tags with href containing 'national-benefits-table'
    links = soup.find_all('a', href=lambda href: href and 'statistics/benefit/archive' in href)
    print(links)
        
links_list = [link['href'] for link in links]

print(links_list)
for link in links_list:
    full_url = "https://www.msd.govt.nz" + link
    getLink.download_excel_files(full_url,save_location)

