import requests
from bs4 import BeautifulSoup
import pandas as pd
from concurrent.futures import ThreadPoolExecutor

# Function to extract information from a single URL
def extract_info(url):
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')

        # Extract name
        name_tag = soup.find('div', class_='sales-info').find('h1', class_='dockable business-name')
        name = name_tag.text.strip() if name_tag else 'No name found'

        # Extract phone number
        phone_tag = soup.find('a', class_='phone dockable')
        phone = phone_tag.find('span', class_='full').text.strip() if phone_tag else 'No phone number found'

        # Extract website
        website_tag = soup.find('a', class_='website-link dockable')
        website = website_tag['href'] if website_tag else 'No website found'

        # Extract location
        location_tag = soup.find('a', class_='directions small-btn')
        location = location_tag.find('span', class_='address').text.strip() if location_tag else 'No location found'

        return {
            'Name': name,
            'Phone': phone,
            'Website': website,
            'Location': location
        }
    except Exception as e:
        print(f"Failed to extract info from {url}: {e}")
        return None

# Read URLs from the file
with open('link.txt', 'r') as file:
    urls = [url.strip() for url in file.readlines() if url.strip()]

# Use ThreadPoolExecutor to make concurrent requests
data = []
with ThreadPoolExecutor(max_workers=10) as executor:
    results = executor.map(extract_info, urls)

    for result in results:
        if result:
            data.append(result)

# Create a DataFrame from the collected data
df = pd.DataFrame(data)

# Write the DataFrame to an Excel file
output_file = 'extracted_info.xlsx'
df.to_excel(output_file, index=False)

print(f"Data successfully saved to {output_file}")
