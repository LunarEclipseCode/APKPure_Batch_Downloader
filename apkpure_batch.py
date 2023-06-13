import os
import requests
from selenium import webdriver
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from urllib.request import Request, urlopen
from concurrent.futures import ThreadPoolExecutor
from bs4 import BeautifulSoup as soup

# Configuration
browser_type = "chrome"    # Set the desired browser type: "firefox" or "chrome"
gecko_path = "D:\\Mozilla\\geckodriver.exe"
firefox_exe_path = "C:\\Program Files\\Mozilla Firefox\\firefox.exe"
chrome_driver_path = "D:\\Chrome\\chromedriver.exe"
chrome_exe_path = "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe"

destination = "D:\\Downloads\\AppsMore"
website = f"https://apkpure.com/developer/Softecks"
start = 1
end = 2
concurrent = 5

# Create a new Chrome driver instance
if browser_type == "firefox":
    options = FirefoxOptions()
    options.binary_location = firefox_exe_path
    service = FirefoxService(executable_path=gecko_path)
    driver = webdriver.Firefox(service=service, options=options)
elif browser_type == "chrome":
    options = ChromeOptions()
    options.binary_location = chrome_exe_path
    service = ChromeService(executable_path=chrome_driver_path)
    driver = webdriver.Chrome(service=service, options=options)
else:
    raise ValueError("Invalid browser type specified")

agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/91.0.4472.124 Safari/537.36'

# Store links of all the apps
app_links_all = []
app_file_names = []
app_file_type = []
    
for i in range(start, end+1):
    url = f"{website}?page={i}"
    driver.get(url)
    
     # Refresh the page if a 404 error is detected
    try:
        error_element = driver.find_element(By.CLASS_NAME, "p404")
        while error_element is not None:
            driver.refresh()
            error_element = driver.find_element(By.CLASS_NAME, "p404")
    except NoSuchElementException:
        pass
    
    elements = driver.find_elements(By.CLASS_NAME, "more-down1")
    app_links = [element.get_attribute("href") for element in elements]
    
    for weblink in app_links:
        req = Request(weblink, headers={'User-Agent': agent})
        webpage = urlopen(req).read()
        page_soup = soup(webpage, "html.parser") 
        
        # extract the file names
        try:
            name = page_soup.select_one('.info-title').get_text(strip=True)
            version = page_soup.select_one('.info-sdk span').get_text(strip=True)
            type = page_soup.select_one('.info-tag').get_text(strip=True).lower()
            file_name = name + "_" + version + "_" + "Apkpure." + type
            if file_name not in app_file_names:
                app_file_names.append(file_name)
                app_file_type.append(type)
                app_links_all.append(weblink)
    
        except AttributeError:
            print("Missing information on webpage. Skipping...")
        
driver.quit()

def remove_specific_characters(strings, characters_to_remove):
    cleaned_strings = []
    for string in strings:
        cleaned_string = string
        for char in characters_to_remove:
            cleaned_string = cleaned_string.replace(char, '')
        cleaned_strings.append(cleaned_string)
    return cleaned_strings

characters_to_remove = [':']
app_file_names = remove_specific_characters(app_file_names, characters_to_remove)

# Store download links of all the apps
new_urls = []

for url, ext in zip(app_links_all, app_file_type):
    package_name = url.split('/')[-2]
    new_url = f"https://d.apkpure.com/b/{ext.upper()}/{package_name}?version=latest"
    new_urls.append(new_url)
    
# Create the folder if it doesn't exist
os.makedirs(destination, exist_ok=True)

def download_file(url, filename, folder):
    headers = {
        'User-Agent': agent
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        # Build the full file path
        file_path = os.path.join(folder, filename)

        with open(file_path, 'wb') as file:
            file.write(response.content)
        print(f"Downloaded {filename} successfully.")
    else:
        print(f"Failed to download {filename}.")
        
# Create a ThreadPoolExecutor with maximum concurrency of 10
executor = ThreadPoolExecutor(max_workers=concurrent)

# Download files concurrently
futures = []
for link, name in zip(new_urls, app_file_names):
    future = executor.submit(download_file, link, name, destination)
    futures.append(future)

# Wait for all downloads to complete
for future in futures:
    future.result()

# Shut down the executor
executor.shutdown()