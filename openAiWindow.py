import sys
import openai

import re

import dearpygui.dearpygui as dpg

WIDTH, HEIGHT = 1440, 720
WIDTH1, HEIGHT1 = 700, 640
WIDTH2, HEIGHT2 = WIDTH1, 240
WIDTH3, HEIGHT3 = 690, 640
WIDTH4, HEIGHT4 = WIDTH1, 20

POSX1, POSY1 = 10, 10
POSX2, POSY2 = 10, POSY1 + HEIGHT1 + 10
POSX3, POSY3 = 10 + WIDTH1 + 10, 10
POSX4, POSY4 = 10, 10

POSX5, POSY5 = 50, 100
POSX6, POSY6 = 10, 100 + HEIGHT2 + 10

SEQUENCENUMMAX = 9

class AIChat:

    # messages=[
    #     {"role": "system", "content": "You are the best python script programmer in the world."},    
    #     # {"role": "system", "content": "You are the best programmer in the world."},    
    #     {"role": "user", "content": user_input}]

    def __init__(self, key):
        openai.api_key = key

        self.systemContent = ["You are the best python script programmer in the world."]
        self.userContents = []
        self.assistantContents = []

        self.messageList = [{"role": "system", "content": self.systemContent[0]}]
        self.totalTokens = 0
        self.sequenceNum = 0

    def response(self, user_input):
        self.messageList.append({"role": "user", "content": user_input})
        print(self.messageList)

        self.userContents.append(user_input)

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            temperature=0.5,
            messages=self.messageList
        )

        a = response['choices'][0]['message']['content']
        print("assistantAnswer:", unicode_escape_sequence_to_japanese(a))

        print(response)

        return response
    
    def showText(self, sender, data):
        inputLabel = "input"+str(self.sequenceNum)
        responseLabel = "response"+str(self.sequenceNum)

        dpg.configure_item(responseLabel, show=True)
        inputText=dpg.get_value(inputLabel)
        print("userInput: ", inputText)

        dpg.configure_item("nowLoading", show=True)
        # response = chatai.response(inputText)
        response = self.response(inputText)
        dpg.configure_item("nowLoading", show=False)

        a = response['choices'][0]['message']['content']
        self.assistantContents.append(a)

        # a.replace('\\u3002', '\\u3002\\n\\n')  
        responseMassage = unicode_escape_sequence_to_japanese(a)


        if self.sequenceNum < SEQUENCENUMMAX : 
            self.messageList.append({"role": "assistant", "content": a})

            tabLabel = "#"+str(self.sequenceNum)
            dpg.configure_item(tabLabel, show=True)

        if '```python' in a :
            idStart = a.find('```') + 3
            idEnd = a.find('```', idStart+4) 
            code1 = a[idStart:idEnd]

            dpg.set_value("code1", code1)

            responseMassage = a[:idStart] + "  右の窓に抜粋  " + a[idEnd:] 

        status = response['choices'][0]['finish_reason']
        index_num = response['choices'][0]['index']
        role = response['choices'][0]['message']['role']

        incTotalTokens = int(response['usage']['total_tokens'])
        total_tokens = self.incrementTokens(incTotalTokens)
        dpg.set_value("totalToken", "total Tokens = " + str(total_tokens))

        print(status, ", sequenceNum: ", self.sequenceNum, ", id: ", index_num, ", role: ", role, ", total tokens: ", total_tokens, "\n")

        print("before:", responseMassage)

        # # \u3002
        # responseMassage.replace('\\u3002', '\\u3002\\n')  
        responseMassage = responseMassage.replace('。', '。\n')
        responseMassage = responseMassage.replace('.', '.\n')

        print("after:", responseMassage)

        dpg.set_value(responseLabel, responseMassage)

        self.sequenceNum += 1
        tabLabel = "#"+str(self.sequenceNum)
        print(tabLabel)
        dpg.configure_item(tabLabel, show=True)
        dpg.set_value("TabBars", tabLabel)
        

    def getTotalTokens(self):
        return self.totalTokens

    def incrementTokens(self, addTokens):
        self.totalTokens += addTokens
        return self.totalTokens

    def getSequenceNum(self):
        return self.sequenceNum

def unicode_escape_sequence_to_japanese(text):
    pattern = re.compile(r'\\\\u([0-9a-fA-F]{4})')
    return pattern.sub(lambda x: chr(int(x.group(1), 16)), text)

def show_message():
    dpg.configure_item("response0", show=True)
    dpg.set_value("response0", "Button clicked!")

def copyCodeAll(sender, app_data, user_data):
    getCode = dpg.get_value("code1")
    dpg.set_clipboard_text(getCode)

def selectable_callback(sender, data):
    dpg.configure_item(sender, selectable=True)

def main():
    print('>> AIChat: see you ')

if __name__ == '__main__':
    # main()

    with open('key.txt', 'r') as f:
        key = f.read().strip()

    chatai = AIChat(key)

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

    def on_text_changed(sender, data):
        print(dpg.get_value(sender))

    with dpg.window(width=WIDTH1, height=HEIGHT1, label="UserInput and Assistant", tag="window1", pos=(POSX1, POSY1),horizontal_scrollbar=True):
        # dpg.add_input_text(label="Enter Text", callback=on_text_changed)
        # https://pythonprogramming.altervista.org/input-text-examples-in-dearpygui/

        # with dpg.group(horizontal=True):
            # dpg.add_button(label="CopyCodeAll", callback=copyCodeAll)

        with dpg.group(horizontal=True):
            dpg.add_button(label="Send", callback=chatai.showText)
            dpg.add_loading_indicator(tag="nowLoading", style=1, radius=1.5, thickness=1.5, show=False)

        # タブバーを作成
        with dpg.tab_bar(label="TabBars", tag="TabBars"):

            for i in range(10) :
                tabLabel = "#"+str(i)
                inputLabel = "input"+str(i)
                responseLabel = "response"+str(i)

                isShowTab = chatai.getSequenceNum() >= i
                # タブ1を作成
                with dpg.tab(label=tabLabel, tag=tabLabel, show=isShowTab):
                    # dpg.add_text("This is Tab 1")
                    dpg.add_input_text(tag=inputLabel, width=WIDTH, height=HEIGHT2, pos=(POSX5, POSY5), multiline=True, tracked=True, default_value="")
                    dpg.add_input_text(tag=responseLabel, width=WIDTH-50, pos=(POSX6, POSY6), height=HEIGHT2, multiline=True, tracked=True, default_value="")
                
                # # タブ2を作成
                # with dpg.tab(label="#2"):
                #     # dpg.add_text("This is Tab 2")
                #     pass

        # dpg.add_input_text(tag="input1", width=WIDTH, height=HEIGHT2, multiline=True, tracked=True, default_value="")
        # dpg.add_input_text(tag="response0", width=WIDTH, height=HEIGHT2, multiline=True, tracked=True, default_value="")

        dpg.add_text(tag="totalToken", default_value="total Tokens = " + str(chatai.getTotalTokens()))
        
    # with dpg.window(width=WIDTH2, height=HEIGHT2, label="Assistant", tag="window2", pos=(POSX2, POSY2),horizontal_scrollbar=True):
    #     # dpg.add_text("Hello, World!", tag="response0", wrap=300, show=False, drag_callback=selectable_callback)
    #     dpg.add_input_text(tag="response0", width=WIDTH, height=HEIGHT1-100, multiline=True, tracked=True, default_value="")
    #     dpg.add_button(label="Click me", callback=show_message)

    with dpg.window(width=WIDTH3, height=HEIGHT3, label="AssistantCode", tag="window3", pos=(POSX3, POSY3),horizontal_scrollbar=True):
        dpg.add_input_text(tag="code1", width=WIDTH, height=HEIGHT3-100, multiline=True, tracked=True, default_value="")
        dpg.add_button(label="CopyCodeAll", callback=copyCodeAll)

    # with dpg.window(width=WIDTH4, label="Sequence", tag="qaSequence", pos=(POSX4, POSY4), no_title_bar=True, no_move=True):
    #     # dpg.add_input_text(tag="code1", width=WIDTH, height=HEIGHT3-100, multiline=True, tracked=True, default_value="")
    #     with dpg.group(horizontal=True):
    #         dpg.add_text(tag="totalToken", default_value="total Tokens = " + str(chatai.getTotalTokens()))
    #         dpg.add_button(label="CopyCodeAll", callback=copyCodeAll)

    dpg.setup_dearpygui()
    dpg.show_viewport()
    dpg.start_dearpygui()
    dpg.destroy_context()
    