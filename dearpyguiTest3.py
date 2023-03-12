import dearpygui.dearpygui as dpg

POSX0, POSY0 = 10, 10
POSX1, POSY1 = 500, POSY0

def show_message():
    dpg.configure_item("message1", show=True)
    dpg.set_value("message1", "Button clicked!")

def showText(sender, data):
    dpg.configure_item("message1", show=True)
    inputText=dpg.get_value("input1")
    dpg.set_value("message1", inputText)
    print(inputText)


if __name__ == "__main__":
    dpg.create_context()

    # https://github.com/morikatron/snippet/blob/master/dear_pygui_examples/font_example.py
    # font https://fonts.google.com/noto/specimen/Noto+Sans+JP
    with dpg.font_registry():
        with dpg.font(file="./Noto_Sans_JP/NotoSansJP-Medium.otf", size=20) as default_font:
            dpg.add_font_range_hint(dpg.mvFontRangeHint_Japanese)
        dpg.bind_font(default_font)
        with dpg.font(file="./Noto_Sans_JP/NotoSansJP-Bold.otf", size=14) as small_font:
            dpg.add_font_range_hint(dpg.mvFontRangeHint_Japanese)

    dpg.create_viewport(title='openAI, gpt-3.5-turbo', width=1440, height=720)

    with dpg.window(width=400, height=300, label="My Window", tag="test1", pos=(POSX0, POSY0)):
        dpg.add_text("Hello, World!", tag="message1", show=False)
        dpg.add_button(label="Click me", callback=show_message)

    def on_text_changed(sender, data):
        print(dpg.get_value(sender))

    # with dpg.font_registry():
    #     dpg.add_font("NotoSansCJKjp-Regular.otf", 20, "japanese") # default_font=True)


    with dpg.window(label="Text Input", tag="w1", pos=(POSX1, POSY1)):
        # dpg.add_input_text(label="Enter Text", callback=on_text_changed)
        # https://pythonprogramming.altervista.org/input-text-examples-in-dearpygui/
        dpg.add_input_text(label="Enter Text", tag="input1", width=300, multiline=True, default_value="")
        dpg.add_button(label="Send", callback=showText)

    dpg.setup_dearpygui()
    dpg.show_viewport()
    dpg.start_dearpygui()
    dpg.destroy_context()
