
#This script takes a url(validates if its a valid Wikipedia URL) and a an integer number as input ex 1,2 or 3
import requests
from bs4 import BeautifulSoup
import json
import re

#Scrapes the input url or the first 10 unique urls 
def extract_wikipedia_urls(url, all_urls, max_urls=10):
    print("\nScraping URLs in page :",url)
    response = requests.get(url)
    if response.status_code != 200:
        print(f"Failed to retrieve the webpage: {url}")
        return set()
    
    soup = BeautifulSoup(response.content, 'html.parser')
    urls = set()
    
    for tag in soup.find_all('a', href=True):
        full_url = tag['href']
        if full_url.startswith('http'):
            if full_url not in all_urls:
                urls.add(full_url)
            if len(urls) == max_urls:
                break         
    #print(urls)
    return urls

#Performs scraping based on the number of cycles n 
def get_wikipedia_urls(n, link):
    all_urls = set()
    current_urls = extract_wikipedia_urls(link, all_urls)
    all_urls.update(current_urls)
    
    for _ in range(n):
        new_urls = set()
        for url in current_urls:
            extracted_urls = extract_wikipedia_urls(url, all_urls)
            new_urls.update(extracted_urls)
        all_urls.update(new_urls)
        current_urls = new_urls
    
    return all_urls    

#write results to json file
def save_to_json(data, filename='output.json'):
    with open(filename, 'w') as f:
        json.dump(data, f, indent=4)

#validates if its a valid wikipedia URL
def is_valid_wikipedia_url(url):
    wikipedia_url_pattern = re.compile(r'^https?://([a-z]{2,3}\.)?wikipedia\.org/.*$')
    return wikipedia_url_pattern.match(url) is not None


# Get user input
link = input("Enter a Wikipedia page URL: ")
iterations = input("Enter the number of iterations: ") 
n = int(iterations)
# Validate the Wikipedia URL
if not is_valid_wikipedia_url(link):
    print("Error: The provided URL is not a valid Wikipedia link.")
else:

    final_urls = get_wikipedia_urls(n, link)

    # Prepare results
    result = {
        "all_found_links": list(final_urls),
        "total_count": len(final_urls),
        "unique_count": len(final_urls)
    }

    # Display results
    print("All Found Links:")
    for url in result["all_found_links"]:
        print(url)
    print("\nTotal Count:", result["total_count"])
    print("Unique Count:", result["unique_count"])

    # Save results to JSON file
    save_to_json(result)
