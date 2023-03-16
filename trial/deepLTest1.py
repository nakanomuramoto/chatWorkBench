import requests
import json

def translate(text, target_lang):
    url = "https://api-free.deepl.com/v2/translate"
    params = {
        "auth_key": "24d88479-0606-b7ab-197e-c69616e49975:fx",
        "text": text,
        "target_lang": target_lang
    }
    response = requests.post(url, data=params)
    if response.status_code == 200:
        result = json.loads(response.content.decode('utf-8'))
        translations = result.get('translations', [])
        if len(translations) > 0:
            return translations[0].get('text', '')
    return ''

if __name__ == '__main__':
    text = input("翻訳したいテキストを入力してください: ")
    target_lang = input("翻訳後の言語を入力してください (例: JA): ")
    translated_text = translate(text, target_lang)
    print(translated_text)
