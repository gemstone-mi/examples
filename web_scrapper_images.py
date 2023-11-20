import requests
from bs4 import BeautifulSoup
"""
https://www.youtube.com/watch?v=Al20Pyuc5Ck
"""
site_map =  "https://www.pngmart.com/sitemap.xml"
response = requests.get(site_map)
xml = (response.text)
soup = BeautifulSoup(xml, 'xml')

site_maps = []
for loc in soup.find_all('loc'):
    url = loc.text
    if 'posts' in url:
        print(loc.text)
        site_maps.append(url)
         
######
site_map_1  = site_maps[0]
response = requests.get(site_map_1)
soup = BeautifulSoup(response.text, 'xml')
 
master_list = []
for loc in soup.find_all('loc'):
    url = loc.text
    if 'image' in url:
       # print(loc.text)
        master_list.append(url)
        
# Loop through and grab the first 10 images
for image_url in master_list[0:10]:
    #print(image_url)
    response = requests.get(image_url)
    soup = BeautifulSoup(response.text, 'html.parser')
    png_url= soup.find('a',{'class':'download'})['href']
    image = requests.get(png_url)
    image_id = image_url.split('/')[-1]
    image_title = image_url.split('/')[-1]+'-'+png_url.split('/')[-1]
    
    with open (image_title,'wb') as file:
        file.write(image.content)

