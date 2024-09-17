import requests

API_URL = "https://randomuser.me/api/"

def fetch_users(results):
    """Fetches users from Random User API."""
    response = requests.get(API_URL, params={'results': results})
    data = response.json()['results']
    return [
        {   
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
        }
        for user in data
    ]

def save_image(url, file_path):
    """Downloads an image from a URL and saves it locally."""
    response = requests.get(url)
    with open(file_path, 'wb') as image_file:
        image_file.write(response.content)
