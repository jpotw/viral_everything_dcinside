from selenium import webdriver
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os
import pandas as pd
import time
import random #to not be detected as a bot


firefox_options = FirefoxOptions()
# Enable private browsing
firefox_options.add_argument("-private")
# Set additional privacy settings if needed

service = FirefoxService(executable_path=GeckoDriverManager().install())

driver = webdriver.Firefox(service=service, options=firefox_options)

# Navigate to the "특이점이온다(best)" page

driver.get("https://gall.dcinside.com/mgallery/board/lists/?id=thesingularity&exception_mode=recommend")


def scrape_page(driver):
    WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "td.gall_tit.ub-word > a:not(.reply_numbox)")))
    # Random delay before scraping articles
    time.sleep(random.uniform(1, 3))
    
    articles = driver.find_elements(By.CSS_SELECTOR, "td.gall_tit.ub-word > a:not(.reply_numbox)")
    data = []
    for article in articles:
        title = article.text
        article_url = article.get_attribute('href')

        # Navigate to the article's page
        driver.get(article_url)
        
        # Wait for the content of the article to load
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "div.view_content")))
        
        # Extract the content of the article
        content = driver.find_element(By.CSS_SELECTOR, 'div.view_content').text
        
        data.append({'title': title, 'content': content})
        
        # Navigate back to the list page
        driver.back()
        WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "td.gall_tit.ub-word > a:not(.reply_numbox)")))
    
    return data

# Function to click the 'next' button
def go_to_next_page(driver):
    next_page_link = driver.find_element(By.CSS_SELECTOR, "a[href*='page=']")
    driver.get(next_page_link.get_attribute('href'))

# Scrape the first page
driver.get('https://gall.dcinside.com/mgallery/board/lists/?id=thesingularity&page=1&exception_mode=recommend')
data = scrape_page(driver)

print("success!")

# Go to the next page and scrape
go_to_next_page(driver)
random_delay = random.uniform(2, 5)  # Random delay between 2 and 5 seconds
time.sleep(random_delay)  # Wait for the next page to load with a random delay
data.extend(scrape_page(driver))

# Quit the driver
driver.quit()

# Create a pandas DataFrame
df = pd.DataFrame(data)

# Get the desktop path for the current user
desktop_path = os.path.join(os.path.expanduser('~'), 'C:/Users/parkj/OneDrive/바탕 화면')

# Define the path for the Excel file on the desktop
excel_path = os.path.join(desktop_path, '특이점이온다 베스트.xlsx')

# Save the DataFrame to an Excel file on the desktop
df.to_excel(excel_path, index=False)

print(f"The Excel file has been saved to {excel_path}")