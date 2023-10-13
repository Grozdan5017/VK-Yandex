import requests
from datetime import datetime
from time import sleep
from src.saved_to_json import save_to_json


class YaUploader:
    def __init__(self, token_ya):
        self.token_ya = token_ya

    def create_folder(self, folder_name):
        """Метод создает папку для загрузки файла"""
        url = 'https://cloud-api.yandex.net/v1/disk/resources/'
        headers = {'Content-Type': 'application/json',
                   'Accept': 'application/json',
                   'Authorization': self.token_ya}
        params = {'path': folder_name}
        resp = requests.put(url, params=params, headers=headers)
        if resp.status_code == 201:
            print(f'Folder {folder_name} created.')
            return folder_name
        elif resp.status_code == 409:
            params = {'path': f"{folder_name}_{datetime.today().strftime(f'%Y%m%d')}"}
            requests.put(url, params=params, headers=headers)
            print(f"Folder {folder_name}_{datetime.today().strftime(f'%Y%m%d')} created.")
            return f"{folder_name}_{datetime.today().strftime(f'%Y%m%d')}"

    def vk_upload(self, folder_name, data):
        """Метод загружает файл по URL на яндекс диск"""
        result_info = []
        url_upload = 'https://cloud-api.yandex.net/v1/disk/resources/upload'
        headers = {'Content-Type': 'application/json',
                   'Accept': 'application/json',
                   'Authorization': self.token_ya}
        count_upload = 0
        for likes, value in data.items():
            for url, size in value.items():
                file_dict = {}
                params = {
                    'path': str(folder_name) + '/' + str(likes) + '.jpg',
                    'url': url
                }
                resp = requests.post(url_upload, params=params, headers=headers)
                resp.raise_for_status()
                if resp.status_code == 202:
                    count_upload += 1
                    print(f'File {count_upload} of {len(data)} uploaded.')
                    sleep(0.33)

                    file_dict['file_name'] = str(likes) + '.jpg'
                    file_dict['size'] = size

                    result_info.append(file_dict)

        return result_info

    def upload(self, folder_name, data):
        created_folder_name = self.create_folder(folder_name=folder_name)
        saved_data_json = self.vk_upload(folder_name=created_folder_name, data=data)
        save_to_json(saved_data_json)
