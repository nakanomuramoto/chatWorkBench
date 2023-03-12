import sys
import openai

class AIChat:
    def __init__(self, key):
        openai.api_key = key

    def response(self, user_input):
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            temperature=0.5,
            messages=[
                {"role": "system", "content": "You are the best python script programmer in the world."},    
                {"role": "user", "content": user_input}]
        )

        # print(response['choices'][0]['message']['content'])
        # return response['choices'][0]['message']['content']

        a = response['choices'][0]['message']['content']
        # b = a.replace("\n","")
        b = unicode_escape_sequence_to_japanese(a)
        # s_from_b = s_from_b_error.encode().decode('unicode-escape')
        print(b)

        return response

import re

def unicode_escape_sequence_to_japanese(text):
    pattern = re.compile(r'\\\\u([0-9a-fA-F]{4})')
    return pattern.sub(lambda x: chr(int(x.group(1), 16)), text)

def main():

    with open('key.txt', 'r') as f:
        key = f.read().strip()

    chatai = AIChat(key)

    while True:
        # ユーザーからの入力を受け取る
        # user_input = input('>> User: ')

        print('>> User: ')
        user_input = sys.stdin.read()

        # ユーザーからの入力が「終了」だった場合にプログラムを終了する
        # if user_input == '終了' or user_input == 'exit' or user_input == 'おわり' or user_input == '' :
        if user_input == '' :
            break
        else:
            print('now loading... ')

        # chataiからの応答を取得する
        response = chatai.response(user_input)
        # print('>> AIChat: ' + response)

        status = response['choices'][0]['finish_reason']
        index_num = response['choices'][0]['index']
        role = response['choices'][0]['message']['role']

        total_tokens = str(response['usage']['total_tokens'])

        # print(response)
        print(status, ", id: ", index_num, ", role: ", role, ", total tokens: ", total_tokens)

    print('>> AIChat: いつでもお話ししてくださいね。')

if __name__ == '__main__':
    main()

    #引数で入力したファイル名の拡張子の前の最後の4桁の数字の一番上の桁を消すシェルスクリプトと実行例を教えて下さい