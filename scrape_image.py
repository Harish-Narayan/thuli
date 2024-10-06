import requests
from bs4 import BeautifulSoup

# Replace with the actual URL you want to scrape
url = "https://starsunfolded.com/bipasha-basu/"  # Example URL
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
}

# Send a GET request to the URL
response = requests.get(url, headers=headers)

# Check if the request was successful
if response.status_code == 200:
    # Parse the HTML content
    soup = BeautifulSoup(response.content, 'html.parser')

    # Find the section that contains "Physical Stats & More"
    physical_stats_header = soup.find('span', string="Physical Stats & More")

    # Initialize dictionary to hold scraped data
    scraped_data = {}

    if physical_stats_header:
        # Get all <tr> elements following the header
        rows = physical_stats_header.find_all_next('tr')

        for row in rows:
            # Extract data from each <td> in the row
            columns = row.find_all('td')
            if columns and len(columns) == 2:
                key = columns[0].get_text(strip=True)
                value = columns[1].get_text(strip=True)

                # Collect only the specific attributes we want
                if key in ['Height', 'Weight (approx.)', 'Figure Measurements (approx.)', 'Eye Colour', 'Hair Colour']:
                    scraped_data[key] = value
            else:
                # Stop if we encounter a row that isn't a data row (e.g., another header)
                if row.find('span') or 'header' in row.get('class', []):
                    break  # Stop if another header is found or based on the class condition

        # Print the filtered scraped data
        for key, value in scraped_data.items():
            print(f"{key}: {value}")
    else:
        print("Physical Stats & More section not found.")
else:
    print(f"Failed to retrieve the page. Status code: {response.status_code}")
