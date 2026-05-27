import requests
import pandas as pd
import os  
import time
import urllib.request
from urllib.request import urlopen
from urllib.error import URLError, HTTPError
import numpy as np

#Make request
url = 'https://www.aucklandmuseum.com'
response = requests.get(url)
response.text

#See status code
response.status_code

api_url = 'http://api.aucklandmuseum.com/search'
endpoint = '/collectionsonline/_search'
url = api_url+endpoint

#Query about bear
params = {'q': 'fish'}

#Stick them together into one long url and make the GET request
response = requests.get(url, params=params)
print("URL:", response.url)
print("STATUS:", response.status_code)

response.text

#check out the json
fishes_json = response.json()
fishes_json 

#See all the top level keys
fishes_json.keys()

#The items are located inside a list inside the records keyword. Let's look at the first item in this list!
artwork = fishes_json["hits"]
artwork

#using pandas, we can use json_normalize to put our data into a dataframe! 
#the API offers another way to display the data in a dataframe: check the documentation on how it's done
df = pd.json_normalize(fishes_json["hits"]["hits"])
df

#just keep columns we want – we will only need the systemNumber and _iiif_image_base_url for this task
df = df[['_index','_id']]
#get rid of nan rows just in case
df = df.dropna()
#give the image column a nicer name 
df = df.rename(columns={'_index':'index','_id':'id'})
df

#now the image links are working
df['id'][0]

### Helper functions

#this returns a list of tuples of object ID and their image URls
def merge(list1, list2):    
    merged_list = [(list1[i], list2[i]) for i in range(0, len(list1))]
    return merged_list

#this downloads the images and gives them the object ID as a file name
def download_image(img_list, file_path):
    filename = '{}.jpg'.format(img_list[0])
    fullpath = '{}{}'.format(file_path, filename)
    try: 
        urllib.request.urlretrieve(img_list[1], fullpath) 
    except URLError:
        print(f"Error downloading: {img_list[0]}")
        errorlist.append(img_list[0])
    except:
        print(f"Error downloading: {img_list[0]}")
        errorlist.append(img_list[0])

#this returns a list of tuples of object ID and their image URls
id_url = df['id'].to_list()
id_id = df['index'].to_list()
id_list = merge(id_id, id_url)

#make directory to put images into
directory = "fishes"
file_path = os.path.join(r"C:\\Users\\62704\\Documents\\GitHub\\intro-to-ds-24-25-Yinshu_Lu\\data", directory + "/")  
os.mkdir(file_path)  

#download images, BE CAREFUL about how many images you have! i'd suggest to stop at 100. simply index image_list like so: image_list[:n]

#the errorlist flags what images did not download for whatever reason
errorlist= []

t1 = time.perf_counter()

for url in id_list:
    download_image(url, file_path)
        
t2 = time.perf_counter()

print(f'Finished in {t2-t1} seconds')