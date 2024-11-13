import requests
import os

PEXEL_API_URL = "https://api.pexels.com/v1/search"

def download_image_from_url(timed_url: list[tuple[float, str]], path_folder: str):
    try:
        os.makedirs('./temp')
    except FileExistsError:
        pass

    for time, url in timed_url:
        print(f"Download image from {url}")
        file_type = url.split('.')[-1]
        res = requests.get(url)

        path = f"{path_folder}/{int(time * 1000)}.{file_type}"

        with open(path, "wb") as image:
            image.write(res.content)

def get_image_urls(words: list[tuple[float, str]]) -> list[tuple[float, str]]:
    headers = {
        'Authorization': os.environ['PEXEL_API_KEY']
    }

    image_sources = []

    for time, word in words:
        print(f"Getting URL for {word}")
        params = {
            'query': word,
            'per_page': 8,
            'orientation': 'landscape',
            'locale': 'en-US',
            'size': 'large'
        }

        response = requests.get(
            PEXEL_API_URL,
            headers=headers,
            params=params
        ) 

        if response.status_code != 200:
            print(f"Something went wrong when search for: {word}")
            continue 

        #Get random but predictable image
        image_url = response.json()['photos'][int(time * 1000) % 8]['src']['original']
        image_sources.append((time, image_url)) 

    return image_sources
