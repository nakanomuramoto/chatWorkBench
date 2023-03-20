import requests
import json

def translate(key, text, target_lang):
    url = "https://api-free.deepl.com/v2/translate"
    params = {
        "auth_key": "e8967030-1822-a6bb-a532-157a9111a3c2:fx",
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

def checkRate(key):
    url = "https://api-free.deepl.com/v2/usage"
    payload = {
        "auth_key": key,
    }
    response = requests.get(url, params=payload)
    data = response.json()
    print(data)
    current_usage_rate = data["character_count"] / data["character_limit"]

    return current_usage_rate

if __name__ == '__main__':

    with open('..\\keyDeepL.txt', 'r') as f:
        keyDeepL = f.read().strip()

    text = input("翻訳したいテキストを入力してください: ")
    target_lang = input("翻訳後の言語を入力してください (例: JA): ")
    translated_text = translate(keyDeepL, text, target_lang)
    print(translated_text)

    print(f"Current usage rate: {checkRate(keyDeepL):.2%}")

