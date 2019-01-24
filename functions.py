import requests
from bs4 import BeautifulSoup as bs
import pandas as pd
from lxml.html import fromstring
import random
import time
import numpy as np


def get_proxies(number):

    free_proxy_urls = ['https://www.us-proxy.org/', 'https://free-proxy-list.net/']
    proxy_list = list()

    for every_url in free_proxy_urls:
        source = requests.get(every_url)
        parser = fromstring(source.text)

        for i in parser.xpath('//tbody/tr')[:number]:
            if i.xpath('.//td[7][contains(text(),"yes")]'):
                proxy = ":".join([i.xpath('.//td[1]/text()')[0], i.xpath('.//td[2]/text()')[0]])
                proxy_list.append(proxy)
    return proxy_list

def try_each_proxy(each_page, proxy):
    
    print ('Using proxy: ', proxy)

    page = requests.get(each_page, proxies={"http": proxy, "https": proxy})
    soup = bs(page.content, 'html.parser')
    each_page_with_links = soup.find_all('div',{'class':'company g_0'})

    return each_page_with_links

def get_all_city_links(industry):

    cities = ['manila', 'quezon-city', 'taguig']
    base_url  = 'https://www.businesslist.ph/category/'
    link_for_each_city = []
    all_pages = []
    proxies = get_proxies(500)

    for city in cities:
        link_for_each_city.append(base_url + industry + '/city:' + city +'/')

    for each_city in link_for_each_city:
        done = False
        while done == False:
            proxy = random.choice(proxies)
            try:
                page = requests.get(each_city, proxies={"http": proxy, "https": proxy})
                soup = bs(page.content, 'html.parser')
                text_in_page = soup.find('div', {'class':'pages_container_top'}).text
                number_in_text = ''

                for letters in text_in_page:
                    if letters in ['0','1','2','3','4','5','6','7','8','9']:
                        number_in_text += letters
                number_of_results = int(number_in_text)
                number_of_pages = int(np.ceil(number_of_results / 20))
                print ('Total number of Pages are: ', number_of_pages)

                for every_page in range(1,number_of_pages+1):
                    all_pages.append(each_city + str(every_page))
                done = True
            except:
                print ("Retrying...")
                proxy = random.choice(proxies)
    return all_pages

def link_get(count, list_of_pages, industry):
    all_links = []

    for each_page in list_of_pages:
        finished = False
        while finished == False:
            proxies = get_proxies(500)
            proxy = random.choice(proxies)
            try:
                each_page_with_links = try_each_proxy(each_page, proxy)
                base_url = 'https://www.businesslist.ph'
                for links in each_page_with_links:
                    link = base_url + (links.find('a').get('href'))
                    all_links.append(link)
                    finished = True
            except:
                print ('Failed: Trying another proxy.')

        df = pd.DataFrame(all_links, columns=["column"])
        count += 1
        print ('Scrape Successful.... Adding to CSV.')

        if count == 1:
            df.to_csv(industry + '.csv', index=False)
        else:
            with open(industry + '.csv', 'a') as f:
                df.to_csv(f, header=False, index = False)
        time.sleep(3)
        print (f"{count} is done")

    return count
