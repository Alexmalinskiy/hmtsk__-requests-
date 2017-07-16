import os
import os.path
import requests


def translate_file(from_file, to_lang, from_lang, to_file):
    """
    YANDEX translation plugin
    docs: https://tech.yandex.ru/translate/doc/dg/reference/translate-docpage/
    https://translate.yandex.net/api/v1.5/tr.json/translate ?
    key=<API-ключ>
     & text=<переводимый текст>
     & lang=<направление перевода>
     & [format=<формат текста>]
     & [options=<опции перевода>]
     & [callback=<имя callback-функции>]
    :param from_file: <str> file for translation.
    :param to_lang: <str> lang translated to.
    :param from_lang: <str> lang translated from.
    :param to_file: <str> file translation text to
    """
    url = 'https://translate.yandex.net/api/v1.5/tr.json/translate'
    key = 'trnsl.1.1.20161025T233221Z.47834a66fd7895d0.a95fd4bfde5c1794fa433453956bd261eae80152'

    with open(from_file, 'r', encoding='utf8') as file:
        params = {
            'key': key,
            'lang': from_lang + '-' + to_lang,
            'text': file.read(),
        }
        response = requests.get(url, params=params).json()
        translated = ' '.join(response.get('text', []))

    with open(to_file, 'w') as f:
        f.write(translated)


def get_files_for_translation(path):
    return [file for file in os.listdir(path) if os.path.splitext(file.lower())[1] == ".txt"]


def main_func(to_lang):
    path = os.path.abspath(os.path.dirname(__file__))
    files = get_files_for_translation(path)
    for file in files:
        translate_file(from_file=file, to_lang=to_lang, from_lang=os.path.splitext(file.lower())[0],
                       to_file=file.replace(os.path.splitext(file.lower())[1],
                                            "_transl_to_"+to_lang+os.path.splitext(file.lower())[1]))


if __name__ == '__main__':
    main_func('ru')

