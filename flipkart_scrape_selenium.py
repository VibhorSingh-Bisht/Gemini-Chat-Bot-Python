from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import pandas as pd
import os

def main():
    HEADERS = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36'}
    TAGS = ['Mobile Phones']#,"Laptops","Television","Shoes"]
    URLS = [f"https://www.flipkart.com/search?q={i.replace(' ','%20')}&otracker=search&otracker1=search&marketplace=FLIPKART&as-show=on&as=off" for i in TAGS]

    options = webdriver.ChromeOptions()
    #options.add_experimental_option()
    options.add_argument('--headless')
    options.add_argument('log-level=3')
    
    for key, value in HEADERS.items():
        options.add_argument(f"--{key}={value}")
    
    driver = webdriver.Chrome(options=options)
    for URL in URLS:
        driver.get(URL)
        page_source = driver.page_source
        soup = BeautifulSoup(page_source,'html.parser')
        #links = soup.find_all("a", attrs={'class':'CGtC98'})
        links = driver.find_elements(By.CLASS_NAME,'CGtC98')
        print(links)
        return


if __name__ == '__main__':
    main()