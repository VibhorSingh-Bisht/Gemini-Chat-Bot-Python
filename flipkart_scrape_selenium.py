from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import pandas as pd
import os
import json

# Function to extract Product Title
def get_title(soup):
    try:
        # Outer Tag Object
        title = soup.find("span", attrs={"class":'VU-ZEz'})

        # Inner NavigatableString Object
        title_value = title.text

        # Title as a string value
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
            # If there is some deal price
            price = soup.find("div", attrs={'class':'Nx9bqj CxhGGd'})
            price = price.text

        except:
            price = ""

    return price

# Function to extract Product Rating
def get_rating(soup):

    try:
        rating = soup.find("i", attrs={'class':'col-12-12 ggs1+C'}).text
        rating = rating + "out of 5"

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

# Function to extract Availability Status
def get_image(soup):
    try:
        image = soup.find('img',attrs={'class','DByuf4 IZexXJ jLEJ7H'})
        if image and 'srcset' in image.attrs:
            srcset = image['srcset']
            # Split the srcset into individual URLs
            srcset_urls = srcset.split(',')
            # Extract the second URL
            if len(srcset_urls) > 1:
                return srcset_urls[0]

    except AttributeError:
        image = "Not Available"

    return image


def main():
    HEADERS = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36'}
    TAGS = ['Mobile Phones',"Laptops","Television","Shoes"]
    URLS = [f"https://www.flipkart.com/search?q={i.replace(' ','%20')}&otracker=search&otracker1=search&marketplace=FLIPKART&as-show=on&as=off" for i in TAGS]

    options = webdriver.ChromeOptions()
    #options.add_experimental_option()
    options.add_argument('--headless')
    options.add_argument('log-level=3')
    
    for key, value in HEADERS.items():
        options.add_argument(f"--{key}={value}")
    
    driver = webdriver.Chrome(options=options)
    links_list = []
    for URL in URLS:
        driver.get(URL)
        page_source = driver.page_source
        soup = BeautifulSoup(page_source,'html.parser')
        script_tag = soup.find('script', {'id': 'jsonLD', 'type': 'application/ld+json'})
        #links = driver.find_elements(By.CSS_SELECTOR,'a.CGtC98')
        #print(page_source)
        
        links = []
        if script_tag:
            json_content = script_tag.string
            data = json.loads(json_content)

            # Extract URLs from the JSON data
            links = [item['url'] for item in data['itemListElement']]

        # Loop for extracting links from Tag Objects
        for link in links:
            link = link.split('pid')[0]
            links_list.append(link)

    d = {"title":[], "price":[], "rating":[], "reviews":[],"Image URL":[]}
    # Loop for extracting product details from each link
    
    for link in links_list:
        try:
            driver.get(link)
            new_page_source = driver.page_source
            new_soup = BeautifulSoup(new_page_source, "html.parser")

            # Function calls to display all necessary product information
            d['title'].append(get_title(new_soup))
            d['price'].append(get_price(new_soup))
            d['rating'].append(get_rating(new_soup))
            d['reviews'].append(get_review_count(new_soup))
            d['Image URL'].append(get_image(new_soup))
        except Exception as e:
            print(f'error in {link}: {e}')
            continue
    driver.quit()

    amazon_df = pd.DataFrame.from_dict(d)
    amazon_df = amazon_df.replace({'title': ''}, pd.NA)
    amazon_df = amazon_df.dropna(subset=['title'])
    file_path = f'{os.getcwd()}\\data\\amazon_data.csv'
    if not os.path.isfile(file_path):
        amazon_df.to_csv(file_path, mode='w', index=False, header=True)
    else:
    
        amazon_df.to_csv(file_path, mode='a', index=False, header=False) 


if __name__ == '__main__':
    main()