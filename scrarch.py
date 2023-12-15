
import requests
from bs4 import BeautifulSoup

YouTube_trending_URL = 'https://www.youtube.com/feed/trending'

response = requests.get(YouTube_trending_URL)
print('Status Code:', response.status_code)
#print('Output',response.text[:1000])

with open('trending.html', 'w') as f:
  f.write(response.text)

doc = BeautifulSoup(response.text, 'html.parser')

print("page title: ", doc.title.text)

#find all the video divs

video_divs = doc.find_all('div', class_='ytd-video-renderer')
print(f'found {len(video_divs)} videos')