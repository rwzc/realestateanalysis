#!/usr/bin/env python
# coding: utf-8

# ## Package requirements
# - check the requirements.txt file
# - Citations and Credits to 
#     - https://github.com/aloysiuschan/99co
#     - https://towardsdatascience.com/get-your-own-data-building-a-scalable-web-scraper-with-aws-654feb9fdad7

# The webscrapper adheres to the 99.co Robots.txt file config
# ![](./99coRobotstxt.png)

# ### Import the following packages

# In[1]:


import pandas as pd
import yaml
import re
import requests
import random
from time import sleep
from selenium import webdriver
from bs4 import BeautifulSoup
from datetime import date
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.action_chains import ActionChains
from webdriver_manager.chrome import ChromeDriverManager
import session_info


# In[2]:


session_info.show()


# ### WIP Using of proxy ip addresses

# In[3]:


# proxy = '164.100.130.128:8080'
# try:
#     r = requests.get('https://httpbin.org/ip', proxies={'http': proxy, 'https': proxy}, timeout=3)
#     print(r.json())
# except:
#     print('failed')
#     pass


# In[4]:


def settings():
    #%reset -f
    today = date.today()
    ### connect to the webpage
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    driver.get("https://www.99.co/singapore/sale/condos-apartments")
    locations_dict = {}
    return today, driver, locations_dict


# ## Get locations for the each location
# set your locations in the locations.yaml file
# example
# 
# locations:
#   - kovan:
#     - url: 'https://www.99.co/singapore/sale?autocom=false&enquiry_destination=Search%20Map&isFilterUnapplied=false&listing_type=sale&main_category=condo&map_bounds=1.337677%2C103.877125%2C1.380978%2C103.90737&marker_query_ids=adgRrXqqZgoSRdmHGT5FMqm8&marker_query_type=cluster&name=161C%20Tampines%20Road&page_num=1&page_size=35&property_segments=residential&query_coords=1.36183734450573%2C103.892547448029&query_ids=de9DDoU9YzNLMWMpHwK45B3A&query_limit=radius&query_type=cluster&radius_max=1000&rental_type=&show_cluster_preview=true&show_description=true&show_future_mrts=true&show_internal_linking=true&show_meta_description=true&show_nearby=true&show_new_listings=true&sort_field=floorarea_ppsf&sort_order=asc&sub_categories=generic_condo&zoom=16'

# In[5]:


def import_yaml(locations_dict):
    with open('./locations.yaml', 'r') as file:
        location_file = yaml.safe_load_all(file)
        for location in location_file:
            locations = location['locations']
    return locations


# In[6]:


def listContainers():
    link_list = []
    name_list = []
    address_list = []
    district_list = []
    leasehold_list = []
    property_type_list = []
    year_list = []
    rooms_list = []
    price_list = []
    bathrooms_list = []
    pricepsf_list = []
    sqf_list = []
    datestamp_list = []
    return link_list, name_list, address_list, district_list, leasehold_list, property_type_list, year_list,rooms_list, price_list, bathrooms_list, pricepsf_list, sqf_list, datestamp_list


# ## loop over all the available pages, and extract information

# In[7]:


def scrape(driver):
    link_list, name_list, address_list, district_list, leasehold_list, property_type_list, year_list,rooms_list, price_list, bathrooms_list, pricepsf_list, sqf_list, datestamp_list = listContainers()
    
    pagenum = 1
    action = ActionChains(driver)

    while True:
        my_page = driver.page_source
        my_html = BeautifulSoup(my_page, "html.parser") # get html

        containers = my_html.find_all('div', {'data-testid':'searchListingItem'})

        for i in range(len(containers)):
            #print(containers[i])

            try: # link
                link = containers[i].findAll('a', {'class':'_3Ajbv'})[0].get('href')
                # print('link', link)
            except:
                link = 'unknown'

            try: # name
                name_ = containers[i].findAll('a', {'class':'_1vzK2'})[0].text.split('in', 1)
                name = name_[1]
            except:
                name = 'unknown'

            try: # Address
                address_district = containers[i].findAll('span', {'class':'_3xhkj'})[0].text.split('·')
                address = address_district[0]
            except:
                address = 'unknown'

            try: # district
                address_district = containers[i].findAll('span', {'class':'_3xhkj'})[0].text.split('·')
                district = address_district[1]
            except:
                district = 'unknown'

            try: # leasehold
                leasehold_property_type_year = containers[i].findAll('div', {'class':'_3hW-E'})[0].text
                leasehold_property_type_year_regex = re.findall('\d*\D+',leasehold_property_type_year)
                leasehold = leasehold_property_type_year.split('·')[1]

            except:
                leasehold = 'unknown'

            try: # property_type
                leasehold_property_type_year = containers[i].findAll('div', {'class':'_3hW-E'})[0].text
                leasehold_property_type_year_regex = re.findall('\d*\D+',leasehold_property_type_year)
                property_type = leasehold_property_type_year_regex[0]
            except:
                leasehold = 'unknown'

            try: # year
                leasehold_property_type_year = containers[i].findAll('div', {'class':'_3hW-E'})[0].text
                leasehold_property_type_year_regex = re.findall('\d*\D+',leasehold_property_type_year)
                year_lease_list = leasehold_property_type_year_regex[1].split('·')
                year = year_lease_list[0]
            except:
                year = 'unknown'

            try: # rooms
                for n in containers[i].findAll('div', {'class':'cUjn9'}):
                    rooms = n.findAll('p')[0].text
            except:
                rooms = 'unknown'

            # price,bathrooms,price_psf,sqf_list
            try: # price
                price_psf_list = containers[i].findAll('div', {'class':'_3XjHl'})[0].text.split('$')
                if price_psf_list[0] == 'Make an offer':
                    pass
                price = ('$' + price_psf_list[1])
            except:
                price = 'unknown'
            
            try: # bathrooms
                for n in containers[i].findAll('div', {'class':'cUjn9'}):
                    bathrooms = n.findAll('p')[1].text
            except:
                bathrooms = 'unknown'
            
            try: # pricepsf
                price_psf_list = containers[i].findAll('div', {'class':'_3XjHl'})[0].text.split('$')
                if price_psf_list[0] == 'Make an offer':
                    pass
                pricepsf = ('$' + price_psf_list[2])
            except:
                pricepsf = 'unknown'
            
            try: # sqf
                for n in containers[i].findAll('div', {'class':'cUjn9'}):
                    sqft_list = n.findAll('p')[2].text
                sqf = sqft_list.split('/')[0]
            except:
                sqf = 'unknown'

            try: # datestamp
                scrape_date = date.today()
            except:
                scrape_date = 'unknown'
            
            link_list.append(link)
            name_list.append(name)
            address_list.append(address)
            district_list.append(district)
            leasehold_list.append(leasehold)
            property_type_list.append(property_type)
            year_list.append(year)
            rooms_list.append(rooms)
            price_list.append(price)
            bathrooms_list.append(bathrooms.replace('\xa0',''))
            pricepsf_list.append(pricepsf.strip())
            sqf_list.append(sqf)
            datestamp_list.append(scrape_date)
        
        pagenum += 1
        random_sleep = random.randint(2, 3)
        sleep(random_sleep)

        btn_page = driver.find_element(By.CLASS_NAME, "SearchPagination-links")
        action.move_to_element(btn_page)
        action.perform()
        try:
            button_disabled = driver.find_elements(By.CSS_SELECTOR, "li.next.disabled")
            # print(button_disabled)
            if len(button_disabled)==1:
                raise Exception('No more next page')

            # driver.find_element_by_link_text("Next").click()
            driver.find_element(By.CLASS_NAME, "next").click()
            print('Page:', pagenum)

        except:
            print('FINAL -- No more next page')
            break
    print('End of loop')


    updated_link_list = []
    for link in link_list:
        # print(type(link))
        updated_link = 'https://www.99.co'+link
        updated_link_list.append(updated_link)

    # Put lists into df
    df = pd.DataFrame({'name': pd.Series(name_list, dtype = 'object'),
                   'address': pd.Series(address_list, dtype = 'object'),
                   'district': pd.Series(district_list, dtype = 'object'),
                   'leasehold': pd.Series(leasehold_list, dtype = 'object'),
                   'property_type': pd.Series(property_type_list, dtype = 'object'),
                   'year': pd.Series(year_list, dtype = 'object'),
                   'rooms': pd.Series(rooms_list, dtype = 'object'),
                   'price': pd.Series(price_list, dtype = 'object'),
                   'bathrooms': pd.Series(bathrooms_list, dtype = 'object'),
                   'price_psf': pd.Series(pricepsf_list, dtype = 'object'),
                   'sqf_list': pd.Series(sqf_list, dtype = 'object'),
                   'link': pd.Series(updated_link_list, dtype = 'object'),
                   'scrape_date': pd.Series(datestamp_list, dtype = 'object'),
    })

    return df


# In[8]:


def main():
    today, driver, locations_dict = settings()
    locations = import_yaml(locations_dict)
    for location, value in locations.items():
        url = value['url']
        driver.get(url)
        # begin scrape
        print(f'BEGIN SCRAPE FOR {location}')
        df = scrape(driver)
        df.to_csv(f'{location}_listings_{today}.csv', index=False)
        print(f'END SCRAPE FOR {location}******************\n')
        random_sleep = random.randint(1, 2)
        sleep(random_sleep)
    print('\nJob is complete')
main()