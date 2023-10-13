import json


def save_to_json(data):
    try:
        with open('json.json', 'w') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

        print('json сохранен')
        return 'ok'
    except Exception as ex:
        print(f'Ошибка сохранения json. {ex}')
        return
