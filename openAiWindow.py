import sys
import openai

import dearpygui.dearpygui as dpg

POSX0, POSY0 = 10, 10
POSX1, POSY1 = 720, POSY0
WIDTH, HEIGHT = 1440, 720
WIDTH1, HEIGHT1 = 700, 500

class AIChat:
    def __init__(self, key):
        openai.api_key = key

    def response(self, user_input):
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            temperature=0.5,
            messages=[
                {"role": "system", "content": "You are the best python script programmer in the world."},    
                # {"role": "system", "content": "You are the best programmer in the world."},    
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

def show_message():
    dpg.configure_item("message1", show=True)
    dpg.set_value("message1", "Button clicked!")

def showText(sender, data):
    dpg.configure_item("message1", show=True)
    inputText=dpg.get_value("input1")

    response = chatai.response(inputText)

    a = response['choices'][0]['message']['content']
    responseMassage = unicode_escape_sequence_to_japanese(a)

    status = response['choices'][0]['finish_reason']
    index_num = response['choices'][0]['index']
    role = response['choices'][0]['message']['role']

    total_tokens = str(response['usage']['total_tokens'])

    # print(response)
    print(status, ", id: ", index_num, ", role: ", role, ", total tokens: ", total_tokens)

    dpg.set_value("message1", responseMassage)
    print(inputText)

def selectable_callback(sender, data):
    dpg.configure_item(sender, selectable=True)

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
    # main()

    with open('key.txt', 'r') as f:
        key = f.read().strip()

    chatai = AIChat(key)

    #引数で入力したファイル名の拡張子の前の最後の4桁の数字の一番上の桁を消すシェルスクリプトと実行例を教えて下さい

    dpg.create_context()

    # https://github.com/morikatron/snippet/blob/master/dear_pygui_examples/font_example.py
    # font https://fonts.google.com/noto/specimen/Noto+Sans+JP
    with dpg.font_registry():
        with dpg.font(file="./Noto_Sans_JP/NotoSansJP-Medium.otf", size=20) as default_font:
            dpg.add_font_range_hint(dpg.mvFontRangeHint_Japanese)
        dpg.bind_font(default_font)
        with dpg.font(file="./Noto_Sans_JP/NotoSansJP-Bold.otf", size=14) as small_font:
            dpg.add_font_range_hint(dpg.mvFontRangeHint_Japanese)

    dpg.create_viewport(title='openAI, gpt-3.5-turbo', width=WIDTH, height=HEIGHT)

    with dpg.window(width=WIDTH1, height=HEIGHT1, label="My Window", tag="test1", pos=(POSX0, POSY0)):
        # dpg.add_text("Hello, World!", tag="message1", wrap=300, show=False, drag_callback=selectable_callback)
        dpg.add_input_text(tag="message1", width=WIDTH1-30, height=HEIGHT1-100, multiline=True, default_value="")
        dpg.add_button(label="Click me", callback=show_message)

    def on_text_changed(sender, data):
        print(dpg.get_value(sender))

    # with dpg.font_registry():
    #     dpg.add_font("NotoSansCJKjp-Regular.otf", 20, "japanese") # default_font=True)


    with dpg.window(width=WIDTH1, height=HEIGHT1, label="Text Input", tag="w1", pos=(POSX1, POSY1)):
        # dpg.add_input_text(label="Enter Text", callback=on_text_changed)
        # https://pythonprogramming.altervista.org/input-text-examples-in-dearpygui/
        dpg.add_input_text(tag="input1", width=WIDTH1-30, height=HEIGHT1-100, multiline=True, default_value="")
        dpg.add_button(label="Send", callback=showText)

    dpg.setup_dearpygui()
    dpg.show_viewport()
    dpg.start_dearpygui()
    dpg.destroy_context()
    