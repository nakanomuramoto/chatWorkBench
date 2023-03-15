import dearpygui.dearpygui as dpg

dpg.create_context()
dpg.create_viewport(title='test', width=1750, height=825)

# callback runs when user attempts to connect attributes
def link_callback(sender, app_data):
    # app_data -> (link_id1, link_id2)
    linkId = dpg.add_node_link(app_data[0], app_data[1], parent=sender)

    print(linkId)

    # print(app_data[0],  dpg.get_item_label(app_data[0]), dpg.get_item_info(app_data[0]))
    a1ParentTag = dpg.get_item_info(app_data[0])['parent']
    # print(a1ParentTag, dpg.get_item_label(a1ParentTag), dpg.get_item_info(a1ParentTag))

    # a1c1 = dpg.get_item_info(a1ParentTag)['children'][1][0]
    a1c2 = dpg.get_item_info(a1ParentTag)['children'][1][1]
    # a1c3 = dpg.get_item_info(a1ParentTag)['children'][1][2]
    # print(a1c1, a1c2, a1c3)

    # print(a1c1, dpg.get_item_label(a1c1), dpg.get_item_info(a1c1))
    # print(a1c2, dpg.get_item_label(a1c2), dpg.get_item_info(a1c2))
    # print(a1c3, dpg.get_item_label(a1c3), dpg.get_item_info(a1c3))

    a1c21 = dpg.get_item_info(a1c2)['children'][1][0]
    v1 = dpg.get_value(a1c21)
    print(a1c21)
    # print(a1c21, dpg.get_item_label(a1c21), dpg.get_value(a1c21))
    print("|")

    a2 = app_data[1]
    # print(a2)
    # print(a2, dpg.get_item_label(a2), dpg.get_item_info(a2))
    a2ParentTag = dpg.get_item_info(a2)['parent']
    # print(a2ParentTag, dpg.get_item_label(a2ParentTag), dpg.get_item_info(a2ParentTag))
    # a2c0 = dpg.get_item_info(a2ParentTag)['children'][1][0]
    # a2c1 = dpg.get_item_info(a2ParentTag)['children'][1][1]
    a2c2 = dpg.get_item_info(a2ParentTag)['children'][1][2]
    # print(a2c20, dpg.get_item_label(a2c20), dpg.get_item_info(a2c20))
    # print(a2c21, dpg.get_item_label(a2c21), dpg.get_item_info(a2c21))
    # print(a2c2, dpg.get_item_label(a2c2), dpg.get_item_info(a2c2))
    a2c21 = dpg.get_item_info(a2c2)['children'][1][0]
    print(a2c21)
    # print(a2c21, dpg.get_item_label(a2c21), dpg.get_item_info(a2c21))
    print()

    v2 = dpg.set_value(a2c21, v1)

# callback runs when user attempts to disconnect attributes
def delink_callback(sender, app_data):
    print(app_data,  dpg.get_item_label(app_data), dpg.get_item_info(app_data))
    aParentTag = dpg.get_item_info(app_data)['parent']
    print(aParentTag,  dpg.get_item_label(aParentTag), dpg.get_item_info(aParentTag))
    # ac0 = dpg.get_item_info(aParentTag)['children'][0][0]
    # ac10 = dpg.get_item_info(aParentTag)['children'][1][0]
    ac11 = dpg.get_item_info(aParentTag)['children'][1][1]
    # print(ac0, dpg.get_item_label(ac0), dpg.get_item_info(ac0))
    # print(ac10, dpg.get_item_label(ac10), dpg.get_item_info(ac10))
    print(ac11, dpg.get_item_label(ac11), dpg.get_item_info(ac11))
    # ac11c0 = dpg.get_item_info(ac11)['children'][1][0]
    # ac11c1 = dpg.get_item_info(ac11)['children'][1][1]
    ac11c2 = dpg.get_item_info(ac11)['children'][1][2]
    # print(ac11c0, dpg.get_item_label(ac11c0), dpg.get_item_info(ac11c0))
    # print(ac11c1, dpg.get_item_label(ac11c1), dpg.get_item_info(ac11c1))
    print(ac11c2, dpg.get_item_label(ac11c2), dpg.get_item_info(ac11c2))
    ac11c2c0 = dpg.get_item_info(ac11c2)['children'][1][0]
    print(ac11c2c0, dpg.get_item_label(ac11c2c0), dpg.get_item_info(ac11c2c0))
    dpg.set_value(ac11c2c0, " - ")

    # app_data -> link_id
    dpg.delete_item(app_data)

def update_slider(sender, data):
    value = dpg.get_value(sender)
    dpg.set_value("slider1", value)

with dpg.window(tag="MainWindow", width=640, height=480, label="My Window"):
    # add a button to trigger the message display
    dpg.add_text(tag="slider1", label="message1", show=True)
    # add a node
    with dpg.node_editor(tag="nodeEditor", callback=link_callback, delink_callback=delink_callback):
        with dpg.node(tag="N1", label="Node 1", pos=[100, 100]):
            # with dpg.node_attribute(label="Node A1input", attribute_type=dpg.mvNode_Attr_Input, show=False):
            #     pass
            dpg.add_node_attribute(tag="N1in", attribute_type=dpg.mvNode_Attr_Input, show=False)

            with dpg.node_attribute(tag="N1contents", label="NodeA1", attribute_type=dpg.mvNode_Attr_Static):
                # A1Text = dpg.add_text(default_value="This is a Node 1.")
                dpg.add_slider_float(tag="Slider", min_value=0.0, max_value=100.0, callback=update_slider)
            
            dpg.add_node_attribute(tag="N1out", attribute_type=dpg.mvNode_Attr_Output, show=True)

        with dpg.node(tag="N2", label="Node 2", pos=[300, 100]):
            dpg.add_node_attribute(tag="N2in", attribute_type=dpg.mvNode_Attr_Input, show=True)
            dpg.add_node_attribute(attribute_type=dpg.mvNode_Attr_Output, show=False)

            with dpg.node_attribute(tag="N2contents", label="Node A2", attribute_type=dpg.mvNode_Attr_Static):
                dpg.add_text(" - ")


dpg.setup_dearpygui()

# show the DearPyGui viewport
dpg.show_viewport()

# start the DearPyGui event loop
dpg.start_dearpygui()

# destroy the DearPyGui context when finished
dpg.destroy_context()
