import csv
import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime

# Function to scrape the URLs and extract <loc> tags
def scrape_and_extract_locs(url):
    locs = []
    try:
        response = requests.get(url, timeout=10)  # Timeout for the request
        response.raise_for_status()  # will throw an exception for 4XX/5XX status
        soup = BeautifulSoup(response.content, 'xml')
        locs = [loc_tag.text for loc_tag in soup.find_all('loc')]
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err} - URL: {url}")
    except requests.exceptions.ConnectionError as conn_err:
        print(f"Connection error occurred: {conn_err} - URL: {url}")
    except requests.exceptions.Timeout as timeout_err:
        print(f"Timeout error occurred: {timeout_err} - URL: {url}")
    except requests.exceptions.RequestException as req_err:
        print(f"An error occurred: {req_err} - URL: {url}")
    except Exception as err:
        print(f"An unexpected error occurred: {err} - URL: {url}")
    finally:
        return locs

# Generate a unique output file name with a timestamp
timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
output_file_name = f'extracted_locs_{timestamp}.csv'

# Read the CSV with URLs
with open('input_urls.csv', mode='r', newline='') as file:
    reader = csv.reader(file)
    url_list = [row[0] for row in reader]

# List to hold all the sitemaps and locs
sitemap_locs = []

# Loop over all URLs in the CSV
for sitemap_url in url_list:
    locs = scrape_and_extract_locs(sitemap_url)
    for loc in locs:
        sitemap_locs.append([sitemap_url, loc])

# Save the extracted locs to a CSV file with a unique name
df = pd.DataFrame(sitemap_locs, columns=['Sitemap', 'Loc'])
df.to_csv(output_file_name, index=False)

print(f"Data extracted and saved to {output_file_name}")