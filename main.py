import requests
from bs4 import BeautifulSoup
import pandas as pd

proxies = {
  "http": "http://10.10.1.10:3128",
  "https": "https://10.10.1.10:1080",
}

url = 'https://bikroy.com/en/ads/bangladesh/property'
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}

r = requests.get(url, headers=headers)

soup = BeautifulSoup(r.text, 'html.parser')

data = {'Title': [], 'Price': [], "Address": [], 'Bedrooms': [], 'Bathrooms': [], 'Size': [], 'Facing': [], 'Completion status': [], 'Land share': [], 'Description': []}

# print(soup.prettify())
a = soup.select('a.card-link--3ssYv.gtm-ad-item')

for link in a:
    href = link.get('href')
    if href:
      url = f'https://bikroy.com{href}'
      r = requests.get(url)
      
      soup_1 = BeautifulSoup(r.text, 'html.parser')

      titles = soup_1.select('h1.title--3s1R8')
      prices = soup_1.select('div.amount--3NTpl')
      property_infos = soup_1.select('div.word-break--2nyVq.value--1lKHt')
      property_titles= soup_1.select('div.word-break--2nyVq.label--3oVZK')
      description = soup_1.find(class_='description--1nRbz')

      for title in titles:
        data['Title'].append(title.text)

      for price in prices:
        data["Price"].append(price.text)

      for property_info, property_title in zip(property_infos, property_titles):  
          title_text = property_title.text.strip().lower()
          info_text = property_info.text.strip()
          
          if title_text == 'address:':
              data['Address'].append(info_text)
          elif title_text == 'bedrooms:':
              data['Bedrooms'].append(info_text)
          elif title_text == 'bathrooms:':
              data['Bathrooms'].append(info_text)
          elif title_text == 'size:':
              data['Size'].append(info_text)
          elif title_text == 'facing:':
              data['Facing'].append(info_text)
          elif title_text == 'completion status:':
              data['Completion status'].append(info_text)
          else:
              data['Land share'].append(info_text)

      if description is not None:
        p_tag = description.find_all('p')
        description_text = ""
        for p in p_tag:
            description_text += p.text + "\n"
        data['Description'].append(description_text)
      else:
        data['Description'].append("No description available")
      
      


for i in range(len(data['Land share'])):
    try:
        print(f"Title: {data['Title'][i]}\n\nPrice: {data['Price'][i]}\n\nAddress: {data['Address'][i]}\nBedrooms: {data['Bedrooms'][i]}\nBathrooms: {data['Bathrooms'][i]}\nSize: {data['Size'][i]}\nFacing: {data['Facing'][i]}\nCompletion status: {data['Completion status'][i]}\nLand share: {data['Land share'][i]}\n\nDescription:\n\n{data['Description'][i]}\n\n")
    except IndexError:
        pass

# df = pd.DataFrame.from_dict(data)
# df.to_excel('data.xlsx', index=False)