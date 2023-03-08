import openai

class AIChat:
    def __init__(self, key):
        openai.api_key = key

    def response(self, user_input):
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            temperature=0.0,
            messages=[
                # {"role": "system", "content": "You are the best shell script programmer in the world."},
                {"role": "user", "content": user_input}]
        )

        # print(response['choices'][0]['message']['content'])
        # return response['choices'][0]['message']['content']

        a = response['choices'][0]['message']['content']
        b = a.replace("\n","")
        # s_from_b = s_from_b_error.encode().decode('unicode-escape')
        print(b)

        return response

def main():

    with open('key.txt', 'r') as f:
        key = f.read().strip()

    chatai = AIChat(key)

    while True:
        # ユーザーからの入力を受け取る
        user_input = input('>> User: ')

        # ユーザーからの入力が「終了」だった場合にプログラムを終了する
        if user_input == '終了' or user_input == 'exit' or user_input == 'おわり':
            break

        # chataiからの応答を取得する
        response = chatai.response(user_input)
        # print('>> AIChat: ' + response)
        print(response)

    print('>> AIChat: いつでもお話ししてくださいね。')

if __name__ == '__main__':
    main()

    #引数で入力したファイル名の拡張子の前の最後の4桁の数字の一番上の桁を消すシェルスクリプトと実行例を教えて下さい