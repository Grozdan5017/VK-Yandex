from src.vk import VkUser
from src.yandex_upload import YaUploader


def main():
    vk_user_id = input('enter the vk user id: ').strip()
    token_ya_disk = input('enter the token yandex disk: ').strip()
    folder_name = input('enter the folder name: ').strip()

    vk_user = VkUser(user_id=vk_user_id, version='5.131')
    data_photos = vk_user.get_photos()
    if data_photos == '403':
        print('Доступ запрещен к фотографиям пользователя')
        return
    elif data_photos == '-1':
        print('Неизвестная ошибка при получении фотографий пользователя')
        return
    elif data_photos == '204':
        print('Альбом пуст')
        return

    upload = YaUploader(token_ya_disk)
    upload.upload(folder_name=folder_name, data=data_photos)


if __name__ == '__main__':
    main()
