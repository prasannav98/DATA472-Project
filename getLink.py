import requests
from bs4 import BeautifulSoup
import os

def download_excel_files(url, save_location):
    # Replace 'url' with the URL of the website you want to scrape
    response = requests.get(url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        # Find all <a> tags with href containing 'national-benefits-table'
        links = soup.find_all('a', href=lambda href: href and 'national-benefit-tables' in href)
        print(links)
        
    links_list = [link['href'] for link in links]

    print(links_list)
    # Filter out only the links from the list


    # Loop through each link and download the associated file
    for link in links_list:
        # Construct the full URL
        full_url = "https://www.msd.govt.nz" + link
        
        # Get the filename from the URL
        filename = os.path.basename(full_url)
        
        # Check if file already exists in the target directory
        if not os.path.exists(os.path.join(save_location, filename)):
            # File doesn't exist, proceed with downloading
            response = requests.get(full_url)
            if response.status_code == 200:
                # Save the file to the preferred location
                with open(os.path.join(save_location, filename), 'wb') as f:
                    f.write(response.content)
                print(f"Downloaded: {filename}")
            else:
                print(f"Failed to download: {filename}")
        else:
            print(f"File already exists: {filename}")