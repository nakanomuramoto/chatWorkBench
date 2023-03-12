import dearpygui.dearpygui as dpg
# import dearpygui._dearpygui as internal_dpg

g_list = [
    [0x3041, 0x3096],
    [0x30A0, 0x30FF],
    [0x3400, 0x4DB5],
    [0x4E00, 0x9FCB],
    [0xF900, 0xFA6A],
    [0x2E80, 0x2FD5],
    [0xFF5F, 0xFF9F],
    [0x3000, 0x303F],
    [0x31F0, 0x31FF],
    [0x3220, 0x3243],
    [0x3280, 0x337F],
    [0xFF01, 0xFF5E],
    [0x0000, 0x007F]
]

# "./data/NotoSansCJKjp-Medium.otf",
# dpg.add_additional_font("D:/git/DearPyGui/assets/NotoSerifCJKjp-Medium.otf", 
                    # 24, custom_glyph_ranges=g_list)

# add_additional_font("./data/NotoSansCJKjp-Medium.otf", 24, "japanese")

def show_message():
    dpg.configure_item("message1", show=True)
    dpg.set_value("message1", "Button clicked!")


dpg.create_context()

with dpg.font_registry():
    with dpg.font(file="./Noto_Sans_JP/NotoSansJP-Medium.otf", size=20) as default_font:
        dpg.add_font_range_hint(dpg.mvFontRangeHint_Japanese)
    dpg.bind_font(default_font)
    with dpg.font(file="./Noto_Sans_JP/NotoSansJP-Bold.otf", size=14) as small_font:
        dpg.add_font_range_hint(dpg.mvFontRangeHint_Japanese)

with dpg.window(label="Main Window", tag="Main Window"):
    dpg.add_text("フォントの設定を行うと日本語が表示できます")
    dpg.add_separator()
    with dpg.group(tag="license"):
        dpg.add_text("本プログラムでは表示フォントに「Noto Sans JP」(https://fonts.google.com/noto/specimen/Noto+Sans+JP) を使用しています。")
        dpg.add_text("Licensed under SIL Open Font License 1.1 (http://scripts.sil.org/OFL)")
        dpg.bind_item_font("license", small_font)

dpg.create_viewport(title='test', width=1440, height=720)

with dpg.window(width=400, height=300, label="My Window", tag="test1"):
    dpg.add_text("Hello, World!", label="message1", show=False)
    dpg.add_button(label="Click me", callback=show_message)

def on_text_changed(sender, data):
    print(dpg.get_value(sender))

# with dpg.font_registry():
#     dpg.add_font("NotoSansCJKjp-Regular.otf", 20, "japanese") # default_font=True)


with dpg.window(label="Text Input", tag="w1"):
    # dpg.add_font("NotoSerifCJKjp-Medium.otf", 20, custom_glyph_ranges=g_list, parent="w1")
    dpg.add_input_text(label="Enter Text", callback=on_text_changed)

dpg.setup_dearpygui()
dpg.show_viewport()
dpg.start_dearpygui()
dpg.destroy_context()
