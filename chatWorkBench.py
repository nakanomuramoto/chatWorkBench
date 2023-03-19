import os
import sys

import requests
import json

import openai

import re

import pyperclip

import dearpygui.dearpygui as dpg

WIDTH, HEIGHT = 1440, 720
WIDTH1, HEIGHT1 = 700, 640
WIDTH2, HEIGHT2 = WIDTH1, 240

POSX1, POSY1 = 10, 30
POSX3, POSY3 = 10 + WIDTH1 + 10, 30

POSX5, POSY5 = 10, 100
POSX6, POSY6 = 10, 100 + HEIGHT2 + 30

SEQUENCENUMMAX = 9

class AITranslate:
    def __init__(self, key):
        self.keyDeepL = key

    def translate(self, text, target_lang):
        url = "https://api-free.deepl.com/v2/translate"
        params = {
            "auth_key": self.keyDeepL,
            "text": text,
            "target_lang": target_lang
        }
        response = requests.post(url, data=params)
        if response.status_code == 200:
            result = json.loads(response.content.decode('utf-8'))
            translations = result.get('translations', [])
            if len(translations) > 0:
                return translations[0].get('text', '')

        print(self.keyDeepL)

        return ''

class AIChat:

    # messages=[
    #     {"role": "system", "content": systemComment},    
    #     {"role": "user", "content": user_input},
    #     {"role": "assistant", "content": a}]

    def __init__(self, key, deepL) : 
        openai.api_key = key

        self.systemContent = ["You are the best python script programmer in the world. Only the Python scripts in your response should be displayed between ~~~~~~.  Show me the explanation afterwards."]
        self.userContents = []
        self.userCode = []        
        self.assistantContents = []
        self.assistantCode = []

        self.messageList = [{"role": "system", "content": self.systemContent[0]}]
        self.totalTokens = 0
        self.sequenceInputNum = 0
        self.sequenceResponseNum = 0

    def resetChat(self):
        print("log reset")
        self.systemContent = ["You are the best python script programmer in the world. Only the Python scripts in your response should be displayed between ~~~~~~.  Show me the explanation afterwards."]
        self.userContents = []
        self.userCode = []        
        self.assistantContents = []
        self.assistantCode = []

        self.messageList = [{"role": "system", "content": self.systemContent[0]}]
        
        inputLabel = "input0"
        dpg.set_value(inputLabel, "")
        dpg.configure_item(inputLabel, enabled=True)

        inputEnLabel = "input0_EN"
        dpg.set_value(inputEnLabel, "")
        dpg.configure_item(inputEnLabel, enabled=True)

        responseLabel = "response0"
        dpg.set_value(responseLabel, "")
        dpg.configure_item(responseLabel, enabled=False)

        responseJpLabel = "response0_JP"
        dpg.set_value(responseJpLabel, "")
        dpg.configure_item(responseJpLabel, enabled=False)

        self.sequenceInputNum = 0
        self.sequenceResponseNum = 0
        for i in range(SEQUENCENUMMAX + 1) :
            tabLabel = "#"+str(i)
            tabEnLabel = "#"+str(i)+"_EN"
            inputLabel = "input"+str(i)
            inputEnLabel = "input"+str(i)+"_EN"
            inputCodeLabel = "inputCode"+str(i)             

            tabAnsLabel = "#_"+str(i)
            tabJpAnsLabel = "#_"+str(i)+"_JP"
            responseLabel = "response"+str(i)
            responseJpLabel = "response"+str(i)+"_JP" 
            responseCodeLabel = "responseCode"+str(i)
            responseJpCodeLabel = "responseCode"+str(i)+"_JP"

            dpg.configure_item(tabLabel, show=(1 > i))
            dpg.configure_item(tabEnLabel, show=(0 > i))
            dpg.configure_item(tabAnsLabel, show=(0 > i))
            dpg.configure_item(tabJpAnsLabel, show=(0 > i))

            dpg.set_value(inputLabel, "")
            dpg.configure_item(inputLabel, enabled=True)
            dpg.set_value(inputEnLabel, "")
            dpg.configure_item(inputEnLabel, enabled=True)

            dpg.set_value(inputCodeLabel, "")
            dpg.set_value(responseLabel, "")
            dpg.set_value(responseJpLabel, "")
            dpg.set_value(responseCodeLabel, "")
            dpg.set_value(responseJpCodeLabel, "")

        self.totalTokens = 0
        dpg.set_value("totalToken", "total Tokens = " + str(self.totalTokens))


    def response(self, user_input):
        self.messageList.append({"role": "user", "content": user_input})
        print(self.messageList)

        self.userContents.append(user_input)

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo", # "gpt-4",
            temperature=0.5,
            messages=self.messageList
        )

        a = response['choices'][0]['message']['content']
        # print("assistantAnswer:", unicode_escape_sequence_to_japanese(a))

        print(response)

        return response
    
    def SendMessageToOpenAI(self, sender, data):
        inputLabel = "input"+str(self.sequenceInputNum)
        inputText=dpg.get_value(inputLabel)

        if(inputText == ""):
            return
        else:    
            inputEnLabel = "input"+str(self.sequenceInputNum)+"_EN"

            if dpg.get_value(inputEnLabel) != "":
                inputText = dpg.get_value(inputEnLabel)

            inputCodeLabel = "inputCode"+str(self.sequenceInputNum) 

            # inputText=dpg.get_value(inputLabel)
            inputCode=dpg.get_value(inputCodeLabel)
            inputText += inputCode
            print("userInput: ", inputText)

            dpg.configure_item("nowLoading", show=True)
            response = self.response(inputText)
            dpg.configure_item("nowLoading", show=False)

            a = response['choices'][0]['message']['content']
            self.assistantContents.append(a)

            responseMassage = unicode_escape_sequence_to_japanese(a)

            self.sequenceResponseNum = self.sequenceInputNum
            responseLabel = "response"+str(self.sequenceResponseNum)
            responseCodeLabel = "responseCode"+str(self.sequenceResponseNum)
            dpg.configure_item(responseLabel, show=True)

            if self.sequenceInputNum < SEQUENCENUMMAX : 
                self.messageList.append({"role": "assistant", "content": a})

                tabLabel = "#"+str(self.sequenceInputNum)
                dpg.configure_item(tabLabel, show=True)

            if '~~~~~~' in a :
                idStart = a.find('~~~~~~') + 6
                idEnd = a.find('~~~~~~', idStart+4) 
                code1 = a[idStart:idEnd]

                print("code ", code1)
                dpg.set_value(responseCodeLabel, code1)
                self.assistantCode.append(code1)

                responseMassage = a[:idStart] + "  下の窓に抜粋  " + a[idEnd:] 
            else:
                self.assistantCode.append("")

            status = response['choices'][0]['finish_reason']
            index_num = response['choices'][0]['index']
            role = response['choices'][0]['message']['role']

            incTotalTokens = int(response['usage']['total_tokens'])
            total_tokens = self.incrementTokens(incTotalTokens)
            dpg.set_value("totalToken", "total Tokens = " + str(total_tokens))

            print(status, ", sequenceNum: ", self.sequenceInputNum, ", id: ", index_num, ", role: ", role, ", total tokens: ", total_tokens, "\n")

            responseMassage = responseMassage.replace('。', '。\n')
            responseMassage = responseMassage.replace('. ', '.\n')

            tabAnsLabel = "#_"+str(self.sequenceResponseNum) 
            dpg.set_value("TabAnsBars", tabAnsLabel)
            tabAnsLabel = "#_"+str(self.sequenceResponseNum)                 
            dpg.configure_item(tabAnsLabel, show=True)      

            dpg.set_value(responseLabel, responseMassage)
            dpg.configure_item(responseLabel, enabled=False)

            dpg.configure_item(inputLabel, enabled=False)
            if dpg.get_value(inputEnLabel) != "":
                dpg.configure_item(inputEnLabel, enabled=False)

            tabLabel = "#"+str(self.sequenceInputNum)    
            dpg.set_value("TabBars", tabLabel)
            
            # tabAnsLabel = "#_"+str(self.sequenceInputNum) 
            # dpg.set_value("TabAnsBars", tabAnsLabel)
            # tabAnsLabel = "#_"+str(self.sequenceInputNum)                 
            # dpg.configure_item(tabAnsLabel, show=True)            

            self.sequenceInputNum += 1
            tabLabel = "#"+str(self.sequenceInputNum)
            dpg.configure_item(tabLabel, show=True)

    def getTotalTokens(self):
        return self.totalTokens

    def incrementTokens(self, addTokens):
        self.totalTokens += addTokens
        return self.totalTokens

    def getSequenceNum(self):
        return self.sequenceInputNum

    def translateInput(self, sender, app_data):
        inputLabel = "input"+str(self.sequenceInputNum)
        inputText=dpg.get_value(inputLabel)

        if(inputText == ""):
            return
        else:  
            print("deepL input", inputText)
            dpg.configure_item("nowTranlating", show=True)
            inputEnText = deepL.translate(inputText, "EN")
            dpg.configure_item("nowTranlating", show=False)  
            print("deepL output", inputEnText)

            tabEnLabel = "#"+str(self.sequenceInputNum)+"_EN"
            dpg.configure_item(tabEnLabel, show=True)

            inputEnLabel = "input"+str(self.sequenceInputNum)+"_EN"
            dpg.set_value(inputEnLabel, inputEnText)   

            inputCodeLabel = "inputCode"+str(self.sequenceInputNum) 
            inputEnCodeLabel = "inputCode"+str(self.sequenceInputNum)+"_EN" 
            dpg.set_value(inputEnCodeLabel, dpg.get_value(inputCodeLabel))    

            dpg.set_value("TabBars", tabEnLabel)

    def translateOutput(self, sender, app_data):
        responseLabel = "response"+str(self.sequenceResponseNum)
        responseText = pyperclip.paste()

        if (responseText == "") or (dpg.get_value(responseLabel) == "") :
            return
        else:  
            print("deepL input En ", responseText)
            dpg.configure_item("nowTranlatingJP", show=True)
            responseJpText = deepL.translate(responseText, "JA")
            dpg.configure_item("nowTranlatingJP", show=False)  
            print("deepL output Jp ", responseJpText)

            tabJpAnsLabel = "#_"+str(self.sequenceResponseNum)+"_JP"
            dpg.configure_item(tabJpAnsLabel, show=True)

            responseJPLabel = "response"+str(self.sequenceResponseNum)+"_JP"
            dpg.set_value(responseJPLabel, responseJpText)   

            responseLabel = "responseCode"+str(self.sequenceResponseNum) 
            responseJPCodeLabel = "responseCode"+str(self.sequenceResponseNum)+"_JP" 
            dpg.set_value(responseJPCodeLabel, dpg.get_value(responseLabel))    

            dpg.set_value("TabAnsBars", tabJpAnsLabel)

def unicode_escape_sequence_to_japanese(text):
    pattern = re.compile(r'\\\\u([0-9a-fA-F]{4})')
    return pattern.sub(lambda x: chr(int(x.group(1), 16)), text)

def copyCodeAll(sender, app_data, user_data):
    responseCodeLabel = "responseCode"+str(user_data)
    getCode = dpg.get_value(responseCodeLabel)
    dpg.set_clipboard_text(getCode)

def exit(_sender, _data):
    dpg.stop_dearpygui()


def main():
    print('>> AIChat: see you ')

if __name__ == '__main__':
    # main()

    with open('key.txt', 'r') as f:
        key = f.read().strip()

    validTranslate = os.path.isfile('keyDeepL.txt')

    if validTranslate :
        with open('keyDeepL.txt', 'r') as f:
            keyDeepL = f.read().strip()

        deepL = AITranslate(keyDeepL)
    else:
        deepL = ""

    chatai = AIChat(key, deepL)

    dpg.create_context()

    with dpg.viewport_menu_bar():
        with dpg.menu(label="File"):
            # dpg.add_menu_item(label="Open", callback=openImage)
            # dpg.add_menu_item(label="SetPath", callback=setPath)
            # dpg.add_menu_item(label="Save", callback=print_me)
            # dpg.add_menu_item(label="Save As", callback=print_me)

            with dpg.menu(label="Settings"):
                # dpg.add_menu_item(label="Setting 1", callback=print_me, check=True)
                # dpg.add_menu_item(label="Setting 2", callback=print_me)
                
                dpg.add_combo(("Python", ""), label="Combo", default_value="Python")
                dpg.add_slider_float(label="temperature", show=False)

            dpg.add_menu_item(label="Reset", callback=chatai.resetChat)

            dpg.add_menu_item(label="Quit", callback=exit, user_data = chatai)

    # https://github.com/morikatron/snippet/blob/master/dear_pygui_examples/font_example.py
    # font https://fonts.google.com/noto/specimen/Noto+Sans+JP
    with dpg.font_registry():
        with dpg.font(file="./Noto_Sans_JP/NotoSansJP-Medium.otf", size=20) as default_font:
            dpg.add_font_range_hint(dpg.mvFontRangeHint_Japanese)
        dpg.bind_font(default_font)
        with dpg.font(file="./Noto_Sans_JP/NotoSansJP-Bold.otf", size=14) as small_font:
            dpg.add_font_range_hint(dpg.mvFontRangeHint_Japanese)

    dpg.create_viewport(title='openAI, gpt-3.5-turbo', width=WIDTH, height=HEIGHT)

    with dpg.window(width=WIDTH1, height=HEIGHT1, label="Assistant", tag="window2", pos=(POSX3, POSY3), horizontal_scrollbar=True):
        with dpg.group(horizontal=True):
            dpg.add_text(default_value="response from chatGPT " )
            dpg.add_button(tag="entoJpTranslation", label="Translation clipboard to JP", indent=250, callback=chatai.translateOutput, show=validTranslate)
            dpg.add_loading_indicator(tag="nowTranlatingJP", style=1, radius=1.5, thickness=1.5, show=False, color=(10,120,180))  

        with dpg.tab_bar(label="assistantTabBars", tag="TabAnsBars") :
            for i in range(SEQUENCENUMMAX + 1) :
                tabAnsLabel = "#_"+str(i)
                tabJpAnsLabel = "#_"+str(i)+"_JP"

                responseLabel = "response"+str(i)
                responseJpLabel = "response"+str(i)+"_JP"   
                responseCodeLabel = "responseCode"+str(i)
                responseJpCodeLabel = "responseCode"+str(i)+"_JP"

                copyCodeAllLabel = "copyCodeAllLabel"+str(i)

                isShowTaba = chatai.getSequenceNum() > i
                with dpg.tab(label=tabAnsLabel, tag=tabAnsLabel, show=isShowTaba):
                    dpg.add_input_text(tag=responseLabel, width=WIDTH, height=HEIGHT2, pos=(POSX5, POSY5), default_value="", multiline=True, enabled=False , tracked=True)
                    dpg.add_button(label="copy Code below", pos=(POSX5, POSY6-30+2) , callback=copyCodeAll, user_data = i)
                    dpg.add_input_text(tag=responseCodeLabel, width=WIDTH, height=HEIGHT2, pos=(POSX6, POSY6), default_value="", multiline=True, tracked=True) 

                with dpg.tab(label=tabJpAnsLabel, tag=tabJpAnsLabel, show=isShowTaba):
                    dpg.add_input_text(tag=responseJpLabel, width=WIDTH, height=HEIGHT2, pos=(POSX5, POSY5), default_value="", multiline=True, enabled=False , tracked=True)
                    dpg.add_button(label="copy Code below", pos=(POSX5, POSY6-30+2) , callback=copyCodeAll, user_data = i)
                    dpg.add_input_text(tag=responseJpCodeLabel, width=WIDTH, height=HEIGHT2, pos=(POSX6, POSY6), default_value="", multiline=True, tracked=True)

    with dpg.window(width=WIDTH1, height=HEIGHT1, label="User", tag="window1", pos=(POSX1, POSY1), horizontal_scrollbar=True):
        # https://pythonprogramming.altervista.org/input-text-examples-in-dearpygui/

        with dpg.group(horizontal=True):
            dpg.add_button(label="Ask openAI", callback=chatai.SendMessageToOpenAI)
            dpg.add_loading_indicator(tag="nowLoading", style=1, radius=1.5, thickness=1.5, show=False, color=(10,220,10)) 
            dpg.add_button(tag="jptoEnTranslation", label="Translation to EN", indent=150, callback=chatai.translateInput, show=validTranslate)
            dpg.add_loading_indicator(tag="nowTranlating", style=1, radius=1.5, thickness=1.5, show=False, color=(10,120,180))         
            dpg.add_text(tag="totalToken", default_value="total Tokens = " + str(chatai.getTotalTokens()), indent=500)
      
        with dpg.tab_bar(label="TabBars", tag="TabBars") :
            for i in range(SEQUENCENUMMAX + 1) :
                tabLabel = "#"+str(i)
                tabEnLabel = "#"+str(i)+"_EN"

                inputLabel = "input"+str(i)
                inputEnLabel = "input"+str(i)+"_EN"
                inputCodeLabel = "inputCode"+str(i) 
                inputEnCodeLabel = "inputCode"+str(i)+"_EN"                       

                isShowTab = chatai.getSequenceNum() >= i
                with dpg.tab(label=tabLabel, tag=tabLabel, show=isShowTab):
                    dpg.add_input_text(tag=inputLabel, width=WIDTH, height=HEIGHT2, pos=(POSX5, POSY5), default_value="", multiline=True, tracked=True, enabled=True, tab_input=True)
                    dpg.add_text("Code Suggestion" , pos=(POSX5, POSY6-32)) # 
                    dpg.add_input_text(tag=inputCodeLabel, width=WIDTH, height=HEIGHT2, pos=(POSX6, POSY6), default_value="", multiline=True, tracked=True, enabled=True)

                with dpg.tab(label=tabEnLabel, tag=tabEnLabel, show=False):
                    dpg.add_input_text(tag=inputEnLabel, width=WIDTH, height=HEIGHT2, pos=(POSX5, POSY5), default_value="", multiline=True, tracked=True, enabled=True, tab_input=True)
                    dpg.add_text("Code Suggestion" , pos=(POSX5, POSY6-32)) # 
                    dpg.add_input_text(tag=inputEnCodeLabel, width=WIDTH, height=HEIGHT2, pos=(POSX6, POSY6), default_value="", multiline=True, tracked=True, enabled=True)
        
    dpg.setup_dearpygui()
    dpg.show_viewport()
    dpg.start_dearpygui()
    dpg.destroy_context()
    