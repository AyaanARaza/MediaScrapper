import os
import requests # type: ignore
from bs4 import BeautifulSoup # type: ignore
from urllib.parse import urljoin, urlparse

url = input("Url: ")

if not os.path.exists("downloaded_media"):
    os.makedirs("downloaded_media")

response = requests.get(url)
if response.status_code == 200:
    soup = BeautifulSoup(response.content, 'html.parser')
    media_tags = soup.find_all(['img', 'video', 'source'])    
    for i, tag in enumerate(media_tags):
        if 'src' in tag.attrs:
            media_url = urljoin(url, tag['src'])
            parsed_url = urlparse(media_url)
            media_name = os.path.basename(parsed_url.path)
            if not media_name:
                media_name = f'media_{i + 1}'
            try:
                media_data = requests.get(media_url).content
                media_path = os.path.join("downloaded_media", media_name)
                with open(media_path, 'wb') as handler:
                    handler.write(media_data)
                print(f"Downloaded {media_path}")
            except Exception as e:
                print(f"Failed to download {media_url}. Error: {e}")
else:
    print(f"Failed. Status code: {response.status_code}")