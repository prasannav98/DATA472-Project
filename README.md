# How to use the project:
The entire project is automated and runs once every 3 months powered by the crontab. To access the data follow the GET links
- [data](http://13.210.241.172:5000/pvv13/national-benefits)

- [metadata](http://13.210.241.172:5000/pvv13/national-benefits-meta)

# What does each file in the repo do:

## main.py
This script automates the process of scraping a webpage from the Ministry of Social Development (MSD) website for links to Excel files related to benefit statistics and downloading these files to a specified local directory.
The script makes an HTTP GET request to a specified MSD webpage.
It parses the HTML content of the webpage using BeautifulSoup.
The script searches for links on the page that contain 'statistics/benefit/archive' in their href attributes.
For each found link, it constructs the full URL and uses getLink, to download the corresponding Excel files to a specified local directory.

## getLink.py
This script automates the process of downloading Excel files from a specified webpage. It performs the following steps:
It sends a GET request to a provided URL.
Then it uses BeautifulSoup to parse the HTML content and find links containing 'national-benefit-tables' in their href attributes.
After which, it collects the href values of the found links and extracts them.
Finally, it constructs full URLs for these links, checks if the files already exist in the specified local directory, and downloads them if they do not.

## datacleaning.py
The datacleaning.py script is designed to automate the cleaning and processing of benefit statistics data stored in Excel files. 
It transforms the data into a consolidated CSV format, making it ready for analysis or further processing.
It automatically reads Excel files from the specified directory.
Then cleans and restructures the data, handling NaN values and reorganizing columns.
After which, it saves cleaned data to intermediate CSV files.
Finally, it merges the final CSV files into a single master file.
It deletes unnecessary intermediate files for a clean workspace.

## meta.json
It has all the metadata of the extracted data. 
