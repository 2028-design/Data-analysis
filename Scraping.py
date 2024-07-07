import httpx
from bs4 import BeautifulSoup
import csv
import os
from selenium import webdriver
from selenium.webdriver.common.by import By

# Function to create a directory if it doesn't exist
def create_directory(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)

# Function to scrape data from a single sub-URL
def scrape_data_from_sub_url(sub_url):
    try:
        response = httpx.get(sub_url)
        response.raise_for_status()

        html_content = response.text  # Get the HTML content as text

        # Use BeautifulSoup to parse the HTML content
        soup = BeautifulSoup(html_content, 'lxml').text

        # Return the parsed HTML content as text
        return str(soup)

    except httpx.HTTPError as e:
        print(f"HTTP error while accessing {sub_url}: {e}")
        return None
    except Exception as e:
        print(f"Error while processing {sub_url}: {e}")
        return None

# Function to save HTML content to a text file
def save_html_to_text_file(html_content, file_path):
    try:
        with open(file_path, 'a', encoding='utf-8') as file:
            file.write(html_content)

    except Exception as e:
        print(f"Error while saving to {file_path}: {e}")

# Define the directory where you want to save the files (custom folder path)
output_directory = r"D:\TYN\data\Anand\09-06 0kb\rest"# Replace with your local directory path

# Create the output directory if it doesn't exist
create_directory(output_directory)

# Set up the Selenium WebDriver
driver = webdriver.Chrome()

# Read URLs and names from the CSV file
csv_file_path = r"C:\Users\TIGER\Downloads\empty text files - Anand.csv"# Replace with the path to your CSV file
company_urls = {}

with open(csv_file_path, 'r') as csv_file:
    csv_reader = csv.DictReader(csv_file)
    for row in csv_reader:
        company_name = row['Name']
        if company_name not in company_urls:
            company_urls[company_name] = set()
        company_urls[company_name].add(row['URL'])

# Create a set to keep track of visited sub-URLs
visited_sub_urls = set()

# Iterate through the sub-URLs and scrape data
for company_name, base_urls in company_urls.items():
    print(f"Scraping data for {company_name}:")

    for base_url in base_urls:
        driver.get(base_url)

        # Wait for JavaScript content to load (you might need to adjust the waiting time)
        driver.implicitly_wait(10)

        # Get the list of unique sub-URLs from the current page
        sub_urls = set(a.get_attribute('href') for a in driver.find_elements(By.TAG_NAME, 'a'))

        # Define the output file name based on company name
        file_name = f"{company_name}.txt"
        file_path = os.path.join(output_directory, file_name)

        for sub_url in sub_urls:
            if sub_url not in visited_sub_urls:
                print(f"Processing sub URL: {sub_url}")
                sub_url_html = scrape_data_from_sub_url(sub_url)

                if sub_url_html:
                    # Save the HTML content to the text file
                    save_html_to_text_file(sub_url_html, file_path)

                # Add the visited sub-URL to the set
                visited_sub_urls.add(sub_url)

# Close the browser
driver.quit()