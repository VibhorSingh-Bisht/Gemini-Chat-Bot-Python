from bs4 import BeautifulSoup
import requests
import pandas as pd
import numpy as np
import os

# Function to extract Product Title
def get_title(soup):

    try:
        # Outer Tag Object
        title = soup.find("span", attrs={"id":'productTitle'})

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
        price = soup.find("span", attrs={'class':'a-price-whole'})
        price = price.text
        price = '₹' + price

    except AttributeError:

        try:
            # If there is some deal price
            price = soup.find("span", attrs={'class':'a-price-whole'})
            price = price.text
            price = '₹' + price

        except:
            price = ""

    return price

# Function to extract Product Rating
def get_rating(soup):

    try:
        rating = soup.find("i", attrs={'class':'a-icon a-icon-star a-star-4-5'}).string.strip()

    except AttributeError:
        try:
            rating = soup.find("span", attrs={'class':'a-icon-alt'}).string.strip()
        except:
            rating = ""

    return rating

# Function to extract Number of User Reviews
def get_review_count(soup):
    try:
        review_count = soup.find("span", attrs={'id':'acrCustomerReviewText'}).string.strip()

    except AttributeError:
        review_count = ""

    return review_count

# Function to extract Availability Status
def get_availability(soup):
    try:
        available = soup.find("div", attrs={'id':'availability'})
        available = available.find("span").string.strip()

    except AttributeError:
        available = "Not Available"

    return available

def main():

    # add your user agent
    HEADERS = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36'}

    # The webpage URL
    TAGS = ['Mobile Phones',"Laptops","Television","Shoes"]
    URLS = [f"https://www.amazon.in/s?k={i.replace(' ','+')}&ref=nb_sb_noss" for i in TAGS]

    #store links
    links_list = []
    for URL in URLS:
        # HTTP Request
        webpage = requests.get(URL, headers=HEADERS)

        # Soup Object containing all data
        soup = BeautifulSoup(webpage.content, "html.parser")

        # Fetch links as List of Tag Objects
        links = soup.find_all("a", attrs={'class':'a-link-normal s-no-outline'})

        # Loop for extracting links from Tag Objects
        for link in links:
            link = link.get('href')
            link = link.split('ref')[0]
            links_list.append(link)

    d = {"title":[], "price":[], "rating":[], "reviews":[],"availability":[]}

    # Loop for extracting product details from each link
    for link in links_list:
        try:
            new_webpage = requests.get("https://www.amazon.in" + link, headers=HEADERS)

            new_soup = BeautifulSoup(new_webpage.content, "html.parser")

            # Function calls to display all necessary product information
            d['title'].append(get_title(new_soup))
            d['price'].append(get_price(new_soup))
            d['rating'].append(get_rating(new_soup))
            d['reviews'].append(get_review_count(new_soup))
            d['availability'].append(get_availability(new_soup))
        except:
            continue

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

