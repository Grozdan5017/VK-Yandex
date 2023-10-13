from datetime import datetime
import os
import requests
from dotenv import load_dotenv

dotenv_path = os.path.join('.env')

if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)


class VkUser:
    url = 'https://api.vk.com/method/'

    def __init__(self, user_id, version='5.131'):
        self.user_id = user_id
        self.version = version
        self.params = {
            'access_token': os.environ.get('TOKEN_VK'),
            'v': self.version
        }

    def get_photos(self, count=None, album_id='profile'):
        """
        Метод получает количество лайков и URL фотографий
        Возвращает dict {likes: {url: size}}
        """

        photos_url = self.url + 'photos.get'
        photos_params = {
            'owner_id': int(self.user_id),
            'album_id': album_id,
            'extended': 1,
            'count': count,
            'rev': 1
        }
        res = requests.get(photos_url, params={**self.params, **photos_params}).json()
        if 'error' in res:
            if res['error']['error_code'] == 200:
                return '403'
            else:
                return '-1'
        elif len(res['response']['items']) == 0:
            return '204'

        #  Получение url фотографий в макс. размере
        photo_url_dict = {}
        for photo in res['response']['items']:
            photo_url = photo['sizes'][-1]['url']
            likes = photo['likes']['count']
            size = photo['sizes'][-1]['type']
            if likes not in photo_url_dict:
                photo_url_dict[likes] = {photo_url: size}
            else:
                photo_url_dict[f"{likes}_{datetime.today().strftime(f'%Y%m%d')}"] = {photo_url: size}
        return photo_url_dict
