from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import pandas as pd
import os
import json
import requests
from openpyxl import Workbook
from openpyxl.drawing.image import Image
from io import BytesIO

# Function to extract Product Title
def get_title(soup):
    try:
        title = soup.find("span", attrs={"class":'VU-ZEz'})
        title_value = title.text
        title_string = title_value.strip()
    except AttributeError:
        title_string = ""
    return title_string

# Function to extract Product Price
def get_price(soup):
    try:
        price = soup.find("div", attrs={'class':'Nx9bqj CxhGGd'})
        price = price.text
    except AttributeError:
        try:
            price = soup.find("div", attrs={'class':'Nx9bqj CxhGGd'})
            price = price.text
        except:
            price = ""
    return price

# Function to extract Product Rating
def get_rating(soup):
    try:
        rating = soup.find("i", attrs={'class':'col-12-12 ggs1+C'}).text
        rating = rating + " out of 5"
    except AttributeError:
        rating = ""
    return rating

# Function to extract Number of User Reviews
def get_review_count(soup):
    try:
        rating = soup.find_all("div", attrs={'class':'row j-aW8Z'})
        review_count_final = ''
        for i in rating:
            review_count_final += i.text
    except AttributeError:
        review_count_final = ""
    return review_count_final

# Function to extract Image URL
def get_image(soup):
    try:
        image = soup.find('img', attrs={'class':'DByuf4 IZexXJ jLEJ7H'})
        if image and 'srcset' in image.attrs:
            srcset = image['srcset']
            srcset_urls = srcset.split(',')
            if len(srcset_urls) > 1:
                return srcset_urls[0].strip().split(' ')[0]
    except AttributeError:
        image = "Not Available"
    return image

# Function to download image and return it as a PIL Image
def download_image(image_url):
    response = requests.get(image_url)
    if response.status_code == 200:
        img = Image(BytesIO(response.content))
        return img
    else:
        return None

def main():
    HEADERS = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36'}
    TAGS = ['Mobile Phones', "Laptops", "Television", "Shoes"]
    URLS = [f"https://www.flipkart.com/search?q={i.replace(' ', '%20')}&otracker=search&otracker1=search&marketplace=FLIPKART&as-show=on&as=off" for i in TAGS]

    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('log-level=3')
    for key, value in HEADERS.items():
        options.add_argument(f"--{key}={value}")

    driver = webdriver.Chrome(options=options)
    links_list = []
    for URL in URLS:
        driver.get(URL)
        page_source = driver.page_source
        soup = BeautifulSoup(page_source, 'html.parser')
        script_tag = soup.find('script', {'id': 'jsonLD', 'type': 'application/ld+json'})
        links = []
        if script_tag:
            json_content = script_tag.string
            data = json.loads(json_content)
            links = [item['url'] for item in data['itemListElement']]
        for link in links:
            link = link.split('pid')[0]
            links_list.append(link)

    wb = Workbook()
    ws = wb.active
    ws.title = "Amazon Data"
    ws.append(["Title", "Price", "Rating", "Reviews", "Image"])

    for link in links_list:
        try:
            driver.get(link)
            new_page_source = driver.page_source
            new_soup = BeautifulSoup(new_page_source, "html.parser")

            title = get_title(new_soup)
            price = get_price(new_soup)
            rating = get_rating(new_soup)
            reviews = get_review_count(new_soup)
            image_url = get_image(new_soup)

            img = None
            if image_url != "Not Available":
                img = download_image(image_url)

            ws.append([title, price, rating, reviews, ""])

            if img:
                img_row = ws.max_row
                img_column = 5  # Assuming the "Image" column is the 5th column
                img_anchor = f'E{img_row}'
                ws.add_image(img, img_anchor)

        except Exception as e:
            print(f'Error in {link}: {e}')
            continue

    driver.quit()

    file_path = os.path.join(os.getcwd(), 'data', 'amazon_data.xlsx')
    wb.save(file_path)

if __name__ == '__main__':
    main()
