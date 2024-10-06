import requests
from bs4 import BeautifulSoup
import json

# List of celebrities categorized by body shape
celebrities = {
    'Pear Shape': ['bipasha-basu', 'vidya-balan', 'rani-mukerji', 'sonakshi-sinha', 'shreya-ghoshal'],
    'Apple Shape': ['shilpa-shetty', 'kareena-kapoor', 'bhumi-pednekar', 'richa-chadha', 'parineeti-chopra'],
    'Oval Shape': ['swara-bhasker', 'huma-qureshi', 'zareen-khan', 'divya-dutta', 'neha-dhupia'],
    'Rectangle Shape': ['madhuri-dixit', 'anushka-sharma', 'deepika-padukone', 'kriti-sanon', 'taapsee-pannu'],
    'Hourglass Shape': ['aditi-rao-hydari', 'katrina-kaif', 'priyanka-chopra', 'sushmita-sen', 'malaika-arora'],
    'Inverted Triangle Shape': ['pooja-hegde', 'karisma-kapoor', 'aishwarya-rai', 'tamannaah', 'nargis-fakhri']
}

# Define user-agent for the request header
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
}

def scrape_physical_stats(celebrity_name):
    # URL to scrape
    url = f"https://starsunfolded.com/{celebrity_name}/"
    response = requests.get(url, headers=headers)

    # Check if the request was successful
    if response.status_code == 200:
        # Parse the HTML content
        soup = BeautifulSoup(response.content, 'html.parser')

        # Find the section that contains "Physical Stats & More"
        physical_stats_header = soup.find('span', string="Physical Stats & More")

        # Initialize a dict to hold the scraped stats
        scraped_stats = {}

        if physical_stats_header:
            # Get all <tr> elements following the header
            rows = physical_stats_header.find_all_next('tr')

            for row in rows:
                # Extract data from each <td> in the row
                columns = row.find_all('td')
                if columns:
                    # Use the first <td> as the key and the second as the value
                    row_data = [col.get_text(strip=True) for col in columns]
                    
                    # Append relevant stats to the dict
                    if row_data[0] in ['Height', 'Weight (approx.)', 'Eye Colour', 'Hair Colour', 'Figure Measurements (approx.)']:
                        scraped_stats[row_data[0]] = row_data[1]
                else:
                    # Stop if we encounter a row that isn't a data row (e.g., another header)
                    if row.find('span') or row.get('class') == ['column-1']:  # Adjust based on your observation
                        break  # Stop if another header is found or based on the class condition
            return scraped_stats
        else:
            return "Physical Stats & More section not found."
    else:
        return f"Failed to retrieve the page. Status code: {response.status_code}"

# Big dictionary to hold all the data
big_dict = {}

# Iterate through each body shape and its celebrities
for body_shape, celeb_list in celebrities.items():
    for celeb in celeb_list:
        celeb_name = celeb.replace('-', ' ').title()
        print(f"Fetching stats for: {celeb_name}")
        stats = scrape_physical_stats(celeb)
        if isinstance(stats, dict):
            # Add the celebrity's stats to the big dictionary
            big_dict[celeb_name] = stats
        else:
            # Handle case where stats are not available
            big_dict[celeb_name] = stats

# Write the dictionary to a JSON file
with open('celebrity_physical_stats.json', 'w') as json_file:
    json.dump(big_dict, json_file, indent=4)

print("Data has been written to celebrity_physical_stats.json")
