import functions as scraper
import pandas as pd

identifier = False

industry = input('Enter the industry extension from url: ')
index_number = eval(input("Index Number from csv file: "))
continue_from_csv = input('Continue from CSV? Enter Yes or No as exact match: ')

while identifier == False:

    if continue_from_csv == "Yes":
        df = pd.read_csv(industry + "-city-links"+ ".csv")
        list_of_pages = df["links"][index_number:]
        scraper.link_get(index_number, list_of_pages, industry)
        identifier = True

    elif continue_from_csv == "No":
        list_of_pages = scraper.get_all_city_links(industry)
        df = pd.DataFrame({"links":list_of_pages})
        df.to_csv(industry + "-city-links"+ ".csv", index=False)
        scraper.link_get(0, list_of_pages, industry)
        identifier = True

    else:
        ("Wrong input, try again.")
        break
df = pd.read_csv(industry + '.csv')
df = df.drop_duplicates()
df.to_csv(industry + '-duplicates-dropped.csv', index=False)
"""
what is the process?

I input the industry, then it will get manila url.
At the first page, will get the number of pages and save that list to get links per page.

get all links on all cities first
save that list and then use it for getting each link per page.

"""
