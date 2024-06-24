import requests
from bs4 import BeautifulSoup

# Base URL of the Yellow Pages search results page
base_url = 'https://www.yellowpages.com/search?search_terms=restaurant&geo_location_terms=San+Francisco%2C+CA&page='

# Number of pages to scrape
num_pages = int(input('How many page:'))

# Function to get company links from a single page
def get_company_links(page_number):
    url = base_url + str(page_number)
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    cards = soup.find_all('div', class_='result')
    links = []

    for card in cards:
        link_tag = card.find('a', class_='business-name')
        if link_tag and 'href' in link_tag.attrs:
            link = link_tag['href']
            full_link = f"https://www.yellowpages.com{link}"
            links.append(full_link)
    
    return links

# Collect links from multiple pages
all_links = []
for page in range(1, num_pages + 1):
    all_links.extend(get_company_links(page))

# Print all collected links
for link in all_links:
    print(link)
    with open('links.txt','a') as file:
        file.write(link+'\n')
