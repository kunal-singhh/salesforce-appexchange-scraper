import requests
from bs4 import BeautifulSoup
import re
import openpyxl

# Create a new workbook
workbook = openpyxl.Workbook()
sheet = workbook.active

# Set the column headers
headers = ['Developer Name', 'Location', 'Badges', 'Website', 'Social Media']
sheet.append(headers)

# Step 1: Send a GET request to the Salesforce AppExchange developer listing page
url = 'https://appexchange.salesforce.com/developers'
response = requests.get(url)
soup = BeautifulSoup(response.content, 'html.parser')

def save_to_file(content, filename):
    with open(filename, 'w') as file:
        file.write(content)

# Step 2: Extract the required information from the developer listing page
developer_list = soup.find_all('tr', {'class': 'appx-result-section-table-tr'})
for developer in developer_list:

    # Extract developer name
    developer_name = developer.find('p', {'class': 'slds-truncate appx-listing-title-el'}).text.strip()

    # Extract developer location
    developer_location = developer.find('span', {'class': 'appx-tile-feature--label'}, text='Locations').find_next_sibling('span').text.strip()

    # Extract developer badges
    badges = developer.find_all('span', {'class': 'appx-tile-content-el-value'})
    badges_list = [badge.text.strip() for badge in badges]
    badges_str = ', '.join(badges_list)

    # Extract links to developer website and social media profiles
    links = developer.find_all('a', href=re.compile(r'https?://(www\.)?([A-Za-z_0-9.-]+)\.[A-Za-z]{2,}.*'))
    links_dict = {link.text.strip(): link['href'] for link in links}

    # Get website link and social media link from links_dict
    website = links_dict.get('Website', '')
    social_media = links_dict.get('Social Media', '')

    # Append developer details to the sheet
    sheet.append([developer_name, developer_location, badges_str, website, social_media])

# Save the workbook as an Excel file
workbook.save('developer_details.xlsx')

print("Data saved successfully in developer_details.xlsx.")
