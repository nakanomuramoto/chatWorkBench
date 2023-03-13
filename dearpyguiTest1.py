import dearpygui.dearpygui as dpg

buf = ""
string = "This is a sample text.\n" * 50

def show_message(sender, data, str0):
    # dpg.add_text("Hello, World!")
    # dpg.set_value("message1", True)
    buf += str0
    dpg.set_value(text, buf)

dpg.create_context()
dpg.create_viewport(title='Quick Metric Calculator (alpha)', width=1750, height=825)

with dpg.window(width=400, height=300, label="My Window"):
    # add a button to trigger the message display
    dpg.add_button(label="Show Message", callback=show_message, user_data = string)
    dpg.add_text("Hello, World!", label="message1", show=False)

with dpg.window(label="Text Display", width=400, height=300):
    text = dpg.add_text(buf, wrap=400, parent=dpg.add_child(width=380, height=280))
    # dpg.add_scrollbar(direction=dpg.mvDir_Vertical, callback=lambda sender, data: dpg.set_item_height(text, data[0]), parent=text)

dpg.setup_dearpygui()

# show the DearPyGui viewport
dpg.show_viewport()

# start the DearPyGui event loop
dpg.start_dearpygui()

# destroy the DearPyGui context when finished
dpg.destroy_context()


