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

# Step 2: Extract the required information from each developer's page
developer_elements = soup.select('.appx-tile-table')
for developer_element in developer_elements:
    # Extract the developer link
    developer_link = developer_element['href']

    # Send a GET request to the developer's page
    developer_response = requests.get(developer_link)
    developer_soup = BeautifulSoup(developer_response.content, 'html.parser')
    print(str(developer_soup))
    save_to_file(str(developer_soup) , 'developer_response.html');

    # # Extract developer name
    # developer_name = developer_soup.select_one('.appx-listing-title').text.strip()

    # # Extract developer location
    # developer_location = developer_soup.select_one('.appx-tile-feature--label:contains("Locations")').find_next_sibling('span').text.strip()

    # # Extract developer badges
    # badges = developer_soup.select('.appx-tile-content-el-value')
    # badges_list = [badge.text.strip() for badge in badges]
    # badges_str = ', '.join(badges_list)

    # # Extract links to developer website and social media profiles
    # links = developer_soup.select('a[href^="http"], a[href^="https"]')
    # links_dict = {link.text.strip(): link['href'] for link in links}

    # # Get website link and social media link from links_dict
    # website = links_dict.get('Website', '')
    # social_media = links_dict.get('Social Media', '')

    # # Append developer details to the sheet
    # sheet.append([developer_name, developer_location, badges_str, website, social_media])

# Save the workbook as an Excel file
# workbook.save('developer_details.xlsx')

# print("Data saved successfully in developer_details.xlsx.")
