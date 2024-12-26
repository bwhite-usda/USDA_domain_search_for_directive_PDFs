from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import time

def search_usda_pdfs_with_selenium():
    driver = webdriver.Chrome()  # Replace with your preferred browser
    driver.get("https://www.google.com")

    # Search for PDFs
    search_box = driver.find_element(By.NAME, "q")
    search_box.send_keys("site:usda.gov filetype:pdf Directive")
    search_box.send_keys(Keys.RETURN)

    # Handle Google login (if required)
    # **Note:** This is a simplified example. You might need to adjust based on Google's specific login flow and any changes to the website's structure.
    # If Google prompts for login:
    login_button = driver.find_element(By.XPATH, "//input[@id='identifierId']")
    login_button.send_keys("your_google_email")
    next_button = driver.find_element(By.XPATH, "//button[@id='identifierNext']")
    next_button.click()

    # Wait for the password field to appear
    time.sleep(2)

    password_field = driver.find_element(By.XPATH, "//input[@name='password']")
    password_field.send_keys("your_google_password")
    sign_in_button = driver.find_element(By.XPATH, "//button[@id='passwordNext']")
    sign_in_button.click()

    # Wait for search results to load after login
    time.sleep(5)

    # Parse the HTML content
    soup = BeautifulSoup(driver.page_source, 'html.parser')

    # Extract PDF links
    pdf_links = []
    for a_tag in soup.find_all("a", href=True):
        href = a_tag['href']
        if "pdf" in href and "Directive" in href:
            # Clean up the URL from Google redirect nonsense
            match = re.search(r"https?://[^\s&]+", href)
            if match:
                pdf_links.append(match.group())

    return pdf_links

if __name__ == "__main__":
    pdf_links = search_usda_pdfs_with_selenium()
    print("Found PDF links with 'Directive' in the title:")
    for link in pdf_links:
        print(link)

