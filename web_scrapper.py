"""
Written by Garnet Merrill 11/08/2023
This script will read a list of URLs in and then hit the pages looking for errors
"""

import csv
import requests
from bs4 import BeautifulSoup
import re
import subprocess
from urllib.parse import urlparse
from concurrent.futures import ThreadPoolExecutor

def get_boca_urls():
    boca_query = "SELECT BOCA_Form_Link__c FROM program__c WHERE publish_boca__c = TRUE"
    output = subprocess.check_output(['sf', 'data', 'query', '-o', 'Production', '-q', boca_query , '-r', 'csv'])
    reader = csv.reader(output.decode().splitlines())
    results = list(reader)
    urls = []  # Initialize an empty list to store the links
    for result in results:
        soup = BeautifulSoup(result[0], 'html.parser')
        link = soup.a['href'] if soup.a else 'No link'
        urls.append(link)  # Append the link to the list
    return urls  # Return the list of links

def extract_bocatype(url):
    pattern = r'creditapplication/(.*?)(?=\?)'
    match = re.search(pattern, url)
    return match.group(1) if match else None

def extract_pgm(url):
    pattern = r'pgm=([^&]*)'
    match = re.search(pattern, url)
    return match.group(1) if match else None

def scrape_url(url):
    if url.strip():
        parsed_url = urlparse(url)
        if bool(parsed_url.scheme):
            response = requests.get(url)
            soup = BeautifulSoup(response.text, 'lxml')  # Changed parser to 'lxml'
            title_tag = soup.find('title')
            if title_tag is not None:
                if 'Application Error' not in title_tag.string:
                    return 'good'
                else:
                    return 'bad'
            else:
                if 'errorCode' in response.text:
                    #print(f'Error code found in response: {url}')
                    boca_type = extract_bocatype(url)
                    boca_pgm = extract_pgm(url)
                    print(f'Error code found in response: {boca_type} {boca_pgm} {url}')
                else:
                    boca_type = extract_bocatype(url)
                    boca_pgm = extract_pgm(url)
                    print(f'No title tag found: {boca_type} {boca_pgm} {url}')
              
                return 'not found'
    return None

def scrape_page(boca):
    gcount = 0
    bcount = 0
    nfcount = 0

    with ThreadPoolExecutor() as executor:
        results = executor.map(scrape_url, boca)
        for result in results:
            if result == 'good':
                gcount += 1
            elif result == 'bad':
                bcount += 1
            elif result == 'not found':
                nfcount += 1
      

               

    print(f'Good: {gcount} Bad: {bcount} Not Found: {nfcount}')

if __name__ == "__main__":
    boca_urls = get_boca_urls()
    scrape_page(boca_urls)
