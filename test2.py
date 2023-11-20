import csv
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import time
import getpass


#Use Chromdriver to get the page
browser_driver = Service('/usr/bin/chromedriver')
page_to_scrape = webdriver.Chrome(service=browser_driver)
page_to_scrape.get("http://quotes.toscrape.com")

#Use Selenium to login
page_to_scrape.find_element(By.LINK_TEXT, 'Login').click()
time.sleep(3)

username = page_to_scrape.find_element(By.ID, "username")
password = page_to_scrape.find_element(By.ID, "password")
username.send_keys("admin")
#prompt for password
my_pass = getpass.getpass()
password.send_keys()

page_to_scrape.find_element(By.CSS_SELECTOR, "input.btn-primary").click()

file = open("scraped_quotes.csv", "w")
writer = csv.writer(file)

writer.writerow(["QUOTES", "AUTHORS"])
while True:
    quotes = page_to_scrape.find_elements(By.CLASS_NAME, "text")
    authors = page_to_scrape.find_elements(By.CLASS_NAME, "author")
    for quote, author in zip(quotes, authors):
        print(quote.text + " - " + author.text)
        writer.writerow([quote.text, author.text])
    try:
        page_to_scrape.find_element(By.PARTIAL_LINK_TEXT, "Next").click()
    except NoSuchElementException:
        break
file.close()