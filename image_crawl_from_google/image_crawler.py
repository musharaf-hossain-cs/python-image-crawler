from bs4 import *
import requests as rq
import os
from pathlib import Path

def findLinks(url):
    r1 = rq.get(url)
    soup1 = BeautifulSoup(r1.text, 'html.parser')
    links = []
    images = soup1.find_all('img')
    for img in images:
        link = img['src']
        if link.find('https://') != -1:
            links.append(link)
    # print(len(images), len(links))
    return links

def downloadImages(links, directory, name):
    path = Path(directory)
    if not os.path.exists(directory):
        path.mkdir(parents=True, exist_ok=True)
    for link in links:
        r2 = rq.get(link)
        with open(directory + '/' + name + '_' + str(links.index(link)) + '.jpg', 'wb') as f:
            f.write(r2.content)


def actor_front_facing(actors):
    for actor in actors:
        url = 'https://www.google.com/search?q=' + actor + '+front+facing' + '&source=lnms&tbm=isch'
        links = findLinks(url)
        downloadImages(links, './images/' + actor.replace(' ', '_'), actor.replace(' ', '_'))
        print(actor + ' images downloaded')

# search_item = ['dog', 'cat', 'horse', 'bird', 'fish', 'srk', 'salman khan']
# for item in search_item:
#     url = 'https://www.google.com/search?q=' + item + '&source=lnms&tbm=isch'
#     links = findLinks(url)
#     downloadImages(links, './images/' + item , item)
#     print(item + ' images downloaded')

actors = ['shah rukh khan', 'salman khan', 'amitabh bacchan', 'priyangka chopra', 'deepika padukone', 'ranbir kapoor', 'katrina kaif', 'anushka sharma']
actor_front_facing(actors)