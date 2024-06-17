from selenium import webdriver
from bs4 import BeautifulSoup


options = webdriver.ChromeOptions()
#options.add_experimental_option()
options.add_argument('--headless')
options.add_argument('log-level=3')
driver = webdriver.Chrome(options=options)
driver.get('https://www.flipkart.com/samsung-galaxy-f14-5g-goat-green-128-gb/p/itm032d1a69999cc?')
page_source1 = driver.page_source
soup = BeautifulSoup(page_source1,'html.parser')
image = soup.find('img',attrs={'class','DByuf4 IZexXJ jLEJ7H'})
if image and 'srcset' in image.attrs:
        srcset = image['srcset']
        # Split the srcset into individual URLs
        srcset_urls = srcset.split(',')
        print(srcset)
        print(srcset_urls)
        # Extract the second URL
        if len(srcset_urls) > 1:
            print(srcset_urls[1])

driver.quit()