import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import openpyxl

# Create a new workbook
workbook = openpyxl.Workbook()
sheet = workbook.active

# Set the column headers
headers = ['Developer Name', 'Location', 'Badges', 'LinkedIn', 'Twitter', 'Website']
sheet.append(headers)

# Set up Selenium
chrome_options = Options()
chrome_options.add_argument("--headless")  # Run Chrome in headless mode
service = Service('path/to/chromedriver')  # Path to your chromedriver executable
driver = webdriver.Chrome(service=service, options=chrome_options)

# Step 1: Load the Salesforce AppExchange developer listing page
driver.get('https://appexchange.salesforce.com/developers')

# Wait for the page to fully load
time.sleep(5)

# Step 2: Extract the required information from each developer's page
developer_elements = driver.find_elements(By.CSS_SELECTOR, '.appx-tile-table')
for developer_element in developer_elements:
    # Extract the developer link
    developer_link = developer_element.get_attribute('href')

    # Load the developer's page
    driver.get(developer_link)

    # Wait for the page to fully load
    time.sleep(5)

    # Extract developer name
    # developer_name_element = driver.find_element(By.CSS_SELECTOR, '.appx-listing-title')
    # developer_name = developer_name_element.text.strip()

    # Extract developer location
    # location_element = driver.find_element(By.XPATH, "//span[contains(text(), 'Locations')]/following-sibling::span")
    # developer_location = location_element.text.strip()

    # Extract developer badges
    # badges_elements = driver.find_elements(By.CSS_SELECTOR, '.appx-tile-content-el-value')
    # badges_list = [badge.text.strip() for badge in badges_elements]
    # badges_str = ', '.join(badges_list)

    # Extract links from the developer's page
    links_elements = driver.find_elements(By.CSS_SELECTOR, 'a[href^="http"], a[href^="https"]')
    links_dict = {}
    for link in links_elements:
        link_text = link.text.strip()
        link_url = link.get_attribute('href')
        if link_text in ['LinkedIn', 'Twitter', 'Website']:
            links_dict[link_text] = link_url

    # Get the LinkedIn, Twitter, and Website links
    linkedin = links_dict.get('LinkedIn', '')
    twitter = links_dict.get('Twitter', '')
    website = links_dict.get('Website', '')
    print(linkedin, twitter, website)

    # Append developer details to the sheet
    sheet.append([linkedin, twitter, website])

# Save the workbook as an Excel file
workbook.save('developer_details.xlsx')

# Quit the Selenium driver
driver.quit()

print("Data saved successfully in developer_details.xlsx.")
