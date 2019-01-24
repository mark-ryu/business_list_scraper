import requests
from bs4 import BeautifulSoup as bs
import pandas as pd
import time
import functions as scraper
import numpy as np

title = input("Enter the filename without csv extension: ")
continue_from = eval(input("Enter Row to Start from: "))
df = pd.read_csv(f"{title}-duplicates-dropped.csv")

proxies = scraper.get_proxies(500)
proxy = np.random.choice(proxies)

for each_url in df.column[continue_from:]:

    name = 'None'
    weblinks = 'None'
    telephone = 'None'
    mobile = 'None'
    number_of_employees = 'None'
    contact = 'None' 
    fax = 'None' 
    manager = 'None'
    finished = False
    number_of_tries = 1

    while finished == False:
        
        try:

            url = each_url

            print ('Trying Proxy: ', proxy)
            
            page = requests.get(url, proxies={"http": proxy, "https": proxy})
            soup = bs(page.content, 'html.parser')
            all_texts = soup.find_all('div', {'class':'label'})
            
            # print("Process time is: ", time.process_time())

            try:
                name = soup.find('span', {'id':'company_name'}).text
            except:
                name = 'None'
            try:
                weblinks = soup.find("div", class_= "text weblinks").text
            except:
                weblinks = 'None'
            try:
                telephone = soup.find('div',{'class':'text phone'}).text
            except:
                telephone = 'None'    
            try:
                for each in all_texts:
                    if each.text == 'Mobile phone':
                        mobile = each.find_next().contents[0]
            except:
                mobile = 'None'
            try:
                for each in all_texts:
                    if each.text == 'Employees':
                        number_of_employees = each.find_next().contents[0]
            except:
                number_of_employees = 'None'
            try:
                for each in all_texts:
                    if each.text == 'Contact Person':
                        contact = each.find_next().contents[0]
            except:
                contact = 'None'
            try:
                for each in all_texts:
                    if each.text == 'Fax':
                        fax = each.find_next().contents[0]
            except:
                fax = 'None'
            try:
                for each in all_texts:
                    if each.text == 'Company manager':
                        manager = each.find_next().contents[0]
            except:
                manager = 'None'

        except:

            print ('Trying another proxy...\n')
            number_of_tries += 1
            print ("No. of Tries: ", number_of_tries)

        # if the proxy is caught and returns none values
        if name == 'None':
            proxy = np.random.choice(proxies)

        else:
            finished = True
            continue_from += 1

    else:
        
        print (f'This is the scraped link: {weblinks};') 
        time.sleep(1)
        df_1 = pd.DataFrame.from_dict({'company_name':[name], 'website':[weblinks], 'telephone_no':[telephone], 'mobile_phone':[mobile], 'no._of_employees':[number_of_employees], 'contact_person':[contact], 'fax':[fax], 'company_manager':[manager]})

        if continue_from == 1:
            print (f"{continue_from}: done;")
            df_1.to_csv(f"{title}-done.csv", index = False, encoding="utf-8")

        else:
            print (f"{continue_from}: done;")
            with open(f"{title}-done.csv", 'a',  encoding="utf-8") as f:
                df_1.to_csv(f, header=False, index = False)

print ()
print ('The program is done')
