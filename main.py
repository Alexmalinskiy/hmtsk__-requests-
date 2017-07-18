import os
import os.path
import requests


def get_file_translate(from_lang, to_lang, text):
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
    :param from_lang: <str> lang translated from.
    :param to_lang: <str> lang translated to.
    :param text: <str> text for translation.
    """
    url = 'https://translate.yandex.net/api/v1.5/tr.json/translate'
    key = 'trnsl.1.1.20161025T233221Z.47834a66fd7895d0.a95fd4bfde5c1794fa433453956bd261eae80152'

    params = {
        'key': key,
        'lang': from_lang + '-' + to_lang,
        'text': text,
    }
    response = requests.get(url, params=params).json()
    return ' '.join(response.get('text', []))


def get_file_text(file):
    with open(file, 'r', encoding='utf8') as f:
        text = f.read()
    lang = os.path.splitext(file)[0]
    return text, lang


def write_file_translation(new_file, new_text):
    with open(new_file, 'w', encoding='utf8') as f:
        f.write(new_text)
    print('File with translation {0} has been written successfully'.format(new_file))


def get_txt_files_for_translation():
    files = []
    for file in os.listdir(os.path.abspath(os.path.dirname(__file__))):
        extension = os.path.splitext(file.lower())[1]
        if extension == ".txt":
            files.append(file)
    return files


def main_func(to_lang):
    files = get_txt_files_for_translation()
    for file in files:
        file_text, from_lang = get_file_text(file)
        trans_text = get_file_translate(from_lang, to_lang, file_text)
        write_file_translation(file.replace(from_lang, from_lang.lower() + "-" + to_lang), trans_text)


if __name__ == '__main__':
    main_func('ru')

