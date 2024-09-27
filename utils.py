import requests
import os
import asyncio
import aiohttp

API_URL = "https://randomuser.me/api/"
WEATHER_URL = "https://api.open-meteo.com/v1/forecast"

def fetch_temperature(latitude, longitude):
    """Fetches the current temperature based on latitude and longitude."""
    params = {
        'latitude': latitude,
        'longitude': longitude,
        'current': 'temperature_2m'
    }
    response = requests.get(WEATHER_URL, params=params)
    data = response.json()
    temperature = data['current']['temperature_2m']
    return temperature

def fetch_users(results):
    """Fetches users from Random User API."""
    response = requests.get(API_URL, params={'results': results})
    data = response.json()['results']
    users = []
    for user in data:
        latitude = user['location']['coordinates']['latitude']
        longitude = user['location']['coordinates']['longitude']
        temperature = fetch_temperature(latitude, longitude)
        users.append({
            # users
            'first_name': user['name']['first'],
            'last_name': user['name']['last'],
            'gender': user['gender'],
            'email': user['email'],
            'phone': user['phone'],
            'cell': user['cell'],
            'date_of_birth': user['dob']['date'],
            'age': user['dob']['age'],
            # locations
            'street_name': user['location']['street']['name'],
            'street_number': user['location']['street']['number'],
            'city': user['location']['city'],
            'state': user['location']['state'],
            'country': user['location']['country'],
            'postcode': user['location']['postcode'],
            'latitude': user['location']['coordinates']['latitude'],
            'longitude': user['location']['coordinates']['longitude'],
            'temperature': temperature,
            # logins
            'uuid': user['login']['uuid'],
            'username': user['login']['username'],
            'password': user['login']['password'],
            'salt': user['login']['salt'],
            'md5': user['login']['md5'],
            'sha1': user['login']['sha1'],
            'sha256': user['login']['sha256'],
            # pictures
            'large': user['picture']['large'],
            'medium': user['picture']['medium'],
            'thumbnail': user['picture']['thumbnail']
        })
    return users

def save_image(url, file_path):
    """Downloads an image from a URL and saves it locally."""
    response = requests.get(url)
    with open(file_path, 'wb') as image_file:
        image_file.write(response.content)

async def fetch_image(session, semaphore, url, file_path):
    async with semaphore:
        async with session.get(url) as response:
            if response.status == 200:
                with open(file_path, 'wb') as image_file:
                    image_file.write(await response.read())

async def download_images_async(image_urls, dir, max_concurrent):
    if not os.path.exists(dir):
        os.makedirs(dir)
    semaphore = asyncio.Semaphore(max_concurrent)
    async with aiohttp.ClientSession() as session:
        tasks = []
        for user_id, url in image_urls:
            file_path = os.path.join(dir, f"{user_id}.jpg")
            tasks.append(fetch_image(session, semaphore, url, file_path))
        await asyncio.gather(*tasks)