import pandas as pd
import requests
from bs4 import BeautifulSoup as bs

import re

property_data = []

base_url = "https://www.ouestfrance-immo.com/immobilier/vente/maison/la-foret-fouesnant-29-29057/16044089.htm"

response = requests.get(base_url)
soup = bs(response.content, 'html.parser')

dept_div = soup.find('div', attrs={'id':'refMenuDescriptif'})
extract_dept = dept_div.get_text(strip=True)
dept = re.findall(r"\(\s*\+?(-?\d+)\s*\)", extract_dept)
property_data.append(int(dept[0]))


cost_div = soup.find('span', attrs={'class':"prix hidden-phone"})
property_data.append(cost_div.get_text(strip=True).replace("\xa0", ""))

livingarea_divs = soup.find('ul', attrs={'class':"colGAnn"})

for li in livingarea_divs.find_all('li'):
    span = li.find('span',attrs={'class':"title"})
    if (span != None) and (span.get_text(strip=True)) == 'Surf. habitable':
        living_area = li.find('strong').get_text(strip=True)
        property_data.append(living_area)

for li in livingarea_divs.find_all('li'):
    span = li.find('span',attrs={'class':"title"})
    if (span != None) and (span.get_text(strip=True)) == 'Surf. terrain':
        whole_area = li.find('strong').get_text(strip=True)
        property_data.append(whole_area)

date_div = soup.find('span', attrs={'class':"date"})
property_data.append(date_div.get_text(strip=True))

index_cols = ['Department','Price','Living Area','Ground Area','Date']
df = pd.DataFrame(columns=index_cols)
df = df.append(pd.DataFrame([property_data],columns=index_cols),ignore_index=True)
print(df)

#print(property_data)