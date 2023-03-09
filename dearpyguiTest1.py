import dearpygui.dearpygui as dpg

def show_message(sender, data):
    # dpg.add_text("Hello, World!")
    dpg.set_value("message1", True)

dpg.create_context()
dpg.create_viewport(title='Quick Metric Calculator (alpha)', width=1750, height=825)

with dpg.window(width=400, height=300, label="My Window"):
    # add a button to trigger the message display
    dpg.add_button(label="Show Message", callback=show_message)
    dpg.add_text("Hello, World!", label="message1", show=False)

dpg.setup_dearpygui()

# show the DearPyGui viewport
dpg.show_viewport()

# start the DearPyGui event loop
dpg.start_dearpygui()

# destroy the DearPyGui context when finished
dpg.destroy_context()


